"""
geolib — the Week 5 toolkit: channels, high-dimensional views and maps.

Week 3 gave you `vizlib` (palette, Lie Factor, colour-blindness simulation).
Week 4 added `tslib`. This week sits on top of `vizlib` the same way, so a
Week 5 figure inherits the Week 3 palette and export rules by construction.

**It needs no GIS stack.** Boundaries are shipped as plain GeoJSON and read
with the standard-library `json` module; the projections, the classification
schemes and the polygon drawing are all in here, in about 300 lines. If you
have `geopandas` and `mapclassify` installed you are welcome to use them
instead — say so in your write-up — but nothing this week requires them, and
every number in `TASKS.md` was produced with the functions below.

What lives here:

    read_geojson()        boundaries -> plain dicts, no GIS install
    outlines()            the boundary layer, to sit under symbols
    polygon_area_km2()    exact spherical area; the answer is in km2
    equal_area_xy()       project before you colour an area  (slide 34)
    mercator_xy()         for comparison, so you can measure the damage
    representative_point()  a point guaranteed inside the polygon  (slide 42)

    breaks()              equal-interval, quantile and Jenks  (slide 39)
    gvf()                 goodness of variance fit, to score them
    choropleth()          draw it, classified and legended  (slide 36)
    prop_symbols()        sqrt-scaled symbols on a map       (slide 42)
    size_legend()         the three reference circles        (slide 11)

    scale_frame()         min-max / z-score / rank           (slide 22)
    corr_chain()          greedy axis order by |r|           (slide 24)
    pcp()                 parallel coordinates, grey + brush (slide 25)
    funnel_limits()       Poisson limits for small-area rates (slide 45)

Run `python3 geolib.py` for a self-check.
"""

from __future__ import annotations

import json
import math

import numpy as np
import pandas as pd

from vizlib import PALETTE, MARKERS, style_defaults, save_fig  # noqa: F401

__all__ = [
    "PALETTE", "MARKERS", "style_defaults", "save_fig",
    "read_geojson", "polygon_area_km2", "equal_area_xy", "mercator_xy",
    "plate_carree_xy", "representative_point", "outlines",
    "breaks", "gvf", "choropleth", "prop_symbols", "size_legend",
    "scale_frame", "corr_chain", "pcp", "funnel_limits",
]

R_EARTH_KM = 6371.0088


# ============================================================ reading geometry
def read_geojson(path):
    """
    A GeoJSON FeatureCollection of Polygons -> a list of plain dicts:

        {"code": ..., "name": ..., "ring": [(lon, lat), ...], **properties}

    Only the outer ring of each polygon is kept, which is all the boundaries
    in `data/` have. No geopandas, no shapely, no CRS object — and therefore
    no CRS, which is the point of `equal_area_xy()` below.
    """
    with open(path) as fh:
        gj = json.load(fh)
    out = []
    for feat in gj["features"]:
        geom = feat["geometry"]
        if geom["type"] != "Polygon":
            raise ValueError(f"expected Polygon, got {geom['type']}")
        ring = [tuple(p) for p in geom["coordinates"][0]]
        if ring[0] == ring[-1]:
            ring = ring[:-1]
        rec = dict(feat.get("properties", {}))
        rec["ring"] = ring
        out.append(rec)
    return out


def polygon_area_km2(ring):
    """
    Exact area on a sphere, in square kilometres, by spherical excess.

    Use this and never the shoelace formula on raw longitude/latitude: a
    square degree is about 12,364 km2 at the equator and 6,088 km2 at 60
    degrees, so a degree-space area silently over-weights whatever is
    furthest from the equator. Slide 33.
    """
    ring = list(ring)
    if ring[0] == ring[-1]:
        ring = ring[:-1]
    lon = np.radians([p[0] for p in ring])
    lat = np.radians([p[1] for p in ring])
    n = len(lon)
    total = 0.0
    for k in range(n):
        k2 = (k + 1) % n
        total += (lon[k2] - lon[k]) * (2 + np.sin(lat[k]) + np.sin(lat[k2]))
    return abs(total * R_EARTH_KM ** 2 / 2.0)


