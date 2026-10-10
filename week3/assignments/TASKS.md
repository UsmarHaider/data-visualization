# Week 3 — Assignments: Matplotlib & Seaborn

Five parts covering **Lecture 5** (Matplotlib architecture and figure customization)
and **Lecture 6** (statistical visualization with Seaborn).

| | |
|---|---|
| **L5** | Use Python for basic static chart generation — **CLO1 · Competence** |
| **L6** | Create statistical charts for data exploration — **CLO2 · Competence** |

---

## The point of this week

Week 1 taught you to **see** a chart. Week 2 taught you to **judge** one.
Week 3 teaches you to **build** one — and the fastest way to learn what a good
chart is made of is to take nine bad ones apart.

Nine analysts each published a claim. Part A gives you their data and the
recipe each of them followed, and asks you to **rebuild their chart yourself**
— then work out why it is wrong.

Every one of those charts is arithmetically correct. No number has been
fiddled, no axis is secretly truncated unless the recipe says so, and several
are drawn more carefully than most things you will see published. They are
still all wrong.

> **The one thing this week is really testing.** For every chart there is an
> answer that sounds clever and is not the reason. *"Correlation is not
> causation." "The y-axis is truncated." "The sample is too small."* You will
> reach for one of those, and in most of these nine cases it is either
> irrelevant or already ruled out by how the chart was drawn.
>
> You do not get the marks for being suspicious. You get them for **naming the
> mechanism and proving it from the data.**

| Part | Covers | Marks |
|---|---|---|
| **A** | Diagnose the nine charts | 36 |
| **B** | Lie Factor audit, computed in Python | 15 |
| **C** | Prove a palette is colour-blind safe | 9 |
| **D** | Build the clinical review figure | 25 |
| **E** | One page of written justification | 15 |
| | | **100** |

---

## Setup

Everything is already in this folder. Nothing to download.

```bash
cd week3/assignments
python3 vizlib.py          # self-check: confirms the toolkit works
```

You should get three worked Lie Factors and a colour-blindness simulation of
the course palette. If that runs, everything else will.

**Requirements:** Python 3.9+, and:

```bash
pip install pandas numpy matplotlib seaborn scipy
```

| Path | What it is |
|---|---|
| `vizlib.py` | The toolkit. Palette, `lie_factor()`, `simulate_cvd()`, `match_stats()`. Read it — it is short. |
| `data/` | Ten datasets. Every one of them has something wrong with it. |
| `data/DATA_DICTIONARY.md` | What the columns **mean**. Not what is wrong with them. |
| `starter/starter.py` | Skeleton for Part D. Runs as given and produces a deliberately bad figure. |
| `starter/palette_check.py` | Skeleton for Part C. |
| `starter/popout.py` | The Week 1 carry-forward. Optional, 5 bonus marks. |

---

## The rules

- **Every figure starts with `fig, ax = plt.subplots()`.** There is no
  `plt.plot()` in the starter files and there should be none in yours. Slide 15.
- **Title the finding, not the subject.** "Readmissions jumped 36% after the
  July rollout" beats "Readmissions by month". The second one is a file name.
- **Declare every parameter that changes the picture.** `bins`, `bw_adjust`,
  `cut`, `vmin`, `vmax`, a log scale, a subsample size. "I used the default" is
  not a decision; it is an unexamined one.
- **State every row you removed, with the rule and the count.** A row dropped
  without a stated reason is a row lost.
- **Never a dual-axis chart.** Two measures of different scale become two
  panels, or one panel indexed to a common base. This rule has no exceptions,
  and Part B question 5 is about why.
- **Save before you show.** `fig.savefig(...)` then `plt.show()`. The other way
  round writes a blank file.
- **Your script must run from a clean environment.** A figure you cannot
  regenerate scores zero on reproducibility, however good it looks.

---

## Part A · Rebuild nine charts, then take them apart  (36 marks)

Nine analysts published nine claims. You get their data and the recipe each of
them followed. **Build the chart, then work out why it is wrong.**

Rebuilding it is not busywork — it is Lecture 5. You cannot argue about a
truncated axis or a default bin width until you have been the person who chose
them.

