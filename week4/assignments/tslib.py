"""
tslib — the Week 4 toolkit: time axes, windows, shares and hierarchies.

Week 3 gave you `vizlib` (palette, Lie Factor, colour-blindness simulation).
This week sits on top of it — `tslib` imports the palette and the export
helper from `vizlib` rather than redefining them, so a Week 4 figure looks
like a Week 3 figure by construction.

Six things live here, and you are expected to use all six:

    audit_index()        the six checks from slide 10, run in one call
    window_report()      what a rolling window costs you, in numbers
    lag_at_turn()        how late a trailing mean finds a turning point
    banked_figsize()     Cleveland's 45-degree rule, computed not guessed
    exclusivity_check()  slide 32's first test, before you draw any share
    rollup_other()       an "Other" bucket that declares what it hides

plus three hierarchy marks that need no new install beyond `squarify`:

    treemap()            squarified, with the values printed on the blocks
    sunburst()           the same tree bent round a circle, in polar bars
    cycle_plot()         fold a series so the seasonal cycle lines up

Run `python3 tslib.py` for a self-check.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from vizlib import PALETTE, MARKERS, style_defaults, save_fig  # noqa: F401

__all__ = [
    "PALETTE", "MARKERS", "style_defaults", "save_fig",
    "audit_index", "reindex_full", "window_report", "lag_at_turn",
    "banked_figsize", "exclusivity_check", "rollup_other",
    "treemap", "sunburst", "cycle_plot",
]


# ===================================================================== time
def audit_index(obj, freq: str) -> dict:
    """
    Slide 10, as one call. Run this before you plot anything with a date on
    the x axis, and put its output in your write-up.

    `obj` is a Series or DataFrame that already has a DatetimeIndex (or a
    column you have set as one). `freq` is what you believe the spacing is
    — "h", "D", "MS", and so on.

    Returns a dict with the six things that break time charts:

        dtype_ok        the index really is datetime64, not object
        monotonic       it is sorted
        n_duplicated    timestamps appearing more than once
        n_missing       periods inside the range that were never recorded
        missing_dates   the first few of them, so you can look them up
        partial_tail    the last period holds fewer rows than the one before

    Nothing here is clever. It is the set of checks that, left out, make
    every rolling window and resample you write afterwards quietly wrong.
    """
    idx = obj.index
    out = {
        "dtype_ok": pd.api.types.is_datetime64_any_dtype(idx),
        "monotonic": bool(idx.is_monotonic_increasing),
        "n_rows": int(len(obj)),
    }
    if not out["dtype_ok"]:
        out["n_duplicated"] = out["n_missing"] = None
        out["missing_dates"] = []
        out["partial_tail"] = None
        return out

    out["n_duplicated"] = int(idx.duplicated().sum())
    full = pd.date_range(idx.min(), idx.max(), freq=freq)
    missing = full.difference(idx)
    out["n_missing"] = int(len(missing))
    out["missing_dates"] = [str(d) for d in missing[:12]]
    out["span"] = (str(idx.min()), str(idx.max()))

    # a final period that is shorter than the one before it
    per = idx.to_period(_period_alias(freq))
    counts = pd.Series(1, index=per).groupby(level=0).sum()
    out["partial_tail"] = bool(
        len(counts) > 1 and counts.iloc[-1] < 0.8 * counts.iloc[:-1].median())
    out["tail_period"] = str(counts.index[-1]) if len(counts) else None
    out["tail_count"] = int(counts.iloc[-1]) if len(counts) else 0
    return out


def _period_alias(freq: str) -> str:
    """The period a partial tail would be measured in, for a given freq."""
    f = freq.upper()
    if f.startswith("H"):
        return "D"
    if f.startswith("D") or f.startswith("W"):
        return "M"
    return "Y"


def reindex_full(s: pd.Series, freq: str) -> pd.Series:
    """Put the calendar back. Missing periods become NaN, and matplotlib
    breaks the line at NaN — which is the honest picture."""
    return s.reindex(pd.date_range(s.index.min(), s.index.max(), freq=freq))


def window_report(s: pd.Series, windows=(7, 28, 91), center: bool = True
                  ) -> pd.DataFrame:
    """
    What each rolling window actually costs. Slide 21, computed.

    For every window: the standard deviation that survives smoothing, the
    fraction of the raw variation it removed, and how many periods are lost
    at the ends. "Smoother" is not the goal — separating the components is,
    and this table is how you argue which window did that.
    """
    raw_sd = float(s.std())
    rows = []
    for wnd in windows:
        r = s.rolling(wnd, center=center, min_periods=max(2, wnd // 2)).mean()
        sd = float(r.std())
        rows.append({
            "window": wnd,
            "raw_sd": round(raw_sd, 4),
            "smoothed_sd": round(sd, 4),
            "variation_removed_pct": round((1 - sd / raw_sd) * 100, 1),
            "periods_lost_each_end": wnd // 2 if center else wnd - 1,
        })
    return pd.DataFrame(rows)


def lag_at_turn(s: pd.Series, window: int, how: str = "min") -> dict:
    """
    How late a trailing mean finds a turning point. Slide 22, in numbers.

    Returns the date of the turn as a trailing window sees it, as a centred
    window sees it, and the gap in periods. The gap is not a bug — it is
    arithmetic: a trailing mean cannot know about a turn until the window
    has filled.
    """
    trailing = s.rolling(window).mean()
    centred = s.rolling(window, center=True).mean()
    pick = (lambda x: x.idxmin()) if how == "min" else (lambda x: x.idxmax())
    t, c = pick(trailing), pick(centred)
    return {
        "window": window,
        "trailing_turn": t,
        "centred_turn": c,
        "lag_periods": int((t - c) / (s.index[1] - s.index[0])),
        "half_window": window // 2,
    }


def banked_figsize(y, width: float = 9.0, x=None) -> tuple:
    """
    Cleveland's banking to 45 degrees, as a figsize. Slide 16.

    Picks the panel height that puts the median absolute segment slope at
    45 degrees, which is where slopes are compared most accurately. Returns
    `(width, height)` ready for `plt.subplots(figsize=...)`, clipped to a
    sane range so it never hands you a 0.2-inch-tall panel.

    State the number you used. Nobody reports an aspect ratio, which is
    exactly why it is such an effective way to mislead.
    """
    y = np.asarray(y, dtype=float)
    y = y[~np.isnan(y)]
    if len(y) < 3:
        return (width, width * 0.4)
    x = np.arange(len(y)) if x is None else np.asarray(x, dtype=float)
    dx = np.diff(x)
    dy = np.diff(y)
    x_range = np.ptp(x) or 1.0
    y_range = np.ptp(y) or 1.0
    # Median segment slope in data units. A segment covers dx on an axis
    # spanning x_range, so in inches it is (dx / x_range) * width across and
    # (dy / y_range) * height up. Setting those equal -- a 45-degree
    # segment -- and solving for height gives the line below.
    med = np.median(np.abs(dy / np.where(dx == 0, np.nan, dx)))
    if not np.isfinite(med) or med == 0:
        return (width, width * 0.4)
    height = width * y_range / (x_range * med)
    return (width, float(np.clip(height, width * 0.15, width * 1.2)))


# =================================================================== shares
def exclusivity_check(df: pd.DataFrame, flag_cols) -> dict:
    """
    Slide 32's first test, before a single pixel is drawn.

    `flag_cols` are boolean columns, one per category. If a unit can be
    True in two of them the parts are not exclusive, the shares will sum
    past 100%, and no pie, stacked bar or treemap of them is valid.

    Returns the share of units in each category, their sum, and how many
    units are double-counted.
    """
    flags = df[list(flag_cols)].astype(bool)
    n = len(flags)
    shares = (flags.sum() / n * 100).round(2)
    per_unit = flags.sum(axis=1)
    return {
        "n": int(n),
        "shares_pct": shares.to_dict(),
        "sum_pct": round(float(shares.sum()), 2),
        "exclusive": bool((per_unit <= 1).all()),
        "n_multi": int((per_unit >= 2).sum()),
        "pct_multi": round(float((per_unit >= 2).mean() * 100), 2),
        "n_zero": int((per_unit == 0).sum()),
    }


def rollup_other(s: pd.Series, min_share_pct: float = 1.0,
                 label: str = "Other") -> tuple:
    """
    Roll the long tail into one bucket — and hand back what it hides.

    Returns `(series, note)`. The note names how many categories went into
    the bucket and what they are worth, because slide 49's rule is that
    folding 300 small lines into one grey block is reasonable and hiding
    the count is not. Put the note on the figure.
    """
    total = float(s.sum())
    keep = s[s / total * 100 >= min_share_pct]
    tail = s[s / total * 100 < min_share_pct]
    if len(tail) == 0:
        return s.sort_values(ascending=False), f"no categories below {min_share_pct}%"
    out = pd.concat([keep.sort_values(ascending=False),
                     pd.Series({label: tail.sum()})])
    note = (f"{label} = {len(tail)} categories below {min_share_pct}% "
            f"of the total, {tail.sum():,.1f} combined "
            f"({tail.sum() / total * 100:.1f}%)")
    return out, note


# ============================================================== hierarchies
def treemap(ax, sizes, labels=None, values=None, colors=None,
            pad: float = 0.6, fontsize: int = 8, value_fmt: str = "{:,.0f}"):
    """
    A squarified treemap with the numbers printed on the blocks.

    Slide 45: area is read to about plus or minus 20%, so anything that
    matters carries its value in text. That is not decoration, it is the
    fix for using the fourth-best channel.

    Needs `squarify` (`pip install squarify`).
    """
    import squarify

    sizes = np.asarray(sizes, dtype=float)
    if (sizes < 0).any():
        raise ValueError(
            "negative values cannot be drawn as area — slide 49. Split the "
            "negatives out and show them separately.")
    order = np.argsort(sizes)[::-1]
    sizes = sizes[order]
    labels = None if labels is None else [list(labels)[i] for i in order]
    values = None if values is None else [list(values)[i] for i in order]
    if colors is None:
        base = PALETTE["series"] + [PALETTE["series_4th"], PALETTE["muted"]]
        colors = [base[i % len(base)] for i in range(len(sizes))]
    else:
        colors = [list(colors)[i] for i in order]

    norm = squarify.normalize_sizes(sizes, 100, 100)
    rects = squarify.squarify(norm, 0, 0, 100, 100)
    for r, c, i in zip(rects, colors, range(len(rects))):
        ax.add_patch(__import__("matplotlib").patches.Rectangle(
            (r["x"], r["y"]), r["dx"] - pad, r["dy"] - pad,
            facecolor=c, edgecolor=PALETTE["surface"], linewidth=0.8))
        if labels is None or r["dx"] < 9 or r["dy"] < 7:
            continue
        txt = labels[i]
        if values is not None:
            txt += "\n" + value_fmt.format(values[i])
        ax.text(r["x"] + (r["dx"] - pad) / 2, r["y"] + (r["dy"] - pad) / 2,
                txt, ha="center", va="center", fontsize=fontsize,
                color="white", linespacing=1.25)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.invert_yaxis()
    ax.axis("off")
    return ax


def _pt_per_unit(ax) -> float:
    """Typographic points per radial data unit on a polar axes, so a label
    can be measured against the room it actually has."""
    fig = ax.figure
    pos = ax.get_position()
    side_in = min(fig.get_size_inches()[0] * pos.width,
                  fig.get_size_inches()[1] * pos.height)
    r_max = ax.get_ylim()[1] or 1.0
    return (side_in / 2.0) * 72.0 / r_max


def sunburst(ax, df: pd.DataFrame, path, values: str,
             ring_width: float = 0.9, gap: float = 0.004,
             fontsize: int = 7, label_min_frac: float = 0.045):
    """
    The same tree, bent around a circle — in plain matplotlib polar bars.

    `ax` must be polar: `fig.add_subplot(projection="polar")`.
    `path` is the list of columns from the root outwards, e.g.
    `["category", "subcategory"]`, and `values` is the leaf measure.

    Slide 46: angle is share, radius is depth, and every child sits inside
    its parent's angular span. Plotly's `px.sunburst` is the one-liner and
    arrives in Week 6; this draws the same thing with no extra install.
    """
    path = list(path)
    total = float(df[values].sum())
    base = PALETTE["series"] + [PALETTE["series_4th"], PALETTE["muted"],
                                PALETTE["highlight"]]

    def _draw(sub: pd.DataFrame, level: int, theta0: float, hue: int):
        if level >= len(path):
            return
        grouped = (sub.groupby(path[level], observed=True)[values]
                     .sum().sort_values(ascending=False))
        start = theta0
        for i, (name, v) in enumerate(grouped.items()):
            span = v / total * 2 * np.pi
            colour = base[hue % len(base)] if level == 0 else base[hue % len(base)]
            ax.bar(x=start + span / 2, height=ring_width, width=max(span - gap, 0),
                   bottom=1 + level * ring_width, color=colour,
                   edgecolor=PALETTE["surface"], linewidth=0.7,
                   alpha=1.0 - 0.28 * level, align="center")
            if span / (2 * np.pi) >= label_min_frac:
                mid = start + span / 2
                r_mid = 1 + level * ring_width + ring_width / 2
                # Slide 46: outer rings get cramped. Work out how much room
                # the label really has -- radially (the ring is only so
                # thick) and along the arc -- and trim it to the smaller of
                # the two rather than let it run over its neighbour.
                budget = max(3, int(min(ring_width,
                                        span * r_mid) * _pt_per_unit(ax)
                                    / (0.55 * fontsize)))
                txt = str(name)
                if len(txt) > budget:
                    txt = txt[:max(1, budget - 1)] + "…"
                rot = np.degrees(mid)
                rot = rot - 180 if 90 < rot % 360 < 270 else rot
                ax.text(mid, r_mid, txt, ha="center", va="center",
                        rotation=rot, rotation_mode="anchor",
                        fontsize=fontsize, color="white")
            _draw(sub[sub[path[level]] == name], level + 1, start,
                  hue if level else i)
            start += span

    # set the radial limit first -- the label fitting above measures
    # against it
    ax.set_ylim(0, 1 + len(path) * ring_width)
    _draw(df, 0, 0.0, 0)
    ax.set_axis_off()
    return ax


def cycle_plot(ax, s: pd.Series, by: str = "month", color=None):
    """
    Fold a series so the cycle lines up — one line per cycle, slide 25.

    `by` is "month" (one line per year, months across) or "dayofweek"
    (one line per week). This is the Week 1 `flights.csv` chart, written
    once so you never write it again.
    """
    color = color or PALETTE["series"][0]
    if by == "month":
        outer, inner = s.index.year, s.index.month
        xlabel, n = "Month", 12
    elif by == "dayofweek":
        outer, inner = s.index.isocalendar().week, s.index.dayofweek
        xlabel, n = "Day of week", 7
    else:
        raise ValueError("by must be 'month' or 'dayofweek'")

    piv = pd.DataFrame({"outer": outer, "inner": inner, "v": s.to_numpy()})
    piv = piv.pivot_table(index="inner", columns="outer", values="v",
                          aggfunc="mean")
    cols = list(piv.columns)
    for i, c in enumerate(cols):
        shade = 0.22 + 0.78 * (i / max(len(cols) - 1, 1))
        ax.plot(piv.index, piv[c], color=color, alpha=shade, linewidth=1.8,
                marker="o", markersize=3, label=str(c))
    ax.set_xlabel(xlabel)
    ax.set_xticks(range(1, n + 1) if by == "month" else range(n))
    return ax


# ================================================================ self-check
if __name__ == "__main__":
    print(__doc__.strip().splitlines()[0])
    print("-" * 68)

    rng = np.random.default_rng(0)
    idx = pd.date_range("2025-01-01", periods=240, freq="D")
    turn = 150
    y = np.where(np.arange(240) < turn,
                 100 - 0.25 * np.arange(240),
                 100 - 0.25 * turn + 0.80 * (np.arange(240) - turn))
    s = pd.Series(y + rng.normal(0, 3.0, 240), index=idx)

    s_gappy = s.drop(s.index[[40, 41, 42]])
    a = audit_index(s_gappy, "D")
    print(f"audit_index      dtype_ok={a['dtype_ok']}  monotonic={a['monotonic']}  "
          f"dupes={a['n_duplicated']}  missing={a['n_missing']}")
    assert a["n_missing"] == 3 and a["dtype_ok"] and a["n_duplicated"] == 0

    wr = window_report(s, (7, 28, 91))
    print("window_report    " + "  ".join(
        f"w{int(r.window)}:{r.variation_removed_pct:.0f}% removed"
        for r in wr.itertuples()))
    assert wr["variation_removed_pct"].is_monotonic_increasing

    lg = lag_at_turn(s, 31, how="min")
    print(f"lag_at_turn      trailing {lg['trailing_turn'].date()}  "
          f"centred {lg['centred_turn'].date()}  lag {lg['lag_periods']} days "
          f"(half-window {lg['half_window']})")
    assert abs(lg["lag_periods"] - lg["half_window"]) <= 2

    print(f"banked_figsize   {tuple(round(v, 2) for v in banked_figsize(s.to_numpy()))}"
          f"  for a series this steep")

    flags = pd.DataFrame({
        "a": [True, True, False, False], "b": [False, True, True, False],
        "c": [False, False, True, True]})
    ex = exclusivity_check(flags, ["a", "b", "c"])
    print(f"exclusivity      sum={ex['sum_pct']}%  exclusive={ex['exclusive']}  "
          f"double-counted={ex['n_multi']}")
    assert ex["sum_pct"] == 150.0 and not ex["exclusive"]

    tail = pd.Series({"big": 600.0, "mid": 300.0, **{f"t{i}": 1.0 for i in range(100)}})
    rolled, note = rollup_other(tail, 1.0)
    print(f"rollup_other     {len(rolled)} blocks; {note}")
    assert len(rolled) == 3 and "100 categories" in note

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    style_defaults()
    fig = plt.figure(figsize=(10, 4))
    treemap(fig.add_subplot(1, 3, 1), [40, 25, 18, 10, 7],
            list("ABCDE"), values=[40, 25, 18, 10, 7])
    demo = pd.DataFrame({
        "cat": ["Mobile"] * 2 + ["Computing"] + ["Lifestyle"] * 2,
        "sub": ["Phones", "Accessories", "Laptops", "Wearables", "Footwear"],
        "rev": [24.6, 13.1, 18.4, 9.2, 11.2]})
    sunburst(fig.add_subplot(1, 3, 2, projection="polar"), demo,
             ["cat", "sub"], "rev")
    cycle_plot(fig.add_subplot(1, 3, 3),
               pd.Series(np.tile(np.arange(12), 3) + rng.normal(0, 1, 36),
                         index=pd.date_range("2023-01-01", periods=36, freq="MS")))
    fig.tight_layout()
    fig.savefig("_tslib_selfcheck.png", dpi=90)
    plt.close(fig)
    print("treemap/sunburst/cycle_plot  drew _tslib_selfcheck.png")

    print("-" * 68)
    print("all checks passed — tslib is working.")