# ================================================================ projections
def equal_area_xy(lon, lat, lat_ts=None):
    """
    Lambert cylindrical equal-area, in kilometres.

    `lat_ts` is the latitude of true scale. It defaults to the mean latitude
    of whatever you pass in, which is right for one whole country in one
    call — but if you call this once PER POLYGON and let it default, every
    polygon gets a different projection and the districts stop tiling. That
    is slide 33's "two layers, two CRSs" in miniature. `choropleth()`,
    `outlines()` and `prop_symbols()` all share one reference latitude
    across the whole collection for exactly this reason. Shapes
    stretch a little, but a square centimetre means the same number of square
    kilometres everywhere on the sheet — which is the only property a
    choropleth actually needs, because area IS its encoding channel.
    """
    lon = np.asarray(lon, dtype=float)
    lat = np.asarray(lat, dtype=float)
    if lat_ts is None:
        lat_ts = float(np.mean(lat))
    k0 = math.cos(math.radians(lat_ts))
    x = R_EARTH_KM * np.radians(lon) * k0
    y = R_EARTH_KM * np.sin(np.radians(lat)) / k0
    return x, y


def mercator_xy(lon, lat):
    """
    Web Mercator, in kilometres. Conformal: it keeps angles and inflates
    area by sec(latitude), so it is for tiles and navigation and never for
    a choropleth. Here so that you can measure what it would have cost you.
    """
    lon = np.asarray(lon, dtype=float)
    lat = np.asarray(np.clip(lat, -85.05, 85.05), dtype=float)
    x = R_EARTH_KM * np.radians(lon)
    y = R_EARTH_KM * np.log(np.tan(np.pi / 4 + np.radians(lat) / 2))
    return x, y


def plate_carree_xy(lon, lat):
    """Longitude and latitude used directly as x and y. This is what you get
    by default when you plot raw coordinates, and it is equal-area nowhere."""
    return np.asarray(lon, dtype=float), np.asarray(lat, dtype=float)


_PROJ = {"equal_area": equal_area_xy, "mercator": mercator_xy,
         "degrees": plate_carree_xy}


def representative_point(ring):
    """
    A (lon, lat) point inside the polygon, for placing a symbol or a label.

    The vertex mean is inside for a convex ring; if the ring is concave the
    mean can fall outside it, so this falls back to the mid-point of the
    widest horizontal chord. Slide 42 — a centroid that lands in the sea is
    the classic proportional-symbol bug.
    """
    ring = list(ring)
    if ring[0] == ring[-1]:
        ring = ring[:-1]
    xs = np.array([p[0] for p in ring])
    ys = np.array([p[1] for p in ring])
    cx, cy = float(xs.mean()), float(ys.mean())
    if _point_in_ring(cx, cy, ring):
        return cx, cy
    y0 = float(np.median(ys))
    cuts = []
    n = len(ring)
    for k in range(n):
        (x1, y1), (x2, y2) = ring[k], ring[(k + 1) % n]
        if (y1 - y0) * (y2 - y0) < 0:
            cuts.append(x1 + (y0 - y1) * (x2 - x1) / (y2 - y1))
    cuts.sort()
    if len(cuts) >= 2:
        return (cuts[0] + cuts[1]) / 2.0, y0
    return cx, cy


def _collection_lat_ts(feats):
    """The single reference latitude every layer of one map must share."""
    lats = [p[1] for f in feats for p in f["ring"]]
    return float(np.mean(lats))


def _project_ring(ring, projection, lat_ts):
    xs = [p[0] for p in ring]
    ys = [p[1] for p in ring]
    if projection == "equal_area":
        return equal_area_xy(xs, ys, lat_ts=lat_ts)
    return _PROJ[projection](xs, ys)


def _point_in_ring(x, y, ring):
    inside = False
    n = len(ring)
    for k in range(n):
        (x1, y1), (x2, y2) = ring[k], ring[(k + 1) % n]
        if (y1 > y) != (y2 > y):
            xx = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xx:
                inside = not inside
    return inside


