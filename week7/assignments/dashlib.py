"""
dashlib — Week 7's toolkit: the dashboard, the drill-down and the brush.

Built on Week 3's `vizlib` the same way `tslib` (Week 4) and `geolib` (Week 5)
are, so anything drawn here inherits the course palette and the export rules
by construction. Nothing in Weeks 3-6 was rewritten; this file only adds what
a *multi-panel, filterable* figure needs and a static single chart does not.

A dashboard breaks in three ways no single chart can:

1.  **The aggregate moves the other way.** A headline rate improves while
    every group inside it gets worse, because the mix shifted. The default
    view of a dashboard is always the aggregate, so this is the one error a
    reader cannot see by looking. `rate_decomposition()` splits the change
    into the part that is real and the part that is mix.

2.  **The filter double counts.** A unit that belongs to several categories
    is counted once per category, so the sum of the filtered views is larger
    than the unfiltered total. `overlap_factor()` measures it before you draw
    a control that invites the reader to add the parts up.

3.  **The drill-down does not reconcile.** A child level that does not sum to
    its parent means one of the two is wrong, and the reader will find it by
    clicking. `drilldown_check()` is Week 4's `exclusivity_check()` carried
    down a hierarchy.

Then three layout helpers (`dashboard_grid`, `kpi_tile`, `callout`), the
shared-scale rule for small multiples, and a brush that links two panels
with no browser and no install: `LinkedBrush` is plain matplotlib events,
and `select_in_rect()` is the selection logic on its own so it can be tested
without a window.

`python3 dashlib.py` self-tests. Plotly is optional everywhere — `has_plotly()`
tells you whether it is installed, and nothing here needs it.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import vizlib
from vizlib import PALETTE

__all__ = [
    "rate_decomposition", "overlap_factor", "drilldown_check",
    "channel_conflicts", "dashboard_grid", "kpi_tile", "callout",
    "shared_scale", "select_in_rect", "LinkedBrush", "has_plotly",
]


def has_plotly() -> bool:
    """True if Plotly is importable. Nothing in this toolkit requires it."""
    try:
        import plotly  # noqa: F401
        return True
    except Exception:
        return False


# --------------------------------------------------------------- 1. the mix
def rate_decomposition(before: pd.DataFrame, after: pd.DataFrame,
                       group: str, num: str, den: str,
                       per: float = 100.0) -> dict:
    """
    Why the headline rate moved: the within-group part, and the mix part.

    A rate quoted over a whole network is a weighted mean of its groups'
    rates, weighted by each group's share of the denominator. So it can move
    for two completely different reasons, and they have opposite meanings:

        within  — the groups' own rates changed          (something happened)
        mix     — the groups' shares changed             (nothing happened)

    This is the standard two-term (Kitagawa) decomposition, which is exact:
    `within + mix == rate_after - rate_before`, to floating point. The self
    test asserts it.

    Parameters
    ----------
    before, after : DataFrame
        The two periods. Each needs `group`, `num` and `den` columns; rows
        are summed per group, so daily rows are fine.
    group : str
        The column holding the thing the mix is over — mode, product, ward.
    num, den : str
        Numerator and denominator of the rate, in counts. For punctuality:
        `num="trips_on_time"`, `den="trips_operated"`. Never pass a column
        that is already a percentage: a mean of rates is not a rate.
    per : float
        Units of the reported rate. 100 (the default) gives percentage
        points; 1,000 gives a per-mille rate; 1.0 gives a fraction.

    Returns
    -------
    dict with
        rate_before, rate_after, change     the aggregate, in `per` units
        within, mix                         the two parts, summing to change
        reversal                            True if the aggregate moved one
                                            way while EVERY group moved the
                                            other — the dashboard trap
        groups                              a per-group DataFrame: rate
                                            before/after, delta, and share
                                            of the denominator before/after

    Raises
    ------
    ValueError
        If a group is present in one period and not the other. That is a
        real modelling decision — a line that opened, a depot that closed —
        and it must be made deliberately, not averaged over silently.
    """
    def _agg(df, label):
        if not {group, num, den} <= set(df.columns):
            raise ValueError(f"{label}: needs columns {group!r}, {num!r}, {den!r}")
        g = df.groupby(group, dropna=False)[[num, den]].sum()
        if (g[den] <= 0).any():
            bad = g.index[g[den] <= 0].tolist()
            raise ValueError(f"{label}: denominator is zero or negative for {bad}")
        return g

    a, b = _agg(before, "before"), _agg(after, "after")
    only_a, only_b = sorted(set(a.index) - set(b.index)), sorted(set(b.index) - set(a.index))
    if only_a or only_b:
        raise ValueError(
            "the two periods do not carry the same groups — "
            f"only in `before`: {only_a}, only in `after`: {only_b}. "
            "Decide what a group that appears or disappears means, then pass "
            "frames that say so."
        )
    a, b = a.sort_index(), b.reindex(a.index)

    r1, r2 = a[num] / a[den] * per, b[num] / b[den] * per
    w1, w2 = a[den] / a[den].sum(), b[den] / b[den].sum()

    rate_before = float(a[num].sum() / a[den].sum() * per)
    rate_after = float(b[num].sum() / b[den].sum() * per)
    within = float((((w1 + w2) / 2.0) * (r2 - r1)).sum())
    mix = float((((r1 + r2) / 2.0) * (w2 - w1)).sum())
    change = rate_after - rate_before

    delta = r2 - r1
    reversal = bool(
        abs(change) > 1e-12
        and len(delta) > 1
        and ((change > 0 and (delta < 0).all()) or (change < 0 and (delta > 0).all()))
    )

    groups = pd.DataFrame({
        "rate_before": r1, "rate_after": r2, "delta": delta,
        "share_before": w1 * 100.0, "share_after": w2 * 100.0,
        "share_delta": (w2 - w1) * 100.0,
    })
    return {"rate_before": rate_before, "rate_after": rate_after,
            "change": change, "within": within, "mix": mix,
            "reversal": reversal, "per": per, "groups": groups}


# ------------------------------------------------------------ 2. the filter
def overlap_factor(df: pd.DataFrame, unit: str, parts: str, value: str,
                   sep: str = ";") -> dict:
    """
    Does summing by category double count? Week 4's exclusivity test, for a
    dashboard filter.

    A unit that belongs to more than one category — a route through four
    districts, a patient on three drugs, a film in two genres — gets its
    whole value credited to each one. Each filtered view is then correct on
    its own, and the reader who adds them up, or who sees a "by category"
    bar chart with a total, is being lied to.

    `parts` is a column of delimited category lists ("D09;D13;D17").

    Returns
    -------
    dict with
        true_total          sum of `value` over units, each counted once
        attributed_total    sum after crediting every category it belongs to
        factor              attributed / true. 1.0 means exclusive; this is
                            the number to quote in a caption
        units, units_multi  how many units, and how many sit in >1 category
        mean_parts          mean categories per unit
        by_part             attributed value per category, descending
        exclusive           True only when factor == 1 and no unit repeats
    """
    for c in (unit, parts, value):
        if c not in df.columns:
            raise ValueError(f"no column {c!r}")
    if df[unit].duplicated().any():
        dup = df.loc[df[unit].duplicated(), unit].unique().tolist()
        raise ValueError(f"{unit!r} is not unique — repeated: {dup[:5]}")

    lists = df[parts].fillna("").astype(str).apply(
        lambda s: [p.strip() for p in s.split(sep) if p.strip()])
    n_parts = lists.apply(len)
    if (n_parts == 0).any():
        raise ValueError(f"{int((n_parts == 0).sum())} rows have no category in "
                         f"{parts!r} — missing is not a category, decide what they are")

    ex = df.assign(_part=lists).explode("_part")
    by_part = (ex.groupby("_part")[value].sum()
                 .sort_values(ascending=False).rename(value))
    true_total = float(df[value].sum())
    attributed = float(ex[value].sum())
    return {"true_total": true_total, "attributed_total": attributed,
            "factor": attributed / true_total if true_total else float("nan"),
            "units": int(len(df)), "units_multi": int((n_parts > 1).sum()),
            "max_parts": int(n_parts.max()), "mean_parts": float(n_parts.mean()),
            "by_part": by_part,
            "exclusive": bool((n_parts == 1).all())}


# --------------------------------------------------------- 3. the drill-down
def drilldown_check(df: pd.DataFrame, level: str, value: str,
                    within=(), total_label: str | None = None,
                    tol: float = 1e-6) -> dict:
    """
    Do the children sum to the parent, and is a published total hiding in
    among the parts?

    Two failures, one call:

    * **A total row filed as a part.** A published table often carries its
      own subtotal in the same column as the categories ("All tickets",
      "Total", "All ages"). Sum the column and every value is counted twice
      — the give-away is a total of exactly 200%.
    * **Children that do not reconcile.** If the parts do not add to the
      declared total, one of the two numbers is wrong, and a reader who
      drills down will find it.

    Parameters
    ----------
    level : str
        The column holding the categories (and possibly the total label).
    value : str
        The quantity being summed.
    within : sequence of str
        The columns that identify one parent — e.g. `("month", "mode")`.
        Reconciliation is checked inside each combination.
    total_label : str or None
        The label used for the declared total. If None, no total is assumed
        and only the double-count ratio is reported (it will be 100%).

    Returns
    -------
    dict with
        parts_rows, total_rows      row counts of each kind
        sum_all_pct                 summing EVERY row, as a % of the parts.
                                    200.0 means a total row per parent
        mismatches                  DataFrame of parents where
                                    |parts - declared| > tol
        worst_abs, worst_rel_pct    the largest disagreement found
        reconciles                  True when every parent reconciles
    """
    for c in (level, value, *within):
        if c not in df.columns:
            raise ValueError(f"no column {c!r}")
    within = list(within)

    is_total = (df[level].astype(str).str.strip() == total_label) if total_label else \
        pd.Series(False, index=df.index)
    parts, totals = df[~is_total], df[is_total]

    sum_parts = float(parts[value].sum())
    sum_all = float(df[value].sum())
    out = {"parts_rows": int(len(parts)), "total_rows": int(len(totals)),
           "sum_parts": sum_parts, "sum_all": sum_all,
           "sum_all_pct": (sum_all / sum_parts * 100.0) if sum_parts else float("nan")}

    if total_label is None or not len(totals):
        out.update(mismatches=pd.DataFrame(), worst_abs=0.0,
                   worst_rel_pct=0.0, reconciles=True)
        return out

    key = within or [level]
    p = parts.groupby(within, dropna=False)[value].sum() if within else \
        pd.Series({"_all": sum_parts})
    t = totals.groupby(within, dropna=False)[value].sum() if within else \
        pd.Series({"_all": float(totals[value].sum())})
    comp = pd.DataFrame({"parts": p, "declared": t})
    if comp.isna().any().any():
        missing = comp[comp.isna().any(axis=1)]
        comp = comp.fillna(0.0)
    comp["diff"] = comp.parts - comp.declared
    comp["rel_pct"] = np.where(comp.declared != 0,
                               comp["diff"] / comp.declared * 100.0, np.nan)
    bad = comp[comp["diff"].abs() > tol].sort_values("diff", key=abs, ascending=False)
    out.update(mismatches=bad,
               worst_abs=float(comp["diff"].abs().max()),
               worst_rel_pct=float(np.nanmax(np.abs(comp.rel_pct))) if len(comp) else 0.0,
               reconciles=bool(len(bad) == 0))
    return out


# ------------------------------------------------------ 4. the encoding plan
_CHANNELS = ("x", "y", "hue", "size", "shape", "lightness", "facet",
             "row", "column", "angle", "width")

# The channels a reader carries from one panel to the next. Position is read
# against its own axis and is panel-local, so a different x per panel is
# normal; hue, size, shape and lightness are learned once from the legend and
# then applied to the whole screen, which is why only these can conflict.
_IDENTITY_CHANNELS = ("hue", "size", "shape", "lightness", "angle", "width")


def channel_conflicts(panels) -> dict:
    """
    One dashboard, one meaning per channel. Week 2's channel ranking, applied
    across panels instead of inside one chart.

    On a single chart, hue means one thing. On a screen of six, hue very
    often means `mode` top-left, `district` middle and `status` bottom-right
    — and the reader, who learned the legend once, reads all three with the
    first one. That is a dashboard-only failure and it is pure bookkeeping to
    catch, so catch it before you draw.

    Pass one dict per panel: a `panel` name plus any of
    x, y, hue, size, shape, lightness, facet, row, column, angle, width.

        channel_conflicts([
            {"panel": "trend", "x": "date", "y": "boardings", "hue": "mode"},
            {"panel": "map",   "lightness": "legs_per_1000", "hue": "mode"},
        ])

    Only the channels a reader carries between panels can conflict — hue,
    size, shape, lightness, angle, width. `x` and `y` are read against their
    own axis, so a different x in every panel is normal and is reported under
    `positional` rather than flagged.

    Returns
    -------
    dict with
        conflicts       {channel: [variables]} for an identity channel
                        carrying more than one variable — fix these
        redundant       {variable: [channels]} for variables on more than
                        one channel. Not an error: Week 2's redundant coding
                        is deliberate, and this is here so you can say it was
        positional      {x|y: [variables]} for information, never flagged
        channels_used   {channel: [variables]} in full
        ok              True when `conflicts` is empty
    """
    seen: dict[str, list] = {}
    for i, p in enumerate(panels):
        name = p.get("panel", f"panel {i + 1}")
        unknown = set(p) - {"panel"} - set(_CHANNELS)
        if unknown:
            raise ValueError(f"{name}: unknown channel(s) {sorted(unknown)}; "
                             f"known channels are {list(_CHANNELS)}")
        for ch, var in p.items():
            if ch == "panel" or var is None:
                continue
            seen.setdefault(ch, [])
            if var not in seen[ch]:
                seen[ch].append(var)

    var_to_ch: dict[str, list] = {}
    for ch, vs in seen.items():
        for v in vs:
            var_to_ch.setdefault(v, []).append(ch)

    conflicts = {ch: vs for ch, vs in seen.items()
                 if ch in _IDENTITY_CHANNELS and len(vs) > 1}
    return {"conflicts": conflicts,
            "redundant": {v: chs for v, chs in var_to_ch.items() if len(chs) > 1},
            "positional": {ch: vs for ch, vs in seen.items() if ch in ("x", "y")},
            "channels_used": seen,
            "ok": not conflicts}


# ----------------------------------------------------------- 5. the furniture
def dashboard_grid(fig, mosaic, headline: str | None = None,
                   standfirst: str | None = None, order=None,
                   height_ratios=None, width_ratios=None,
                   hspace: float = 0.55, wspace: float = 0.30,
                   top: float = 0.88):
    """
    A named grid with a headline band, so the layout is a decision you can
    point at in your note.

    `mosaic` is a matplotlib mosaic — a list of rows of panel names, or the
    string form. Repeat a name to make a panel span cells; `"."` leaves a
    cell empty.

        axd = dashboard_grid(fig, [["kpi1", "kpi2", "kpi3"],
                                   ["trend", "trend", "map"],
                                   ["mix",   "mix",   "map"]],
                             headline="Bus punctuality fell in every zone",
                             standfirst="...")

    `headline` is the finding, in the title position, where Week 1 says it
    belongs — a dashboard needs one for the screen as a whole, not only one
    per panel. `standfirst` is the line under it: the period, the unit and
    the denominator.

    Pass `order=["kpi1", "trend", "map"]` to stamp the intended reading order
    in the corner of those panels while you are designing. Take it off for
    the submitted figure unless the order is genuinely part of the message.

    Returns the dict of axes keyed by panel name.
    """
    gs_kw: dict = {"hspace": hspace, "wspace": wspace}
    if height_ratios is not None:
        gs_kw["height_ratios"] = height_ratios
    if width_ratios is not None:
        gs_kw["width_ratios"] = width_ratios
    axd = fig.subplot_mosaic(mosaic, gridspec_kw=gs_kw, empty_sentinel=".")

    if headline:
        fig.text(0.01, 0.985, headline, ha="left", va="top",
                 fontsize=15, fontweight="bold", color=PALETTE["ink"])
    if standfirst:
        fig.text(0.01, 0.935, standfirst, ha="left", va="top",
                 fontsize=9.5, color=PALETTE["ink_soft"])
    if headline or standfirst:
        fig.subplots_adjust(top=top)

    if order:
        for i, name in enumerate(order, start=1):
            if name not in axd:
                raise ValueError(f"order names {name!r}, which is not in the mosaic")
            axd[name].text(0.0, 1.0, str(i), transform=axd[name].transAxes,
                           ha="center", va="center", fontsize=8,
                           fontweight="bold", color=PALETTE["surface"],
                           bbox=dict(boxstyle="circle,pad=0.32",
                                     facecolor=PALETTE["ink_soft"], edgecolor="none"))
    return axd


def kpi_tile(ax, label: str, value, delta=None, note: str | None = None,
             good: str = "up", fmt: str = "{:,.0f}", delta_fmt: str = "{:+.2f}",
             series=None) -> None:
    """
    One number, said once. The form for a single headline value — a tile, not
    a one-bar bar chart.

    `delta` is the change against whatever comparison you name in `note`; it
    is drawn with an arrow and a sign as well as a colour, so it is never
    colour alone. `good` says which direction is good ("up", "down", or
    "neutral" for a number with no better or worse) — the tile does not
    assume that up is good, because for delay minutes it is not.

    `series` draws a context sparkline in the bottom of the tile, unlabelled
    and in the muted grey: it carries shape only. If a reader needs to read
    values off it, it wants to be a chart.
    """
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.0, 0.97, label.upper(), ha="left", va="top", fontsize=8.5,
            color=PALETTE["ink_soft"])
    shown = fmt.format(value) if not isinstance(value, str) else value
    ax.text(0.0, 0.76, shown, ha="left", va="top", fontsize=25,
            fontweight="bold", color=PALETTE["ink"])

    if delta is not None:
        if good == "neutral" or delta == 0:
            colour, arrow = PALETTE["ink_soft"], "→"
        else:
            improving = (delta > 0) if good == "up" else (delta < 0)
            colour = PALETTE["series"][2] if improving else PALETTE["highlight"]
            arrow = "▲" if delta > 0 else "▼"
        txt = delta if isinstance(delta, str) else delta_fmt.format(delta)
        ax.text(0.0, 0.40, f"{arrow} {txt}", ha="left", va="top",
                fontsize=11, fontweight="bold", color=colour)

    if note:
        ax.text(0.0, 0.24, note, ha="left", va="top", fontsize=8,
                color=PALETTE["ink_soft"], wrap=True)

    if series is not None:
        s = np.asarray(pd.Series(series).dropna(), dtype=float)
        if s.size > 1:
            x = np.linspace(0.0, 1.0, s.size)
            lo, hi = float(s.min()), float(s.max())
            y = 0.04 + 0.10 * ((s - lo) / (hi - lo) if hi > lo else np.zeros_like(s))
            ax.plot(x, y, lw=1.2, color=PALETTE["muted"], solid_capstyle="round")


def callout(ax, xy, text, xytext=None, color=None, fontsize: int = 9,
            ha: str = "left", va: str = "center"):
    """
    An annotation with a leader line, a surface halo and no box — the mark
    that turns a chart into a sentence.

    `xy` is the point in data coordinates. `xytext` is where the text sits,
    also in data coordinates; left out, the text is offset in points instead,
    so a date or categorical axis needs no arithmetic. The halo is a
    stroke in the surface colour so the text survives landing on a line or a
    filled area. Use it for the one point the reader must not miss, and stop:
    Week 1's rule against labelling every point holds here too.
    """
    import matplotlib.patheffects as pe
    color = color or PALETTE["ink"]
    place = ({"xytext": (20, 24), "textcoords": "offset points"}
             if xytext is None else {"xytext": xytext})

    ann = ax.annotate(
        text, xy=xy, ha=ha, va=va, fontsize=fontsize,
        color=color, zorder=6, **place,
        arrowprops=dict(arrowstyle="-", color=PALETTE["ink_soft"],
                        lw=0.9, shrinkA=2, shrinkB=4,
                        connectionstyle="arc3,rad=0.0"))
    ann.set_path_effects([pe.withStroke(linewidth=3, foreground=PALETTE["surface"])])
    ax.plot([xy[0]], [xy[1]], marker="o", ms=5, mfc=color, mec=PALETTE["surface"],
            mew=1.2, zorder=7, linestyle="none")
    return ann


def shared_scale(axes, which: str = "y", from_zero: bool = False,
                 pad: float = 0.05) -> tuple:
    """
    Put every small multiple on one scale, and hand back the sentence that
    says so.

    Panels on free scales are the commonest way a grid of small multiples
    lies: six panels that look alike while one is thirty times the others.
    Call this on the panels, then put the returned note in the caption.

    Returns `(lo, hi, note)` and sets the limits on every axis.
    """
    axes = list(axes.values()) if isinstance(axes, dict) else list(axes)
    lo, hi = np.inf, -np.inf
    for ax in axes:
        a, b = (ax.get_ylim() if which == "y" else ax.get_xlim())
        lo, hi = min(lo, a), max(hi, b)
    if from_zero:
        lo = min(lo, 0.0)
    span = (hi - lo) or 1.0
    hi = hi + pad * span
    if not from_zero:
        lo = lo - pad * span
    for ax in axes:
        (ax.set_ylim if which == "y" else ax.set_xlim)(lo, hi)
    note = (f"all {len(axes)} panels share one {which}-axis, "
            f"{lo:,.0f} to {hi:,.0f}" + (" (from zero)" if from_zero else ""))
    return lo, hi, note


# ----------------------------------------------------------- 6. the brushing
def select_in_rect(df: pd.DataFrame, x: str, y: str, rect) -> pd.Series:
    """
    The selection logic of a brush, on its own so it can be tested without a
    window. `rect` is `(x0, y0, x1, y1)` in data coordinates, in any corner
    order. Returns a boolean Series, inclusive of the edges.
    """
    x0, y0, x1, y1 = rect
    xlo, xhi = sorted((x0, x1))
    ylo, yhi = sorted((y0, y1))
    return (df[x].between(xlo, xhi)) & (df[y].between(ylo, yhi))


class LinkedBrush:
    """
    Drag a rectangle on one panel, highlight the same rows on another. Plain
    matplotlib events — no browser, no install, and it works in a notebook
    with `%matplotlib widget` or in any interactive window.

        brush = dashlib.LinkedBrush(ax_scatter, routes, "crowding_index",
                                    "punctuality_pct", on_select=repaint)

    `on_select` is called with the boolean mask every time the drag ends.
    Keep it cheap: it runs on every release.

    `simulate(rect)` runs the same path with no event loop, which is how you
    test a brush — and how the self-test below checks this one.
    """

    def __init__(self, ax, df: pd.DataFrame, x: str, y: str, on_select,
                 color: str | None = None):
        self.ax, self.df, self.x, self.y = ax, df, x, y
        self.on_select = on_select
        self.mask = pd.Series(True, index=df.index)
        self.selector = None
        try:
            from matplotlib.widgets import RectangleSelector
            self.selector = RectangleSelector(
                ax, self._on_release, useblit=False, button=[1],
                interactive=True, minspanx=0, minspany=0,
                props=dict(facecolor=color or PALETTE["series"][0], alpha=0.12,
                           edgecolor=color or PALETTE["series"][0], lw=1.0, fill=True))
        except Exception as exc:          # headless backend, old matplotlib
            self._why = exc

    def _on_release(self, click, release):
        if None in (click.xdata, click.ydata, release.xdata, release.ydata):
            return
        self.simulate((click.xdata, click.ydata, release.xdata, release.ydata))

    def simulate(self, rect) -> pd.Series:
        """Apply a selection as if it had been dragged. Returns the mask."""
        self.mask = select_in_rect(self.df, self.x, self.y, rect)
        self.on_select(self.mask)
        return self.mask

    def clear(self) -> pd.Series:
        """Select everything again — the 'reset' a filter must always have."""
        self.mask = pd.Series(True, index=self.df.index)
        self.on_select(self.mask)
        return self.mask


# ------------------------------------------------------------------ self-test
if __name__ == "__main__":
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    vizlib.style_defaults()
    print("dashlib self-test\n" + "-" * 68)
    print(f"plotly installed: {has_plotly()}  (optional — nothing here needs it)")

    # ---- 1. the mix. Two made-up periods, NOT the Week 7 data.
    before = pd.DataFrame({"mode": ["A", "B"], "on_time": [960, 740], "run": [1000, 1000]})
    after = pd.DataFrame({"mode": ["A", "B"], "on_time": [2820, 1450], "run": [3000, 2000]})
    dec = rate_decomposition(before, after, "mode", "on_time", "run")
    print(f"\nrate_decomposition()  {dec['rate_before']:.2f}% -> {dec['rate_after']:.2f}% "
          f"({dec['change']:+.2f} pts)")
    print(f"  within {dec['within']:+.2f} pts, mix {dec['mix']:+.2f} pts, "
          f"reversal={dec['reversal']}")
    print(dec["groups"].round(2).to_string())
    assert abs(dec["within"] + dec["mix"] - dec["change"]) < 1e-9, "decomposition must be exact"
    assert dec["reversal"], "both groups fell while the total rose — that is the case here"
    assert (dec["groups"].delta < 0).all()
    try:
        rate_decomposition(before, after.assign(mode=["A", "C"]), "mode", "on_time", "run")
    except ValueError as e:
        print(f"  a changed group list is refused: {str(e)[:58]}...")
    else:
        raise AssertionError("should have refused a changed group list")

    # ---- 2. the filter
    units = pd.DataFrame({"route": ["R1", "R2", "R3"],
                          "serves": ["X;Y", "Y", "X;Y;Z"],
                          "trips": [100.0, 50.0, 30.0]})
    ov = overlap_factor(units, "route", "serves", "trips")
    print(f"\noverlap_factor()  true {ov['true_total']:,.0f} vs attributed "
          f"{ov['attributed_total']:,.0f}  = {ov['factor']:.3f}x  "
          f"({ov['units_multi']} of {ov['units']} units in >1 category)")
    assert ov["true_total"] == 180 and ov["attributed_total"] == 340
    assert not ov["exclusive"]
    assert abs(ov["factor"] - 340 / 180) < 1e-12
    assert ov["by_part"]["Y"] == 180
    assert overlap_factor(units.assign(serves=["X", "Y", "Z"]),
                          "route", "serves", "trips")["exclusive"]

    # ---- 3. the drill-down
    hier = pd.DataFrame({
        "month": ["M1"] * 4 + ["M2"] * 4,
        "kind": ["p", "q", "r", "TOTAL"] * 2,
        "v": [3.0, 4.0, 5.0, 12.0, 2.0, 2.0, 2.0, 7.0]})
    dd = drilldown_check(hier, "kind", "v", within=("month",), total_label="TOTAL")
    print(f"\ndrilldown_check()  {dd['parts_rows']} part rows, {dd['total_rows']} total rows; "
          f"summing every row gives {dd['sum_all_pct']:.1f}% of the parts")
    print(f"  reconciles={dd['reconciles']}, worst disagreement {dd['worst_abs']:.0f}")
    print(dd["mismatches"].round(2).to_string())
    assert dd["parts_rows"] == 6 and dd["total_rows"] == 2
    assert not dd["reconciles"] and list(dd["mismatches"].index) == ["M2"]
    assert dd["sum_all_pct"] > 200.0, "M2's declared total is larger than its parts"
    # the same file with M2 repaired: one total row per parent, and now the
    # double count is exactly 200% — which is the give-away to look for
    fixed = hier.copy()
    fixed.loc[(fixed.month == "M2") & (fixed.kind == "TOTAL"), "v"] = 6.0
    ddf = drilldown_check(fixed, "kind", "v", within=("month",), total_label="TOTAL")
    assert ddf["reconciles"] and abs(ddf["sum_all_pct"] - 200.0) < 1e-9
    print(f"  with the parts repaired: reconciles={ddf['reconciles']}, "
          f"summing every row gives exactly {ddf['sum_all_pct']:.1f}%")
    clean = hier[hier.kind != "TOTAL"]
    assert drilldown_check(clean, "kind", "v", within=("month",))["sum_all_pct"] == 100.0

    # ---- 4. the encoding plan
    cc = channel_conflicts([
        {"panel": "trend", "x": "date", "y": "boardings", "hue": "mode"},
        {"panel": "bars", "x": "legs", "y": "district", "hue": "mode"},
        {"panel": "map", "lightness": "legs_per_1000", "hue": "district"},
    ])
    print(f"\nchannel_conflicts()  ok={cc['ok']}  conflicts={cc['conflicts']}")
    print(f"  positional channels, reported not flagged: {cc['positional']}")
    assert not cc["ok"] and cc["conflicts"] == {"hue": ["mode", "district"]}
    # a different x per panel is normal, and redundant coding is deliberate
    ok = channel_conflicts([{"panel": "a", "x": "date", "hue": "mode"},
                            {"panel": "b", "x": "legs", "hue": "mode",
                             "shape": "mode"}])
    assert ok["ok"] and ok["redundant"] == {"mode": ["hue", "shape"]}

    # ---- 5 and 6. the furniture and the brush, drawn once
    rng = np.random.default_rng(7)
    pts = pd.DataFrame({"load": rng.uniform(0.4, 1.4, 60),
                        "ontime": rng.uniform(60, 98, 60)})
    days = pd.date_range("2026-01-01", periods=90, freq="D")
    wave = pd.DataFrame({"d": days, "v": 100 + np.arange(90) * 0.6
                         + rng.normal(0, 4, 90)})

    fig = plt.figure(figsize=(11, 6.6))
    axd = dashboard_grid(
        fig, [["kpi", "trend", "trend"], ["scatter", "sm1", "sm2"]],
        headline="dashlib self-test — the furniture, drawn once",
        standfirst="Made-up numbers. Nothing here is the Week 7 data.",
        height_ratios=[1.0, 1.25])
    kpi_tile(axd["kpi"], "on-time, network", 80.60, delta=1.73,
             note="vs the same quarter last year", fmt="{:.2f}%",
             series=wave.v)
    axd["trend"].plot(wave.d, wave.v, color=PALETTE["series"][0])
    axd["trend"].set_title("A series, with one point called out")
    early = wave.iloc[:55]
    peak = early.loc[early.v.idxmax()]
    callout(axd["trend"], (peak.d, peak.v), "the one point\nworth naming")
    axd["scatter"].scatter(pts.load, pts.ontime, s=26,
                           color=PALETTE["muted"], edgecolor=PALETTE["surface"], lw=0.6)
    axd["scatter"].set_title("Brush me")
    axd["scatter"].set_xlabel("load index")
    axd["scatter"].set_ylabel("on-time %")

    picked = {"n": None, "artist": None}

    def repaint(mask):
        # the gotcha in any linked view: take the old highlight off before
        # you draw the new one, or every selection is still on the screen
        if picked["artist"] is not None:
            picked["artist"].remove()
        picked["n"] = int(mask.sum())
        picked["artist"] = axd["scatter"].scatter(
            pts.load[mask], pts.ontime[mask], s=30, color=PALETTE["highlight"],
            edgecolor=PALETTE["surface"], lw=0.6, zorder=5)

    brush = LinkedBrush(axd["scatter"], pts, "load", "ontime", on_select=repaint)
    mask = brush.simulate((0.8, 80, 1.4, 98))
    expect = int(((pts.load >= 0.8) & (pts.ontime >= 80)).sum())
    assert picked["n"] == expect == int(mask.sum()), (picked["n"], expect)
    assert int(brush.clear().sum()) == len(pts) and picked["n"] == len(pts)
    brush.simulate((0.8, 80, 1.4, 98))          # leave the figure selected
    print(f"\nLinkedBrush.simulate()  selected {expect} of {len(pts)} points, "
          f"reset to {len(pts)}, selected again")

    # two small multiples in the SAME unit — the only case a shared scale is
    # meaningful. One is a third of the other, which free scales would hide.
    for name, scale, title in [("sm1", 1.0, "Zone A"), ("sm2", 0.32, "Zone B")]:
        axd[name].plot(wave.d, wave.v * scale, color=PALETTE["series"][0])
        axd[name].set_title(f"{title} — boardings/day", fontsize=10)
        axd[name].tick_params(axis="x", labelrotation=30, labelsize=7)
    lo, hi, note = shared_scale([axd["sm1"], axd["sm2"]], "y", from_zero=True)
    print(f"shared_scale()  {note}")
    assert lo == 0.0 and hi > 0.0

    out = vizlib.save_fig(fig, "_dashlib_selfcheck.png",
                          note="dashlib self-test — synthetic numbers, not the Week 7 data")
    plt.close(fig)
    print(f"\nwrote {out} at 300 dpi")
    print("-" * 68 + "\nall dashlib checks passed")
