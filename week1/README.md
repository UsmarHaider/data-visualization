# Week 1 — Why Visualization & Choosing the Right Chart

Lecture notebook, datasets, exported charts and assignments for Week 1.

← [Back to the course index](../README.md)

## Run the lecture

```bash
cd week1
python3 download_data.py                      # fetches the two datasets into data/
jupyter notebook week1_visualization.ipynb
```

Requires `pandas`, `numpy`, `matplotlib`, `jupyter`, `ipykernel`.

The notebook is committed with its outputs already executed, so you can also just read it on GitHub.

## Contents

| Path | What it is |
|---|---|
| `week1_visualization.ipynb` | The lecture — 43 cells, fully executed |
| `download_data.py` | Downloads the two lecture datasets from public mirrors |
| `data/anscombe.csv` | Anscombe's quartet (44 rows) — the "why visualize" proof |
| `data/titanic.csv` | 891 real Titanic passengers — the working dataset |
| `charts/` | All nine charts as PNGs, ready for slides |
| `assignments/` | Five datasets and five student tasks — see [`assignments/TASKS.md`](assignments/TASKS.md) |

## Lecture structure

| Part | Topic |
|---|---|
| 1 | **Why visualize** — Anscombe's quartet: identical statistics, four different realities |
| 2 | Meet the data — shape, types, missing values |
| 3 | Processing — cleaning, labelling, deriving columns, aggregating to small tidy tables |
| 4 | **Choosing the right chart** — bar, line, histogram, scatter, stacked bar vs pie, grouped bar |
| 5 | **One chart, one message** — a deliberately broken chart, then the fix |
| 6 | Takeaways, craft rules, and four exercises for next week |

## Charts

| File | Teaches |
|---|---|
| `01_why_visualize_anscombe.png` | Why summary statistics are not enough |
| `02_bar_class.png` | Comparison → bar; title the finding; zero baseline |
| `03_line_age.png` | Trend → line; an ordered axis need not be time |
| `04_histogram_age.png` | Distribution → histogram; bar ≠ histogram |
| `05_scatter_age_fare.png` | Relationship → scatter; "no relationship" is an answer |
| `06_pie_vs_stacked_bar.png` | Composition → why the bar beats the pie |
| `07_grouped_bar_class_sex.png` | Two categories at once — and why that's the ceiling |
| `08_messy_bad_example.png` | **Anti-example.** 29 bars, rainbow, dual axis, no message |
| `09_clear_one_message.png` | The fix: one question, grey for context, colour for the message |

Charts `08` and `09` are the pair to put side by side on a slide.

## Assignments

```bash
cd assignments
python3 download_assignment_data.py
```

| Task | Dataset | Practises |
|---|---|---|
| 1 | `datasaurus.csv` | Why visualize — 13 datasets, near-identical statistics |
| 2 | `gapminder.csv` | Trends, and fixing a spaghetti chart two ways |
| 3 | `penguins.csv` | Distributions, relationships, and a real Simpson's paradox |
| 4 | `mpg.csv` | Choosing a different chart for each of five questions |
| 5 | `flights.csv` | Separating a trend from a seasonal cycle |

Full briefs and the marking guide are in [`assignments/TASKS.md`](assignments/TASKS.md).
