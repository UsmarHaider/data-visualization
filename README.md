# Data Visualization

Course repository — lecture notebooks, datasets and assignments.

Every lecture is a single Jupyter notebook that runs top to bottom on real, downloaded data. Notebooks are
committed **with their outputs**, so you can read the whole lecture on GitHub without running anything.

---

## Contents

| Week | Topic | Material |
|---|---|---|
| **1** | Why visualization, and choosing the right chart | [`week1/`](week1/) |

More weeks will be added here as the course runs.

---

## Quick start

```bash
git clone https://github.com/UsmarHaider/data-visualization.git
cd data-visualization

# Lecture
cd week1
python3 download_data.py
jupyter notebook week1_visualization.ipynb

# Assignments
cd assignments
python3 download_assignment_data.py
```

**Requirements:** Python 3.9+, and:

```bash
pip install pandas numpy matplotlib jupyter ipykernel
```

> No data files are committed that you cannot re-download. Each folder has a `download_*.py` script that
> fetches its datasets from public sources, so the repository stays reproducible.

---

## Week 1 — Why visualization, and choosing the right chart

### The lecture — [`week1/week1_visualization.ipynb`](week1/week1_visualization.ipynb)

| Part | Topic | What it covers |
|---|---|---|
| 1 | **Why visualize?** | Anscombe's quartet — four datasets with identical mean, standard deviation, correlation (0.816) and regression line, which look nothing alike when plotted |
| 2 | Meet the data | Shape, data types, and a missing-value audit of the Titanic passenger list |
| 3 | Processing | Cleaning, readable labels, derived columns, and aggregating down to small tidy tables |
| 4 | **Choosing the right chart** | One section per question type — the question chooses the chart, not your taste |
| 5 | **One chart, one message** | A deliberately broken chart, dissected, then rebuilt |
| 6 | Takeaways | The craft rules, plus four exercises |

### Datasets used in the lecture

| File | Rows | Why it's there |
|---|---|---|
| `week1/data/anscombe.csv` | 44 | Anscombe's quartet (1973) — the proof that statistics alone are not enough |
| `week1/data/titanic.csv` | 891 | Real Titanic passengers — categories, numbers, groups and genuine missing values |

### The chart-choice reference from Part 4

| Your question | The data's job | Use |
|---|---|---|
| Which category is biggest? | comparison | **Bar chart** |
| How does it change across an ordered scale? | trend | **Line chart** |
| How is one variable spread out? | distribution | **Histogram** |
| Do two numbers move together? | relationship | **Scatter plot** |
| How does a whole split up? | composition | **Stacked bar** (rarely a pie) |
| Two categories at once? | two-way comparison | **Grouped bar** — but this is the ceiling |

### Charts — [`week1/charts/`](week1/charts/)

All nine are exported as PNGs, ready to drop into slides.

| File | What it teaches |
|---|---|
| `01_why_visualize_anscombe.png` | Why summary statistics are not enough |
| `02_bar_class.png` | Comparison → bar; title the finding; zero baseline |
| `03_line_age.png` | Trend → line; an ordered axis need not be time |
| `04_histogram_age.png` | Distribution → histogram; a bar chart is not a histogram |
| `05_scatter_age_fare.png` | Relationship → scatter; "no relationship" is still an answer |
| `06_pie_vs_stacked_bar.png` | Composition → why a bar beats a pie |
| `07_grouped_bar_class_sex.png` | Two categories at once, and why that is the ceiling |
| `08_messy_bad_example.png` | **Anti-example** — 29 bars, rainbow palette, dual y-axis, no message |
| `09_clear_one_message.png` | The fix — one question, grey for context, colour for the message |

> Charts `08` and `09` are designed to sit side by side on one slide. That pairing is the core of Part 5.

### The assignments — [`week1/assignments/TASKS.md`](week1/assignments/TASKS.md)

Five datasets, five tasks. None of them is the Titanic set used in the lecture, so nothing can be copied
across. Between them they require every chart type from Part 4.

| Task | Dataset | Rows | Practises |
|---|---|---|---|
| 1 | `datasaurus.csv` | 1,846 | **Why visualize** — 13 datasets with near-identical statistics and wildly different shapes |
| 2 | `gapminder.csv` | 1,704 | **Trends and the spaghetti problem** — 142 countries × 12 years; build the mess, then fix it two ways |
| 3 | `penguins.csv` | 344 | **Distributions and relationships** — plus a real Simpson's paradox to discover |
| 4 | `mpg.csv` | 398 | **Chart choice** — five questions, five different charts, each justified |
| 5 | `flights.csv` | 144 | **Time series** — separating a trend from a seasonal cycle |

Each task asks for the chart *and* a written justification of the chart type. The marking guide is at the
bottom of `TASKS.md`.

---

## The rules students are held to

Taken from the lecture and applied to every submitted chart:

- **Title the finding, not the subject.** "1st class survived 3× more often" beats "Survival by class".
- **Bars start at zero.** The bar's length *is* the value, so a cut axis is a lie told with geometry.
- **Never use two y-axes.** Two measures means two charts.
- **Colour must mean something.** If it is decoration, remove it.
- **Grey is a colour.** Mute the context, spend your one bright colour on the message.
- **Sort unordered categories by value.** Ordered ones keep their natural order.
- **Label selectively.** Label every point and you have rebuilt the table.
- **Declare missing data on the chart**, not in a footnote nobody reads.
- **Use a colour-blind-safe palette.** Roughly 1 in 12 men cannot read a red/green chart.

---

## Notes for anyone reusing this material

- The notebook sets a **house style** once in its setup cell — a fixed eight-hue categorical palette chosen
  so that adjacent colours stay distinguishable under colour vision deficiency, plus recessive grid lines and
  no chart border. Every chart inherits it. Change it in one place to re-theme the whole lecture.
- Chart `08` is **deliberately bad** and is labelled as such in the code. Do not lift it as an example of
  good practice.
- Hidden in chart `08` is a second lesson worth pointing out in class: its first bar reads 0% survival for
  first-class female children, a group containing **exactly one passenger**, drawn at the same visual weight
  as a group of 43. Slice data finely enough and you chart noise as though it were a finding.