### What to hand in for each of the nine

Four marks each.

| | Marks |
|---|---|
| **Rebuild it.** Your chart reproduces the published claim from the recipe, and hits the self-check number | 1 |
| **The conclusion and the decoy.** The conclusion the chart invites, in one sentence — plus the first objection you thought of and *why it does not hold here*, ruled out with evidence from the data | 1 |
| **The mechanism.** What is really producing the pattern, named precisely, with the number that demonstrates it | 1 |
| **The redesign.** The honest chart, actually plotted, not described | 1 |

"Correlation is not causation" scores **zero** on the mechanism mark. It is a
true statement about the world and it names no mechanism. Say *which* third
variable, and show the number.

---

### 1 · "Premium-certified helmets have 2.5x the head-injury rate"
`case01_helmet_rickshaw.csv`

> Sum `head_injuries` and `trips` by `helmet_grade`. Plot injuries per 1,000
> trips as a bar chart, y-axis from zero, one bar per grade.

**Self-check:** Standard **2.15**, Premium **5.40**.

### 2 · "Canteen chai sales predict quiz failures"
`case02_chai_quizzes.csv`

> Scatter `cups_doodh_patti_sold` (x) against `quiz_failures` (y), one point
> per month. Fit a least-squares line through it and annotate Pearson r.

**Self-check:** r = **0.98**.

### 3 · "The Smog Action Plan cut Lahore's AQI by a third"
`case03_aqi_monitors.csv`

> Mean `aqi` per `date` across every row. Plot it as a line, **y-axis from
> zero**. Draw a vertical marker at day 61, and a horizontal mean line for
> days 1–60 and another for days 61–120.

**Self-check:** before **202**, after **137** — a **32%** fall.

### 4 · "Four departments behave identically, so fund them equally"
`case04_quartet_depts.csv`

> Not a chart. Produce a table: n, mean study hours, mean score, SD of each,
> Pearson r and the regression slope — one column per `department`.

**Self-check:** every department reports mean **18.00** / **14.50** and
r = **0.816**.

### 5 · "Five cohorts, one set of statistics"
`case05_same_stats_shapes.csv`

> Also not a chart. The same table, one column per `shape_name`.

**Self-check:** every cohort reports **48.00** / **63.00**, SD **12.00** /
**15.00**, r = **0.420**.

### 6 · "Creatinine tracks HbA1c — a finding"
`case06_sensor_matrix.csv`

> Correlation matrix of every numeric column except `age_band`, `study_site`
> and `hr_device_model`. Draw it as an annotated heatmap exactly as the
> analyst did: `cmap="Reds"`, **no `vmin`/`vmax`**, both triangles shown.

**Self-check:** creatinine ↔ hba1c = **0.77**, systolic ↔ map_mmhg =
**0.96**, and the matrix is **20 × 20**.

> This one has something wrong with how it is *drawn* as well as what it
> *says*. Report both, and be clear about which of the two fixing the drawing
> actually solves.

### 7 · "ShaheenGo ran at a loss until May"
`case07_dual_axis_series.csv`

> Line chart with **two y-axes**: `revenue_pkr_m` on the left limited to
> 50–80, `cost_pkr_m` on the right limited to 40–56. `ax.twinx()`.

**Self-check:** the cost line sits **above** the revenue line for the first
four months.

### 8 · "Three bin widths, three different distributions"
`vitals_10k.csv`

> Three histograms of `systolic` side by side, sharing nothing but the data:
> `bins=3`, `bins=45`, `bins=400`.

**Self-check:** n = **10,000** in all three panels.

### 9 · "4.4% of the density sits above 100% saturation"
`vitals_10k.csv`

> Kernel density estimate of `spo2` with the **default** bandwidth. Extend the
> x-axis to 108 so the whole curve is visible, and mark 100.

**Self-check:** the maximum value in the data is **100**. The curve is not.

---

### Two things that will save you an afternoon

- **You are the one choosing the axis now.** Recipe 3 says "y-axis from zero",
  and it means it. If your instinct is to write "the axis is truncated", check
  your own code first.
