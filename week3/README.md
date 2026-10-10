# Week 3 — Python Visualization Foundations: Matplotlib & Seaborn

Datasets, charts and assignments for Week 3.

← [Back to the course index](../README.md)

| Lecture | Topic | Outcome | CLO | 3C |
|---|---|---|---|---|
| **L5** | Matplotlib architecture, basic plotting, figure customization | Use Python for basic static chart generation | CLO1 | Competence |
| **L6** | Statistical visualization — distributions, box plots, heatmaps | Create statistical charts for data exploration | CLO2 | Competence |

## The case

A clinical analytics group must inspect **10,000 patient vital-sign records**
before a safety review: find data-entry anomalies, check which measurements
are not normally distributed, and spot correlated risk indicators. Their
current script calls `plt.plot()` and saves whatever comes out — default
colours, overlapping tick labels, no units, 72 dpi.

You are the data analyst. By the end of the week you produce one
high-resolution multi-panel figure from a script that runs the same way every
time.

Along the way you take apart **nine charts that are wrong** — and discover
that in most of them, the reason you first reach for is not the reason.

No setup needed beyond the libraries; the data is already in `assignments/data/`.

## Contents

| Path | What it is |
|---|---|
| `assignments/TASKS.md` | Five parts, the rules and the marking guide |
| `assignments/vizlib.py` | The toolkit — palette, Lie Factor, colour-blindness simulation, `match_stats` |
| `assignments/charts/` | The nine charts to diagnose |
| `assignments/data/` | Ten datasets + `DATA_DICTIONARY.md` |
| `assignments/starter/` | Three runnable skeletons: Part D, Part C, and the Week 1 bonus |

> Model answers are **not** in this repository. `.gitignore` blocks
> `*TEACHER*`, `*_KEY*`, `*ANSWER*` and `solution/` from ever being committed
> here.

## Assignments

| Part | Covers | Marks |
|---|---|---|
| A | Diagnose the nine charts — conclusion, decoy, mechanism, redesign | 36 |
| B | Lie Factor audit computed in Python, including the one that has none | 15 |
| C | Prove a palette is colour-blind safe, with the failure shown | 9 |
| D | **Hands-on:** the 2×2 clinical review figure, exported at 300 dpi | 25 |
| E | One page of written justification, including the ethics clause | 15 |
| bonus | Week 1's preattentive experiment, rebuilt and run on five people | 5 |

Full briefs in [`assignments/TASKS.md`](assignments/TASKS.md).

## What makes this week different

Every chart in `assignments/charts/` is **arithmetically correct**. Nothing has
been fiddled. Several are drawn more carefully than most published charts. They
are still all wrong, and in most cases the obvious objection — *"correlation is
not causation", "the axis is truncated", "n is too small"* — is either
irrelevant or already ruled out by how the chart was drawn.

That is deliberate. Scepticism is cheap and generic. The marks are for naming
the mechanism and proving it from the data, which means opening the CSV and
computing something.

Three of the nine cases hand students a column that is **not on the chart**,
specifically so a plausible hypothesis can be tested and rejected.

## The datasets

| File | Rows | What it carries |
|---|---|---|
| `vitals_10k.csv` | 10,000 | The primary dataset for Part D. Messy in several unannounced ways |
| `ward_los_wide.csv` | — | The same length-of-stay data in **wide** form, so `.melt()` has something to bite on |
| `case01_helmet_rickshaw.csv` | 1,000 | Delivery-rider safety: 100,000 trips across three road types |
| `case02_chai_quizzes.csv` | 24 | Campus canteen sales and quiz failures, by month |
| `case03_aqi_monitors.csv` | 2,640 | 22 air-quality stations × 120 days. Some cells are blank |
| `case04_quartet_depts.csv` | 44 | Study hours and final scores for four departments, 11 students each |
| `case05_same_stats_shapes.csv` | 900 | Five cohorts forced to identical statistics by `vizlib.match_stats()` |
| `case06_sensor_matrix.csv` | 180 | 20 analysis variables → 190 correlation pairs |
| `case07_lie_factor.csv` | 5 | Measured ink for five published graphics |
| `case07_dual_axis_series.csv` | 6 | Monthly revenue and cost, both in PKR millions |

All data is **synthetic** and generated for CDB601220. The clinical, freight,
air-quality and campus scenarios are illustrative.

## The toolkit — `assignments/vizlib.py`

Four things students are expected to import rather than reinvent:

| Function | What it does |
|---|---|
| `style_defaults()` | Sets the house `rcParams` once, at the top of a script |
| `lie_factor(v0, v1, ink0, ink1, ink_dimension)` | Tufte's Lie Factor. The `ink_dimension` argument is the whole of two of the Part B cases |
| `simulate_cvd(colours_or_image, kind)` | Machado (2009) severity-1.0 matrices in linear RGB. Takes hex codes **or** a rendered figure |
| `delta_e` / `worst_pair` / `verdict` | Perceptual distance in OKLab, so "is this palette safe" is a number, not an opinion |
| `match_stats(x, y, …)` | Forces a dataset to exact target mean, SD and r while keeping its shape |

Run it directly (`python3 vizlib.py`) and it self-tests.

## Carry-forward from Weeks 1 and 2

Three things come back, now as code rather than as a slide:

| From | Then | Now |
|---|---|---|
| **Week 1** · preattentive attributes | Counting 3s on a slide | `starter/popout.py` — build the pop-out panels, then time five classmates and chart it |
| **Week 2** · Lie Factor | Measured with a ruler, one chart | Part B — six charts, the `ink_dimension` trap, and one chart that has no Lie Factor at all |
| **Week 2** · colour-blind-safe palettes | Asserted | Part C — simulated, measured in OKLab, and the failure shown |

## The palette

The course palette is a three-slot subset of Okabe–Ito:
`#0072B2` · `#D55E00` · `#009E73`.

It passes every check on a light surface with **all pairs** compared, not just
adjacent ones: lightness band, chroma floor, colour-vision separation
(worst ΔE 11.0 under deuteranopia), normal-vision separation (worst ΔE 18.7),
and 3:1 contrast against white.

A fourth hue (`#CC79A7`) is provided for the cases that genuinely need one. It
drops the CVD margin to ΔE 7.5 and falls below 3:1 contrast, so whenever it is
used the chart **must** carry direct labels or a table view. Part C question 3
asks students to find that themselves rather than take it on trust.

## The rules students are held to

Carried forward from Weeks 1 and 2, and applied to every submitted figure:

- **Every figure starts with `fig, ax = plt.subplots()`.** No `plt.plot()`.
- **Title the finding, not the subject.** "Readmissions by month" is a file name.
- **Declare every parameter that changes the picture** — `bins`, `bw_adjust`,
  `cut`, `vmin`, `vmax`, a log scale, a subsample size.
- **State every row removed**, with the rule and the count.
- **Never a dual-axis chart.** Two measures means two panels.
- **Save before you show.** The other way round writes a blank file.
- **A correlation has a sign**, so its heatmap gets a diverging map pinned to
  −1 … +1 with a neutral midpoint, and the upper triangle masked.
- **A script you cannot re-run is not a result.**
