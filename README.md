# Week 1 — Why Visualization & Choosing the Right Chart

Lecture notebook for Week 1 of the Data Visualization course.

## Run it

```bash
cd demo1
python3 download_data.py          # fetches the two datasets into data/
jupyter notebook week1_visualization.ipynb
```

Requires `pandas`, `numpy`, `matplotlib`, `ipykernel`.

## What's here

| Path | What it is |
|---|---|
| `download_data.py` | Downloads both datasets from public GitHub mirrors |
| `data/anscombe.csv` | Anscombe's quartet — the "why visualize" proof |
| `data/titanic.csv` | 891 real Titanic passengers — the working dataset |
| `week1_visualization.ipynb` | The lecture, with all output already executed |
| `charts/` | All 9 charts as PNGs, ready to drop into slides |

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

Charts 08 and 09 are the pair to put side by side on a slide.