# ============================================================ classification
def breaks(values, scheme="natural", k=5):
    """
    Class breaks for a choropleth: `k + 1` edges, lowest first. Slide 39.

        "equal"     even steps across the range. One outlier empties
                    four of the five classes.
        "quantile"  equal counts per class. Always looks full, and will
                    happily invent a five-level gradient out of noise.
        "natural"   Jenks: minimise within-class variance. Exact dynamic
                    programming here, not the usual k-means approximation.
    """
    v = np.sort(np.asarray(values, dtype=float))
    v = v[~np.isnan(v)]
    if k < 1 or len(v) < k:
        raise ValueError(f"need at least k={k} values, got {len(v)}")
    if scheme == "equal":
        return list(np.linspace(v[0], v[-1], k + 1))
    if scheme == "quantile":
        return list(np.quantile(v, np.linspace(0, 1, k + 1)))
    if scheme != "natural":
        raise ValueError("scheme must be 'equal', 'quantile' or 'natural'")

    n = len(v)
    csum = np.concatenate([[0.0], np.cumsum(v)])
    csum2 = np.concatenate([[0.0], np.cumsum(v ** 2)])

    def sse(i, j):                       # inclusive i..j-1, 0-based
        m = j - i
        if m <= 0:
            return 0.0
        s = csum[j] - csum[i]
        return (csum2[j] - csum2[i]) - s * s / m

    INF = float("inf")
    cost = np.full((k + 1, n + 1), INF)
    cut = np.zeros((k + 1, n + 1), dtype=int)
    cost[0, 0] = 0.0
    for c in range(1, k + 1):
        for j in range(c, n + 1):
            for i in range(c - 1, j):
                val = cost[c - 1, i] + sse(i, j)
                if val < cost[c, j]:
                    cost[c, j] = val
                    cut[c, j] = i
    # Walk the DP back. cut[c, j] = i means class c holds sorted indices
    # i .. j-1, so the edge BELOW class c is the top of the class under it,
    # v[i-1]. Emitting class upper bounds (rather than lower starts) is what
    # makes `class_of`'s right-inclusive digitize reproduce this partition.
    starts, j = [], n
    for c in range(k, 0, -1):
        i = cut[c, j]
        starts.append(i)
        j = i
    starts = list(reversed(starts))            # length k, starts[0] == 0
    edges = [float(v[0])]
    for i in starts[1:]:
        edges.append(float(v[i - 1]))
    edges.append(float(v[-1]))
    return edges


def gvf(values, edges):
    """
    Goodness of variance fit: 1 - (within-class SSE / total SSE).

    Jenks maximises it by construction, quantile usually scores worst. Report
    it when you justify a scheme — it turns "it looked better" into a number.
    """
    v = np.asarray(values, dtype=float)
    v = v[~np.isnan(v)]
    sdam = float(((v - v.mean()) ** 2).sum())
    if sdam == 0:
        return 1.0
    idx = np.clip(np.digitize(v, edges[1:-1], right=True), 0, len(edges) - 2)
    scdm = 0.0
    for c in np.unique(idx):
        g = v[idx == c]
        scdm += float(((g - g.mean()) ** 2).sum())
    return 1.0 - scdm / sdam


def class_of(values, edges):
    """Which class each value falls in, 0-based."""
    v = np.asarray(values, dtype=float)
    return np.clip(np.digitize(v, edges[1:-1], right=True), 0, len(edges) - 2)