- **Several of these files carry a column the recipe never plots.** Open the
  CSV before you theorise. A hypothesis you can test and reject is worth more
  marks than one you assert.

## Part B · Lie Factor, in code  (15 marks)

Week 2 had you measure graphics with a ruler. This week you compute.

Open `data/case07_lie_factor.csv`. It holds, for five published graphics, the
two data values, the measured ink, the unit that ink was measured in, whether
the quantity is encoded by a length or an area, and a prose description of
what each graphic does. You do not need to see the pictures to audit them —
that is the point of measuring.

Tufte's Lie Factor:

```
                effect shown in the graphic
Lie Factor  =  ─────────────────────────────        effect = (final − initial) / initial
                   effect in the data
```

Honest is 1.0. Tufte accepts 0.95 – 1.05.

1. For each graphic **A–E**, call `vizlib.lie_factor()` and produce a table of
   data effect, graphic effect, Lie Factor and verdict. **(5 marks)**
2. **Exactly one of the five is honest.** Say which, and say what each of the
   other four does wrong — in terms of what the ink is encoding. **(3 marks)**
3. Some of the five need `ink_dimension=2`. Identify them, and explain in one
   sentence what goes wrong if you leave it at 1. **(3 marks)**
4. One of them has a Lie Factor **below** 1. Explain why an understated chart
   is still a distortion, and say who benefits from it. **(2 marks)**
5. **Chart F** is the dual-axis chart you rebuilt in Part A, case 7. Compute
   its Lie Factor — or explain why you cannot. Then look again at
   `case07_dual_axis_series.csv` and say what the data actually shows.
   **(2 marks)**

> Question 5 is worth more thought than its two marks suggest. Work out what
> the Lie Factor formula *assumes* about the chart before you try to apply it.

---

## Part C · Prove the palette, do not claim it  (9 marks)

Week 2 told you to use a colour-blind-safe palette. Anyone can claim that.

Roughly 1 man in 12 and 1 woman in 200 has some form of colour-vision
deficiency. In a cohort of 60 that is about three people who cannot read a
red/green chart. They will not tell you. The simulation will.

`starter/palette_check.py` gets you going.

1. Pick a four-colour palette you like the look of — matplotlib's `tab10`,
   Excel's defaults, one from a dashboard you admire. **Do not pick one you
   already believe is safe.** Run it through `vizlib.simulate_cvd()` for
   `deutan`, `protan` and `tritan`, and show the before/after swatches.
   **(3 marks)**
2. Do the same for `vizlib.PALETTE["series"]` plus the fourth slot. **(2 marks)**
3. Use `vizlib.worst_pair()` to find the pair that collapses worst in **each**
   palette, and report its ΔE. Yes, the course palette has one too — find it
   and say what it means for how you are allowed to use that colour.
   **(2 marks)**
4. State the rule you will follow for the rest of this course when a chart
   needs more than three categories. **(2 marks)**

> The answer to 4 is not "find a bigger palette". Look at what the fourth slot
> does under simulation, then think about what you would add to the chart
> *instead of* another colour.

---

## Part D · Build the clinical review figure  (25 marks)

The application task from Lecture 6, with a real file behind it.

`data/vitals_10k.csv` holds 10,000 patient vital-sign records from the Week 3
case study: a clinical analytics group must inspect them before a safety
review, find data-entry anomalies, check which measurements are not normally
distributed, and spot correlated risk indicators.

**The file has several things wrong with it, none of them announced.**
Find them before you plot anything. Run, in this order:

```python
df.info()
df.describe().T
df.ward.value_counts()
df.admit_date.head(20).tolist()
```

Four of the problems are visible in that output alone. `starter/starter.py`
prints all four for you on its first run.

Then build **one 2×2 figure**:

| Panel | What it shows |
|---|---|
| 1 | A distribution, with the bin width or bandwidth declared on the figure |
| 2 | A box plot comparing a measure across the wards |
| 3 | A scatter of the one pair worth plotting — panel 4 tells you which |
| 4 | An annotated correlation heatmap, built to the rules from Lecture 6 |

