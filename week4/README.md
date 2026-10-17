# Week 4 — Time-Series, Proportions & Hierarchies

Datasets, toolkit and assignments for Week 4.

← [Back to the course index](../README.md)

| Lecture | Topic | Outcome | CLO | 3C |
|---|---|---|---|---|
| **L7** | Time series — resolution, gaps, baselines, rolling means, decomposition | Design time-series visualizations that expose trend, seasonality and cycles | CLO2 | Competence |
| **L8** | Proportions and hierarchies — pie vs bar, stacked forms, treemaps, sunbursts | Compare part-to-whole strategies and construct hierarchical visualizations | CLO2 | Competence |

## The case

An e-commerce platform tracks **hourly web traffic** and a **sales
breakdown across dozens of product sub-categories**. Leadership reviews one
dashboard every Monday morning.

Sub-category share is shown as a multi-slice 3-D pie, so fine comparison is
impossible. Daily traffic is plotted raw, so the weekend rhythm drowns the
trend — and the board keeps missing the seasonal turn.

You are the data visualizer. By the end of the week you produce one
high-resolution four-panel figure from a script that runs the same way
every time: the traffic smoothed so the real trajectory is what leadership
sees, the weekly rhythm shown as a rhythm rather than as noise, and the
catalogue broken down as a treemap with the honest bar chart beside it.

Along the way you take apart **nine more charts that are wrong** — and this
time none of them is broken by a drawing decision.

No setup needed beyond the libraries; the data is already in
`assignments/data/`.

## Contents

| Path | What it is |
|---|---|
| `assignments/TASKS.md` | Five parts, a bonus, the rules and the marking guide |
| `assignments/vizlib.py` | **Week 3's toolkit, unchanged** — palette, Lie Factor, CVD simulation, `save_fig` |
| `assignments/tslib.py` | This week's toolkit, built on top of `vizlib` |
| `assignments/data/` | Twelve datasets + `DATA_DICTIONARY.md` |

> There are **no starter skeletons** this week, by design. Week 3 shipped
> three; from Week 4 students write the script themselves, with `tslib.py`
> as the only scaffolding.
>
> Model answers are **not** in this repository. `.gitignore` blocks
> `*TEACHER*`, `*_KEY*`, `*ANSWER*` and `solution/` from ever being
> committed here.

## Assignments

| Part | Covers | Marks |
|---|---|---|
| A | Rebuild nine charts, then diagnose — conclusion, decoy, mechanism, redesign | 36 |
| B | Smoothing, windows and panel shape, computed rather than eyeballed | 15 |
| C | Part-to-whole legality, and the pie-ranking experiment on a real reader | 9 |
| D | **Hands-on:** the 2×2 e-commerce review figure, exported at 300 dpi | 25 |
| E | One page of written justification, including the window clause | 15 |
| F | *Bonus, marked separately* — Week 1's `flights.csv` task, on data you find | 5 |

Full briefs in [`assignments/TASKS.md`](assignments/TASKS.md).

## What makes this week different

Week 3's nine broken charts were broken by a **drawing** decision — a bin
width, a truncated axis, a rainbow colormap. You could find them by looking
at the figure.

Week 4's nine are broken **before any drawing happens**: by a parse, a
resample, a rolling window, a denominator. Every one of them is a chart you
could stare at all afternoon without seeing the problem, because the
problem is upstream of the pixels. The only way in is to open the file and
compute something.

The nine mechanisms, one per deck idea:

| # | Mechanism | Slide |
|---|---|---|
| 1 | A date column sorted as text | 10 |
| 2 | Plotting by row number, so unrecorded days vanish | 13 |
| 3 | A **level** resampled with `sum()` | 12 |
| 4 | A trailing mean's turning point arriving half a window late | 22 |
| 5 | A window that starts at the seasonal peak | 28 |
| 6 | An incomplete final period | 18 |
| 7 | Volatility leaking upward through a stacked area's moving baseline | 26 |
| 8 | Parts that are not exclusive, so the shares sum past 100% | 32 |
| 9 | A rising share of a falling total | 38 |

Each case carries a **self-check number** so a student knows their rebuild
is faithful before they start diagnosing it.

Two cases are deliberately *incomplete* rather than wrong: the redesign is
not a different chart type, it is the same chart with something else beside
it. That distinction is the point of Lecture 8.

## Carried forward

Nothing from Weeks 1–3 is retired, and `TASKS.md` opens with the table that
maps each idea to where it returns. The three load-bearing ones:

- **Week 1's `flights.csv` question** — *is the seasonality growing, or is
  the business?* — was left open with "suggest a chart that would settle
  it". Part F makes students settle it, on data they source themselves.
- **Week 2's channel ranking** (position > length > angle > area) is now
  doing triple duty: it is why bars beat pies in Part C, and why a treemap
  needs its values printed on it in Part D.
- **Week 3's `vizlib.py` is imported unchanged**, not reimplemented.
  `tslib` builds on it, so a Week 4 figure inherits the Week 3 palette and
  export rules by construction.

## The datasets

| File | Rows | What it carries |
|---|---|---|
| `sessions_hourly.csv` | 12,670 | The primary dataset for Part D. Six unannounced faults |
| `revenue_catalogue.csv` | 345 | Four categories → eight sub-categories → SKUs, with returns |
| `shares_eight.csv` | 8 | The eight slices of the Part C ranking experiment |
| `case01_orders_stringdate.csv` | 24 | Monthly orders, dates written `YYYY-M` |
| `case02_shop_closed.csv` | 69 | Daily sales — trading days only, across a 90-day span |
| `case03_bandwidth_levels.csv` | 1,237 | Hourly concurrent users (a level) and bytes served (a flow) |
| `case04_intervention_lag.csv` | 214 | Daily conversion with one real turning point |
| `case05_revenue_window.csv` | 36 | 36 complete months, strongly seasonal |
| `case06_monthly_partial.csv` | 284 | Daily orders, extracted part-way through October |
| `case07_stacked_products.csv` | 36 | Four product lines × 36 months |
| `case08_channel_attrib.csv` | 4,000 | One row per customer, four non-exclusive touch flags |
| `case09_premium_share.csv` | 8 | Quarterly total and premium revenue |

`sessions_hourly.csv` and `revenue_catalogue.csv` describe the **same
business over the same window**, and the sub-category shares in
`shares_eight.csv` are the catalogue's own — so Part C's pie and Part D's
treemap are one whole at two grains. That is the self-check at the end of
Part D.

All data is synthetic, generated from a fixed seed for CDB601220.

## Requirements

```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels squarify
cd week4/assignments
python3 tslib.py          # self-check that the toolkit runs
```

`statsmodels` (for `seasonal_decompose`) and `squarify` (for the treemap
layout) are new this week. Plotly is **optional** — `px.treemap`,
`px.sunburst` and `px.icicle` are previewed here and arrive properly in
Week 6, when they become interactive. Everything in this week is markable
in matplotlib, and `tslib` ships `treemap()`, `sunburst()` and
`cycle_plot()` so nobody is blocked on an install.