# ================================================================== map marks
def choropleth(ax, feats, values, scheme="natural", k=5, cmap=None,
               projection="equal_area", edgecolor="white", lw=0.35,
               legend=True, legend_title="", fmt="{:,.0f}",
               legend_loc="upper left", legend_anchor=(1.0, 1.0)):
    """
    Colour each polygon by one number about it. Returns the class edges.

    `values` is a dict keyed by the feature's `code`, or a sequence in the
    same order as `feats`. The projection defaults to equal-area because
    colouring an area with a quantity makes area the encoding channel, and
    an area-distorting projection distorts the chart itself. Slide 34.
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon as MplPolygon
    from matplotlib.collections import PatchCollection

    if isinstance(values, dict):
        vals = np.array([values[f["code"]] for f in feats], dtype=float)
    else:
        vals = np.asarray(values, dtype=float)
    edges = breaks(vals, scheme=scheme, k=k)
    idx = class_of(vals, edges)
    cm = plt.get_cmap(cmap or PALETTE["sequential"])
    shades = [cm(0.18 + 0.78 * c / max(k - 1, 1)) for c in range(k)]

    lat_ts = _collection_lat_ts(feats)
    patches, colours = [], []
    for f, c in zip(feats, idx):
        x, y = _project_ring(list(f["ring"]), projection, lat_ts)
        patches.append(MplPolygon(np.column_stack([x, y]), closed=True))
        colours.append(shades[int(c)])
    ax.add_collection(PatchCollection(patches, facecolors=colours,
                                      edgecolors=edgecolor, linewidths=lw))
    ax.autoscale_view()
    ax.set_aspect("equal")
    ax.set_axis_off()

    if legend:
        from matplotlib.patches import Patch
        labels = [f"{fmt.format(edges[c])} – {fmt.format(edges[c + 1])}"
                  for c in range(k)]
        ax.legend(handles=[Patch(facecolor=shades[c], edgecolor=edgecolor,
                                 label=labels[c]) for c in range(k)],
                  title=legend_title or None, loc=legend_loc,
                  bbox_to_anchor=legend_anchor, fontsize=8,
                  title_fontsize=8, frameon=False)
    return edges


def outlines(ax, feats, projection="equal_area", color=None, lw=0.6,
             facecolor="none"):
    """Draw the boundaries only. Put this under `prop_symbols` so the
    symbols have geography beneath them instead of floating in space."""
    from matplotlib.patches import Polygon as MplPolygon
    from matplotlib.collections import PatchCollection
    lat_ts = _collection_lat_ts(feats)
    patches = []
    for f in feats:
        x, y = _project_ring(list(f["ring"]), projection, lat_ts)
        patches.append(MplPolygon(np.column_stack([x, y]), closed=True))
    ax.add_collection(PatchCollection(
        patches, facecolors=facecolor,
        edgecolors=color or PALETTE["grid"], linewidths=lw))
    ax.autoscale_view()
    ax.set_aspect("equal")
    ax.set_axis_off()
    return ax


def prop_symbols(ax, feats, values, projection="equal_area", max_pt=900,
                 color=None, alpha=0.62, edgecolor="white"):
    """
    One symbol per unit, at a point guaranteed inside it, with **area**
    proportional to the value — so the radius goes as the square root.
    Slides 10 and 42. Returns the (x, y, s) arrays actually drawn.
    """
    if isinstance(values, dict):
        vals = np.array([values[f["code"]] for f in feats], dtype=float)
    else:
        vals = np.asarray(values, dtype=float)
    pts = [representative_point(f["ring"]) for f in feats]
    lat_ts = _collection_lat_ts(feats)
    if projection == "equal_area":
        x, y = equal_area_xy([p[0] for p in pts], [p[1] for p in pts],
                             lat_ts=lat_ts)
    else:
        x, y = _PROJ[projection]([p[0] for p in pts], [p[1] for p in pts])
    s = max_pt * vals / vals.max()                 # s is AREA in points^2
    ax.scatter(x, y, s=s, color=color or PALETTE["highlight"],
               alpha=alpha, edgecolor=edgecolor, linewidth=0.7, zorder=5)
    return x, y, s


def size_legend(ax, values, max_pt=900, n=3, color=None, title="",
                loc="upper left", bbox_to_anchor=(1.0, 1.0), fmt="{:,.0f}"):
    """
    The three reference circles from slide 11 — small, middle, large, with
    real values on them. Without this, area is decoration and not data.
    """
    vals = np.asarray(values, dtype=float)
    picks = [vals.min(), np.median(vals), vals.max()][:n] if n == 3 else \
        list(np.quantile(vals, np.linspace(0, 1, n)))
    handles = []
    for v in picks:
        handles.append(ax.scatter([], [], s=max_pt * v / vals.max(),
                                  color=color or PALETTE["muted"],
                                  alpha=0.65, edgecolor="white",
                                  label=fmt.format(v)))
    return ax.legend(handles=handles, title=title or None, loc=loc,
                     bbox_to_anchor=bbox_to_anchor, labelspacing=1.6,
                     borderpad=0.9, frameon=False, fontsize=8,
                     title_fontsize=8, scatterpoints=1)


# ===================================================== high-dimensional views
def scale_frame(df, cols, how="minmax"):
    """
    Put every axis on a common range. Slide 22 — and the one you pick is an
    argument, so name it on the figure.

        "minmax"  0-1 on the observed range. One extreme value flattens
                  the axis and crushes everything else into the bottom.
        "zscore"  mean 0, sd 1. Keeps relative gaps, still outlier-sensitive.
        "rank"    percentile rank. Immune to outliers, and it throws away
                  how big the gaps were.
    """
    X = df[list(cols)].astype(float)
    if how == "minmax":
        rng = X.max() - X.min()
        return (X - X.min()) / rng.replace(0, np.nan)
    if how == "zscore":
        return (X - X.mean()) / X.std(ddof=0).replace(0, np.nan)
    if how == "rank":
        return X.rank(pct=True)
    raise ValueError("how must be 'minmax', 'zscore' or 'rank'")


def corr_chain(df, cols):
    """
    A defensible axis order for a parallel coordinates plot: start at the
    strongest-correlated pair, then always hop to the strongest remaining
    neighbour. Slide 24 — five axes have 60 distinct orders and you are
    going to show exactly one of them, so choose it before you look.
    """
    cols = list(cols)
    r = df[cols].corr().abs()
    np.fill_diagonal(r.values, 0.0)
    i, j = np.unravel_index(np.argmax(r.values), r.shape)
    order = [cols[i], cols[j]]
    while len(order) < len(cols):
        rest = [c for c in cols if c not in order]
        order.append(max(rest, key=lambda c: r.loc[order[-1], c]))
    return order


def pcp(ax, df, cols, how="minmax", highlight=None, hl_color=None,
        bg_color=None, lw_bg=0.7, lw_hl=1.6, alpha_bg=0.55):
    """
    Parallel coordinates: one row becomes one polyline across rescaled
    vertical axes. Grey everything, then draw the brushed subset on top —
    z-order is the whole technique. Slide 25.

    `highlight` is a boolean mask. The real min and max of each axis are
    printed at its foot and head, because the scaled numbers mean nothing.
    """
    from matplotlib.collections import LineCollection

    cols = list(cols)
    N = scale_frame(df, cols, how)
    xs = np.arange(len(cols))
    seg = [np.column_stack([xs, N.iloc[i].to_numpy()]) for i in range(len(N))]
    if highlight is None:
        highlight = np.zeros(len(N), dtype=bool)
    highlight = np.asarray(highlight, dtype=bool)

    ax.add_collection(LineCollection(
        [s for s, h in zip(seg, highlight) if not h],
        colors=bg_color or PALETTE["muted"], linewidths=lw_bg,
        alpha=alpha_bg, zorder=2))
    if highlight.any():
        ax.add_collection(LineCollection(
            [s for s, h in zip(seg, highlight) if h],
            colors=hl_color or PALETTE["highlight"], linewidths=lw_hl,
            zorder=3))
    for x in xs:
        ax.axvline(x, color=PALETTE["grid"], lw=1.0, zorder=1)
    ax.set_xlim(-0.08, len(cols) - 0.92)
    ax.set_ylim(-0.06, 1.06)
    ax.set_xticks(xs)
    ax.set_xticklabels([c.replace("_", "\n") for c in cols], fontsize=8)
    ax.set_yticks([])
    for sp in ("left", "right", "top"):
        ax.spines[sp].set_visible(False)
    for x, c in zip(xs, cols):
        ax.annotate(f"{df[c].min():,.0f}", (x, -0.045), ha="center",
                    va="top", fontsize=7.5, color=PALETTE["ink_soft"])
        ax.annotate(f"{df[c].max():,.0f}", (x, 1.045), ha="center",
                    va="bottom", fontsize=7.5, color=PALETTE["ink_soft"])
    return N


def funnel_limits(population, pooled_rate, per=100_000, z=1.96):
    """
    Poisson control limits for a rate against the population behind it.
    Slide 45: points inside the funnel are noise, whatever the map suggests.

    Returns a DataFrame sorted by population with `lo` and `hi` columns in
    the same units as `pooled_rate`.
    """
    pop = np.asarray(population, dtype=float)
    lam = pooled_rate / per * pop                  # expected count
    lo = (lam - z * np.sqrt(lam)) / pop * per
    hi = (lam + z * np.sqrt(lam)) / pop * per
    out = pd.DataFrame({"population": pop, "expected": lam,
                        "lo": np.maximum(lo, 0.0), "hi": hi})
    return out.sort_values("population").reset_index(drop=True)


# ===================================================================== check
if __name__ == "__main__":
    import itertools
    import os

    print(__doc__.strip().splitlines()[0])
    print("-" * 68)
    here = os.path.dirname(os.path.abspath(__file__))
    D = os.path.join(here, "data")

    # ---- geometry -------------------------------------------------------
    feats = read_geojson(os.path.join(D, "districts.geojson"))
    areas = np.array([polygon_area_km2(f["ring"]) for f in feats])
    df = pd.read_csv(os.path.join(D, "district_health.csv"))
    print(f"read_geojson     {len(feats)} districts, "
          f"{areas.sum():,.0f} km2 total")
    assert len(feats) == 24
    merged = df.set_index("code").loc[[f["code"] for f in feats]]
    assert np.allclose(areas, merged.area_km2.to_numpy(), rtol=2e-3), \
        "the shipped area_km2 column disagrees with the geometry"
    print(f"polygon_area_km2 agrees with the shipped area_km2 column "
          f"(max {np.abs(areas / merged.area_km2 - 1).max() * 100:.3f}% off)")

    # a 1x1 degree cell is a known quantity, so the formula is checkable
    cell = [(70, 0), (71, 0), (71, 1), (70, 1)]
    exact = R_EARTH_KM ** 2 * math.radians(1) * math.sin(math.radians(1))
    assert abs(polygon_area_km2(cell) - exact) / exact < 1e-9
    print(f"                 1x1 deg at the equator = "
          f"{polygon_area_km2(cell):,.0f} km2 (exact)")

    for f in feats:
        px, py = representative_point(f["ring"])
        assert _point_in_ring(px, py, list(f["ring"])), f["code"]
    print("representative_point  inside the polygon for all 24")

    # ---- projections ----------------------------------------------------
    lat_mid = np.array([representative_point(f["ring"])[1] for f in feats])
    mer = areas / np.cos(np.radians(lat_mid))
    print(f"mercator_xy      area inflation {mer.min() / areas.min():.3f}x "
          f"south .. {mer.max() / areas.max():.3f}x north")

    # ---- classification -------------------------------------------------
    rate = (df.cases / df.population * 1e5).to_numpy()
    scores = {}
    for sch in ("equal", "quantile", "natural"):
        e = breaks(rate, sch, 5)
        scores[sch] = gvf(rate, e)
        assert len(e) == 6 and e == sorted(e)
    print("breaks/gvf       " + "  ".join(f"{k}={v:.3f}"
                                          for k, v in scores.items()))
    assert scores["natural"] >= max(scores.values()) - 1e-12, \
        "Jenks must score highest by construction"

    # Jenks must match brute force on a small sample
    sm = np.sort(rate[:9])
    bf = None
    for cuts in itertools.combinations(range(1, 9), 2):
        parts = np.split(sm, cuts)
        s = sum(((p - p.mean()) ** 2).sum() for p in parts if len(p))
        if bf is None or s < bf[0]:
            bf = (s, cuts)
    e3 = breaks(sm, "natural", 3)
    idx = class_of(sm, e3)
    mine = sum(((sm[idx == c] - sm[idx == c].mean()) ** 2).sum()
               for c in np.unique(idx))
    assert abs(mine - bf[0]) < 1e-9, (mine, bf[0])
    print(f"                 Jenks matches brute force on n=9, k=3 "
          f"(SSE {mine:.4f})")

    # ---- high-dimensional ----------------------------------------------
    hi = pd.read_csv(os.path.join(D, "health_indicators.csv"))
    COLS = ["gdp_pc", "healthcare_access", "urban_pct", "median_age",
            "cases_per_100k"]
    for how in ("minmax", "zscore", "rank"):
        S = scale_frame(hi, COLS, how)
        assert S.notna().all().all()
    mm = scale_frame(hi, COLS, "minmax")["gdp_pc"]
    print(f"scale_frame      min-max puts {(mm < 0.10).sum()} of "
          f"{len(mm)} countries below 0.10 on gdp_pc — one outlier does that")
    chain = corr_chain(hi, COLS)
    print(f"corr_chain       {' -> '.join(chain)}")
    assert abs(chain.index("healthcare_access")
               - chain.index("cases_per_100k")) == 1

    fl = funnel_limits([5_000, 50_000, 500_000], 9.0)
    assert (fl.hi - fl.lo).is_monotonic_decreasing
    print(f"funnel_limits    at 9/100k the 95% band is "
          f"{fl.hi[0] - fl.lo[0]:.1f} wide at pop 5,000 and "
          f"{fl.hi[2] - fl.lo[2]:.1f} at pop 500,000")

    # ---- draw something -------------------------------------------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    style_defaults()
    fig, axs = plt.subplots(1, 3, figsize=(13, 4.2))
    e = choropleth(axs[0], feats, dict(zip(df.code, rate)), "natural", 5,
                   legend_title="Cases per 100k")
    axs[0].set_title("choropleth — natural breaks", fontsize=10)
    outlines(axs[1], feats)
    prop_symbols(axs[1], feats, dict(zip(df.code, df.cases)), max_pt=420)
    size_legend(axs[1], df.cases.to_numpy(), max_pt=420, title="Cases")
    axs[1].set_title("prop_symbols — area, not radius", fontsize=10)
    pcp(axs[2], hi, chain, "minmax",
        highlight=(hi.region == "Andara").to_numpy())
    axs[2].set_title("pcp — grey, then brush one region", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(here, "_geolib_selfcheck.png"), dpi=90)
    plt.close(fig)
    print("choropleth/prop_symbols/pcp  drew _geolib_selfcheck.png")

    print("-" * 68)
    print("all checks passed — geolib is working.")