Then finish it: message titles that state findings, axis labels with units,
spines off, a colour-blind-safe palette, and
`fig.savefig(dpi=300, bbox_inches="tight")`.

### Marking

| | Marks |
|---|---|
| The script runs from a clean environment and produces the PNG | 5 |
| Every data problem handled, each with a stated rule | 8 |
| Four panels, each answering a question you can state in one sentence | 6 |
| Finished: titles, units, spines, palette, 300 dpi, source note | 6 |

### Two things that lose marks every year

- **Wide data passed to Seaborn.** `data/ward_los_wide.csv` is in this folder
  on purpose. Seaborn wants long data — one row per observation. `.melt()` it.
- **`plt.savefig()` called after `plt.show()`**, which writes a blank file.
  Hold the named `fig` and call `fig.savefig()` before you show anything.

---

## Part E · The written justification  (15 marks)

One page. Not two.

1. **Per panel:** the question it answers, why that chart type, and which
   Week 2 channel rule it follows. **(6 marks)**
2. **Every parameter you chose**, named and defended. **(5 marks)**
3. **Every row you removed**, with the rule, the count, and what the number
   moved from and to. **(4 marks)**

### The ethics clause — read this one twice

`heart_rate` in `vitals_10k.csv` contains readings above 300 bpm. They are
device faults, and removing them is correct: no human heart beats at 400 bpm.

`showfliers=False` also makes them disappear, and tells the reader nothing.

**If you hide them and do not say so, you lose all 4 marks for item 3,
whatever the rest of the page says.** The defensible version is three
sentences:

> Readings above 250 bpm were removed as device faults (n = …).
> Mean heart rate moves from … to … bpm.
> The figure was also produced without the exclusion; it is in the appendix.

Then apply Week 2's symmetry test to your own write-up: **would you have made
the same removal if it had weakened your conclusion instead of strengthening
it?** If the answer is no, it is not a cleaning rule. It is an edit.

---

## Bonus · Week 1, rebuilt in code  (5 marks)

`starter/popout.py` — optional.

In Week 1 you counted the 3s in a grid of digits, twice. This week you build
the experiment instead of sitting in it. Panels 1 and 2 are written for you;
panels 3 and 4 are yours (size only, then colour **and** shape together).

Then run it on **five classmates**, time them, and chart the result: panel on
the x-axis, mean seconds on the y-axis, individual times as a strip plot over
a faded bar. Zero baseline, a title that states your finding, and a source
note carrying n = 5 and how you randomised the order.

Three sentences: which channel was fastest, which was slowest, and whether
redundant coding cost anything in speed. Results that disagree with the
textbook score full marks when they are reported honestly and explained.

---

## What you hand in

One ZIP on the LMS, named `W3_<RollNo>.zip`:

```
partA_charts.py            rebuilds all nine, and plots your nine redesigns
partA_diagnosis.pdf        your nine diagnoses, with both figures per case
partB_lie_factor.py        + its printed output
partC_palette.py           + the before/after swatch PNG
partD_figure.py            the script
partD_figure.png           the exported 300 dpi figure
partE_justification.pdf    one page
popout_experiment.py       (bonus, optional) + the chart
```

Cite your sources. All data in this folder is synthetic and generated for
CDB601220 — say so if you quote a number from it.

---

## Readings

- **VanderPlas**, *Python Data Science Handbook*, Ch. 4 — especially
  "Multiple Subplots" and "Customizing Ticks". Free online.
- **Seaborn tutorial** — distributions, categorical, matrix plots, and
  "Overview of seaborn plotting functions" (figure-level vs axes-level).
- **Wilke**, *Fundamentals of Data Visualization*, Ch. 7 and Ch. 9. Free online.
- **Anscombe, F. J. (1973)**, "Graphs in Statistical Analysis",
  *The American Statistician* 27(1), 17–21. Four pages, and chart 4 is his.
- **Matejka & Fitzmaurice (2017)**, "Same Stats, Different Graphs". Chart 5 is
  built the way they built the Datasaurus Dozen — read `vizlib.match_stats()`,
  it is four lines.
