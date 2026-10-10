# Data Visualization

Course repository — lecture notebooks, datasets and assignments.

Every lecture is a single Jupyter notebook that runs top to bottom on real, downloaded data. Notebooks are
committed **with their outputs**, so you can read the whole lecture on GitHub without running anything.

---

## Contents

| Week | Topic | Material |
|---|---|---|
| **1** | Why visualization, and choosing the right chart | [`week1/`](week1/) |
| **2** | Visual perception — preattentive attributes, Gestalt, cognitive load | [`week2/`](week2/) |
| **3** | Matplotlib & Seaborn — building figures, and nine charts that are wrong | [`week3/`](week3/) |

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

# Week 1 assignments
cd assignments
python3 download_assignment_data.py

# Week 2 assignments
cd ../../week2/assignments
python3 download_assignment_data.py

# Week 3 assignments — data is already committed, nothing to download
cd ../../week3/assignments
python3 vizlib.py          # self-check that the toolkit runs
```

**Requirements:** Python 3.9+, and:

```bash
pip install pandas numpy matplotlib seaborn scipy jupyter ipykernel
```

> No data files are committed that you cannot re-download. Each folder has a `download_*.py` script that
> fetches its datasets from public sources, so the repository stays reproducible. Week 2 additionally
> *generates* three perception stimulus files from a fixed seed (`SEED = 42`), so every student gets
> identical stimuli.

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

---

## Week 2 — Visual perception

**CLO1 — Identify how the human brain processes visual information.**

Week 2 is assignment-only: five tasks in [`week2/assignments/TASKS.md`](week2/assignments/TASKS.md).

| Task | Topic | Data |
|---|---|---|
| 1 | Preattentive attributes and visual search | `stimuli_search.csv` |
| 2 | Gestalt principles of grouping | `stimuli_gestalt.csv` |
| 3 | Cognitive load and the data-ink ratio | `car_crashes.csv`, `tips.csv` |
| 4 | Channel effectiveness, measured | `channel_trials.csv`, `iris.csv` |
| 5 | Capstone — redesign one chart for the human visual system | `gapminder.csv` or `diamonds.csv` |

### What makes this week different

Three of the five tasks ask the student to **run a small experiment on a real person** — timing a visual
search, counting perceived groups, or estimating a ratio from a single encoded channel. Perception is a claim
about how a brain behaves, so the brief treats it as something to measure rather than recite. Results that
disagree with the textbook ranking score full marks when they are reported honestly and explained.

### Generated stimuli

Preattentive search and Gestalt grouping cannot be demonstrated on an ordinary dataset: they need displays
where exactly one feature varies at a time. `download_assignment_data.py` therefore downloads five public
datasets **and generates three stimulus files** with a fixed seed:

| File | Rows | What it holds |
|---|---|---|
| `stimuli_search.csv` | 2,430 | 90 trials across colour, shape and conjunction conditions at five set sizes |
| `stimuli_gestalt.csv` | 284 | Six panels, one per Gestalt principle, built so connection fights proximity and similarity |
| `channel_trials.csv` | 30 | 5 channels × 6 true ratios, with blank columns for a reader's estimates |

The `conjunction` condition is the centre of the week: the target is the only red circle, and every
distractor is either a red square or a blue circle — so each one shares exactly one feature with the target.
Search time stays flat as the display grows in the colour and shape conditions, and rises in the conjunction
condition. Task 1 makes the student measure that slope themselves.

Full briefs, the rules and the marking guide are in
[`week2/assignments/TASKS.md`](week2/assignments/TASKS.md).

---

## Week 3 — Matplotlib & Seaborn

**CLO1 — Use Python for basic static chart generation.**
**CLO2 — Create statistical charts for data exploration.**

Week 3 is assignment-only: five parts in
[`week3/assignments/TASKS.md`](week3/assignments/TASKS.md), plus a bonus that
rebuilds the Week 1 perception experiment in code.

| Part | Topic | Marks |
|---|---|---|
| A | Rebuild nine charts that are wrong, then take them apart | 36 |
| B | Lie Factor, computed in Python instead of measured with a ruler | 15 |
| C | Prove a palette is colour-blind safe, with the failure shown | 9 |
| D | **Hands-on:** the 2×2 clinical review figure, exported at 300 dpi | 25 |
| E | One page of written justification, including the ethics clause | 15 |
| bonus | Week 1's preattentive experiment, rebuilt and run on five people | 5 |

### What makes this week different

Students are not handed nine finished charts. They get nine **published claims
and the recipe each analyst followed**, and rebuild every chart themselves
before diagnosing it — which turns Part A from a reading exercise into a
Lecture 5 one. Each case carries a self-check number so they know the rebuild
is faithful.

Every one of those charts is **arithmetically correct**. Nothing has been
fiddled. They are still all wrong — and in most of them the obvious objection
(*"correlation is not causation"*, *"the axis is truncated"*, *"n is too
small"*) is either irrelevant or ruled out by the recipe itself.

Scepticism is cheap and generic. The marks are for naming the mechanism and
proving it from the data, which means opening the CSV and computing something.
Three of the nine cases hand the student a column that is **not on the chart**,
specifically so a plausible hypothesis can be tested and rejected.

Between them the nine cases cover the main ways a chart can be arithmetically
correct and still wrong: a third variable that reverses a comparison, a
denominator that moves, data that goes missing in a pattern, summary statistics
that do not constrain shape, a screening matrix read as a result, an axis
convention that manufactures an event, and parameters that quietly decide what
a distribution looks like.

Which case is which is not stated anywhere a student can read. Finding that
out is the assignment.

### The toolkit — [`week3/assignments/vizlib.py`](week3/assignments/vizlib.py)

Short enough to read in one sitting, and students are expected to:

| Function | What it does |
|---|---|
| `lie_factor(...)` | Tufte's Lie Factor, with the `ink_dimension` argument that is the whole of two cases |
| `simulate_cvd(...)` | Machado (2009) matrices in linear RGB — takes hex codes **or** a rendered figure |
| `delta_e` / `worst_pair` | Perceptual distance in OKLab, so "is this palette safe" is a number |
| `match_stats(...)` | Forces a dataset to exact mean, SD and r while keeping its shape |

`python3 vizlib.py` self-tests. Its worked Lie Factor examples are deliberately
**not** the ones in the Part B audit.

### The palette

A three-slot Okabe–Ito subset: `#0072B2` · `#D55E00` · `#009E73`. It passes
every check on a light surface with **all pairs** compared — worst ΔE 11.0
under deuteranopia, 18.7 under normal vision, all three above 3:1 contrast.

A fourth hue (`#CC79A7`) is provided for the cases that need one. It drops the
CVD margin to ΔE 7.5, so any chart using it must carry direct labels or a table
view. Part C makes students find that themselves rather than take it on trust.

### Teacher material

Model answers, the generator scripts and the reveal figures are **not** in this
repository. `.gitignore` blocks `*TEACHER*`, `*_KEY*`, `*ANSWER*`, `solution/`,
`make_task.py`, `reveals.py` and `teacher_key.py` from ever being committed here.
