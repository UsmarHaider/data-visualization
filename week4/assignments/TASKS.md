# Week 4 — Assignments: Time-Series, Proportions & Hierarchies

Five parts covering **Lecture 7** (time series) and **Lecture 8**
(proportions and hierarchies).

| | |
|---|---|
| **L7** | Design time-series visualizations that expose trend, seasonality and cycles; apply rolling averages and time aggregation — **CLO2 · Competence** |
| **L8** | Compare part-to-whole strategies; construct hierarchical visualizations — **CLO2 · Competence** |

---

## The point of this week

Week 1 taught you to **see** a chart. Week 2 taught you to **judge** one.
Week 3 taught you to **build** one. Week 4 gives you the two data shapes
that punish a careless build hardest:

- a measurement that **moves through time**, where the x axis is already
  spent and equal distance must mean equal duration; and
- a whole that **splits into parts**, where the parts have to add up, and
  then splits again.

Week 3's nine broken charts were broken by a *drawing* decision — a bin
width, a truncated axis, a rainbow colormap. This week's nine are broken
**before any drawing happens**: by a parse, a resample, a window, a
denominator. You will not find them by looking at the figure.

> **The one thing this week is really testing.** Last week the trap was
> reaching for a generic objection. This week the trap is reaching for a
> *generic fix*. "Just smooth it." "Just use a bar chart." "Just parse the
> dates." Each of those is sometimes right and each one, applied without
> naming the mechanism, will walk you straight into a different error —
> and in three of the nine cases, into exactly the error the analyst made.
>
> You do not get the marks for fixing the chart. You get them for
> **naming the mechanism and proving it from the data.**

| Part | Covers | Marks |
|---|---|---|
| **A** | Rebuild nine charts, then diagnose them | 36 |
| **B** | Smoothing, windows and panel shape, computed | 15 |
| **C** | Part-to-whole legality, and the pie-ranking experiment | 9 |
| **D** | Build the e-commerce review figure | 25 |
| **E** | One page of written justification | 15 |
| | | **100** |
| **F** | *Bonus* — Week 1's last task, on data you found yourself | 5 |

Part F is marked **out of 5 and reported separately**. It is not added into
the 100 and it is not a gate on anything.

---

## Setup

Everything is already in this folder. Nothing to download.

```bash
cd week4/assignments
python3 tslib.py          # self-check: confirms the toolkit works
```

You should get an index audit, a window report, a measured trailing-mean
lag, a banked aspect ratio, and a PNG with a treemap, a sunburst and a
cycle plot in it. If that runs, everything else will.

**Requirements:** Python 3.9+, and:

```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels squarify
```

Two of those are new this week. `statsmodels` gives you
`seasonal_decompose`; `squarify` gives you the treemap layout.

> **Plotly is optional.** `px.treemap`, `px.sunburst` and `px.icicle` are
> one-liners and they are genuinely better once they are interactive —
> which is Week 6. Everything this week is markable in matplotlib, and
> `tslib` ships `treemap()`, `sunburst()` and `cycle_plot()` so you are
> never blocked on an install. If you use Plotly as well, say so, and
> still submit a 300 dpi static export.

| Path | What it is |
|---|---|
| `vizlib.py` | **Week 3's toolkit, unchanged.** Palette, `lie_factor()`, `simulate_cvd()`, `save_fig()` |
| `tslib.py` | This week's toolkit, built on top of `vizlib`. Read it — it is short |
| `data/` | Twelve datasets. Every one has something wrong with it |
| `data/DATA_DICTIONARY.md` | What the columns **mean**. Not what is wrong with them |

There are no starter scripts this week. Week 3 gave you three skeletons with
the structure already laid out; from here you write the script yourself. The
toolkit is the scaffolding — read `tslib.py` before you start, not after.

---

## Carried forward

Nothing from Weeks 1–3 is retired. This is where each idea comes back, and
you are expected to name them by these names in your write-up.

| From | The idea | Where it returns this week |
|---|---|---|
| **W1** | The question chooses the chart | Part A redesigns; Part D panels 3 and 4 answer different questions about the same numbers |
| **W1** | Title states the finding | Every figure, every part |
| **W1** | Bars start at zero; never two y-axes | Part A cases 5 and 6; the dual-axis ban is absolute |
| **W1** | `flights.csv` — separating trend from seasonal cycle | **Part F**, rebuilt on data you find |
| **W1** | Spaghetti, and the two ways out | Part A case 7's redesign: unstack or facet |
| **W2** | Channel ranking: position > length > angle > area | Part C (pie vs bars) and Part D (treemap vs bars) |
| **W2** | One pop-out per chart; grey for context | Part D panel 1 — raw in grey, signal in colour |
| **W2** | Cognitive load, 4 ± 1 chunks | The `Other` bucket in Part D panel 3 |
| **W2** | Lie Factor | Part B question 5, applied to aspect ratio instead of ink |
| **W2** | Experiments run on real readers | Part C. Invented results still score zero |
| **W3** | `fig, ax = plt.subplots()`, always | Every figure. No `plt.plot()` |
| **W3** | Declare every parameter that changes the picture | Part E. The window length is now one of them |
| **W3** | State every row you removed, with rule and count | Part E, and the ethics clause |
| **W3** | Sequential colormap when there is no midpoint | Part D panel 2's heatmap |
| **W3** | Colour-blind-safe palette, proved not claimed | `vizlib.PALETTE` is already in `tslib` |
| **W3** | `fig.savefig()` **before** `plt.show()` | Still writes a blank file the other way round |

---

## The rules

**New in Week 4 — applied to every chart you produce:**

- **Audit the index before you plot.** A sorted `DatetimeIndex`, with
  duplicates and gaps counted. `tslib.audit_index()` does it in one call and
  its output belongs in your write-up. Slide 10.
- **Name the window on the chart.** "14-day rolling median", not "trend". A
  smoothed line without a stated window scores nothing for the smoothing,
  however good it looks. Slide 23.
- **Keep the raw series.** Smoothing does not remove noise, it moves it.
  The faint raw line stays on the chart. Slide 20.
- **Say which aggregation you used, in the axis label.** "Sessions per day
  (sum)" not "sessions". Never resample a level with `sum()`. Slide 12.
- **A missing period is data.** Reindex onto a complete calendar, let the
  line break, and report the count. If you interpolate, mark it. Slide 13.
- **Check the three part-to-whole conditions before drawing any share** —
  exclusive parts, a meaningful whole, and the share being the actual
  question. `assert abs(shares.sum() - 100) < 1e-6`. Slide 32.
- **Declare the `Other` bucket.** How many categories went in and what they
  are worth. Slide 49.
- **Negatives have no area.** They cannot go in a pie, a treemap or a
  sunburst. Split them out and show them. Slide 49.
- **State the aspect ratio.** Nobody reports one, which is exactly why it
  works as a way to mislead. `tslib.banked_figsize()` computes it. Slide 16.

**Still in force from Weeks 1–3:** everything in the table above. The
dual-axis ban has no exceptions.

---

## Part A · Rebuild nine charts, then take them apart  (36 marks)

Nine analysts published nine claims. You get their data and the recipe each
of them followed. **Build the chart, then work out why it is wrong.**

Every one of these charts is arithmetically correct. No number has been
fiddled, no axis is truncated unless the recipe says so, and several are
drawn more carefully than most things you will see published.

### What to hand in for each of the nine

Four marks each.

| | Marks |
|---|---|
| **Rebuild it.** Your chart reproduces the published claim from the recipe, and hits the self-check number | 1 |
| **The conclusion and the decoy.** The conclusion the chart invites, in one sentence — plus the first objection you thought of and *why it does not hold here*, ruled out with evidence from the data | 1 |
| **The mechanism.** What is really producing the pattern, named precisely, with the number that demonstrates it | 1 |
| **The redesign.** The honest chart, actually plotted, not described | 1 |

"The dates are wrong" scores **zero** on the mechanism mark for case 1, in
the same way "correlation is not causation" scored zero last week. Say
*what* is wrong with them, *which* rows it affects, and show the number
that changes.

---

### 1 · "Orders peak in Q1 and collapse every year — a clear annual cycle"
`case01_orders_stringdate.csv`

> Sort the 24 rows by the `month` column. Plot `orders` against it as a
> line with markers, y-axis from zero.

**Self-check:** 24 points. The line climbs for four points, drops **958**,
climbs for eleven, drops **978**, then climbs again.

### 2 · "Sales grew steadily, 22%, across the quarter"
`case02_shop_closed.csv`

> Plot `sales_pkr_k` against the **row number** — `ax.plot(range(len(df)),
> df.sales_pkr_k)` — because the dates are "just labels". Add a
> least-squares trend line.

**Self-check:** 69 points, first **207**, last **253**, a **+22%** rise.

### 3 · "Peak load jumped 43% overnight on 1 July"
`case03_bandwidth_levels.csv`

> Resample `concurrent_users` to daily with `.sum()`. Plot the daily series
> as a line, y-axis from zero.

**Self-check:** the June daily mean is about **8,800**, the July daily mean
about **12,500** — a **+43%** step.

### 4 · "The new checkout flow started working on 7 September"
`case04_intervention_lag.csv`

> Plot `conversion_pct` raw in grey, with a **31-day trailing** rolling
> mean on top. Read the turning point off the smoothed line and mark it.

**Self-check:** the trailing mean bottoms out on **2025-09-07**.

### 5 · "Revenue has fallen for six straight months"
`case05_revenue_window.csv`

> Take **May to November 2025** only. Plot it as a line with markers,
> **y-axis from zero**.

**Self-check:** 7 points, **158.8** down to **92.2**, a **−41.9%** fall.

> Before you write "the axis is truncated" — read the recipe again. It is
> not. And check `n` before you write that the sample is too small.

### 6 · "Orders collapsed in October"
`case06_monthly_partial.csv`

> Resample `orders` to monthly totals with `.sum()`. Plot as bars from
> zero.

**Self-check:** ten bars. September is **10,805** and October is
**4,041** — 37% of it.

### 7 · "Product D has been erratic since mid-2024"
`case07_stacked_products.csv`

> Stacked area chart of the four products, in column order, `product_a` at
> the bottom and `product_d` on top.

**Self-check:** the total envelope runs between about **548** and **709**.

> This one has a column the recipe never isolates. Open the CSV.

### 8 · "Paid search drives 43% of our customers"
`case08_channel_attrib.csv`

> Count the `True` values in each `touch_*` column, divide by the number of
> customers, and draw a four-slice pie.

**Self-check:** search **42.6%**, social **32.3%**, email **27.5%**,
direct **28.6%**.

### 9 · "Premium is now 38% of revenue — a record"
`case09_premium_share.csv`

> Compute `premium_revenue_pkr_m / total_revenue_pkr_m` per quarter. Plot
> the share as a line, y-axis from zero, and annotate the last point.

**Self-check:** the share rises from **24.0%** to **38.0%**.

---

### Three things that will save you an afternoon

- **Add up your self-check numbers before you theorise.** Case 8's four
  percentages are in the brief above. Add them.
- **Several of these files carry a column the recipe never plots, or a
  property the recipe never checks.** `len(df)` against the span of the
  date column is the cheapest test in this part, and it cracks two cases.
- **Two cases are about the difference between a chart being wrong and a
  chart being incomplete.** For those, the redesign is not a different
  chart type — it is the same chart with something else next to it.

---

## Part B · Smoothing, windows and panel shape — computed  (15 marks)

Week 3 had you compute a Lie Factor instead of eyeballing it. This week you
do the same for the three decisions that silently decide what a time-series
chart says.

Work on the **cleaned daily session series** from Part D — parsed,
de-duplicated, sentinels removed, resampled to daily, gaps and the partial
final month dealt with. You have to finish Part D's cleaning before you can
start Part B; that is deliberate, and it is why Part D is worth the most.

1. **The window is a hypothesis.** Produce `tslib.window_report()` for
   windows 7, 28 and 91. For each, state the cycle it removes, the share of
   the raw variation it removes, and the periods lost at each end. Then say
   which window you will use in Part D and why — in terms of the cycle you
   are cancelling, not smoothness. **(4 marks)**

2. **Three smoothers against one spike.** 29 November 2024 is Black Friday;
   the raw value is **113,710** sessions against a fortnight median of
   about **24,600**. Compute the 14-day centred **mean**, **median** and
   **EWMA** at that date. Report all three, and say which you would use on
   a monitoring dashboard and which in a quarterly report. **(3 marks)**

3. **Decompose it.** Run `seasonal_decompose(..., model="additive",
   period=7)`. Report the peak-to-trough amplitude of the weekly seasonal
   component, and the date of the **largest residual**. The residual is the
   point: everything explainable has been removed, so what is left is the
   event worth investigating. Then re-run with `period=365` and say in one
   sentence what moves from `resid` into `seasonal`. **(3 marks)**

4. **Trailing or centred.** Use `tslib.lag_at_turn()` on the series with a
   31-day window. Report the lag in days against the half-window. Then
   answer: a live dashboard refreshes every morning — which one must it
   show, and what must the caption say? **(2 marks)**

5. **The window is a claim** — the Lie Factor, moved from ink to framing.
   Loop over every combination of **12 start months × 5 window lengths**
   (7, 14, 28, 56, 91) on the same series, fit a straight line to each, and
   count how many combinations produce a **rising** trend and how many a
   **falling** one. Report both counts.

   Then: Tufte's Lie Factor is `(effect shown) / (effect in the data)`.
   Explain why you **cannot** compute it for a cherry-picked window, and
   what the honest substitute is. **(3 marks)**

> Question 5 is worth more thought than its three marks suggest. Work out
> what the Lie Factor formula *assumes* exists before you try to apply it.

---

## Part C · Part-to-whole legality, and the ranking  (9 marks)

1. **The three conditions, tested in code.** For each of the three share
   tables below, run the slide-32 tests — exclusive parts, meaningful
   whole, share-is-the-question — and give a verdict: may this be drawn as
   a pie, a bar chart, or neither?
   - the four `touch_*` columns of `case08_channel_attrib.csv`
   - the eight rows of `shares_eight.csv`
   - `premium` vs `other` revenue in `case09_premium_share.csv`, 2025Q4

   `tslib.exclusivity_check()` does the first test. The other two are
   arguments, not functions. **(3 marks)**

2. **Run the ranking on a real reader.** Draw the eight shares from
   `shares_eight.csv` as a pie with **no numbers on it**, in the file's
   order, `startangle=90, counterclock=False`. Ask your reader to write
   A–H in rank order, largest first, and time them with
   `time.perf_counter()`. Then show the same eight as sorted horizontal
   bars and ask again; time that too. Save both stimuli as PNGs and the
   responses as `pie_ranking_results.csv`, one row per stimulus with the
   reader, their order, and the seconds. **(3 marks)**

3. **Score it.** Against the true order, report how many letters your
   reader placed wrongly on each stimulus, and where in the ranking the
   errors fell. The deck's prediction is specific enough to test: most
   readers get the top two and the bottom one right and disagree about the
   middle, because **C (15.0%), H (13.1%) and G (11.2%)** are three points
   apart. Did yours? **(2 marks)**

4. **State your rule.** One sentence: when, from now on, will you draw a
   pie? **(1 mark)**

> One reader is one reader. Report the times and the errors, say plainly
> what a sample of one can and cannot support, and do not dress it up as an
> experiment. A result that disagrees with the deck and is explained
> honestly scores full marks. **Invented results score zero, and they are
> obvious** — a real reader is slow, inconsistent, and wrong specifically
> in the middle.

---

## Part D · Build the e-commerce review figure  (25 marks)

The application task from slides 54 and 57, with a real file behind it.

`data/sessions_hourly.csv` holds **12,670 hourly rows** of traffic for the
platform on slide 5, and `data/revenue_catalogue.csv` holds its product
catalogue. Leadership reviews one dashboard every Monday. The traffic line
is plotted raw so the weekend drowns the trend, and the category breakdown
is a multi-slice 3-D pie.

**The sessions file has six things wrong with it, none of them announced.**
Find them before you plot anything. Run, in this order:

```python
df.info()
df.describe().T
df.device.value_counts()
df.ts.head(10).tolist()
```

Four of the six are visible in that output alone. The other two only
appear **after** the index is a real `DatetimeIndex` — which is the whole
lesson of slide 10, and the reason the order of those four calls matters.

> **The trap in this file.** `pd.to_datetime(df.ts)` guesses one format and
> turns every row in the other format into `NaT`, which at least tells you
> something is wrong. `pd.to_datetime(df.ts, format="mixed")` parses every
> row, raises nothing, loses no rows — and **silently moves the series to
> the wrong dates**. Check `df.index.min()` and `.max()` against what you
> expect, not just the row count. A parse can succeed on every row and
> still be wrong.

Then build **one 2×2 figure**:

| Panel | What it shows |
|---|---|
| 1 | The daily series: raw in light grey, a rolling mean on top, the window named in the title |
| 2 | A day-of-week × hour-of-day heatmap of mean sessions, sequential colormap |
| 3 | A treemap (or sunburst) of category → sub-category net revenue |
| 4 | The same sub-categories as sorted horizontal bars, values printed |

Panels 3 and 4 are the argument of Lecture 8, side by side: the treemap
shows **where the mass is**, the bars show **by how much**. Say in Part E
which question each one answers.

Then finish it: message titles that state findings, axis labels with units
*and* the aggregation, spines off, a colour-blind-safe palette,
**one hue per parent category** in the treemap, and
`fig.savefig(dpi=300, bbox_inches="tight")`.

**Self-check for the hierarchy.** If you have handled the duplicate SKU and
the negative rows correctly, your eight sub-category shares will land
within **0.3 percentage points** of `shares_eight.csv`. If one of them is
out by around **0.9 points**, you have not.

### Marking

| | Marks |
|---|---|
| The script runs from a clean environment and produces the PNG | 5 |
| Every data problem handled, each with a stated rule | 8 |
| Four panels, each answering a question you can state in one sentence | 6 |
| Finished: titles, units, spines, palette, 300 dpi, source note | 6 |

### Three things that lose marks every year

- **A rolling mean computed before resampling to a regular frequency.** A
  7-row window on an irregular index is not seven days of anything.
- **`resample("D")` treated as a gap check.** It is not. Resampling builds
  a complete regular index, so days that were never recorded come back as
  rows — `0` if you use `.sum()`, `NaN` if you use `.sum(min_count=1)`.
  Count the gaps on the **hourly** index, before you resample.
- **`plt.savefig()` called after `plt.show()`**, which writes a blank file.
  Hold the named `fig` and call `fig.savefig()` first.

---

## Part E · The written justification  (15 marks)

One page. Not two.

1. **Per panel:** the question it answers, why that chart type, and which
   Week 2 channel rule it follows. **(4 marks)**
2. **Every time decision, named and defended:** the parse and how you
   resolved the ambiguous format, the resolution, the aggregation and why
   it suits a flow, the window length and which cycle it removes, centred
   or trailing and why. **(5 marks)**
3. **Every row you removed**, with the rule, the count, and what the number
   moved from and to. **(3 marks)**
4. **Every level you rolled up:** what is in `Other`, how many categories,
   what they are worth, and where you cut the depth. **(3 marks)**

### The ethics clause — read this one twice

Week 3's clause was about rows you delete. This week's is about **the
window you choose**.

Your Part B question 5 result is the evidence: on one unchanged series,
some start-and-window combinations produce a rising trend and others a
falling one. Nobody reading your chart can see the combinations you
rejected.

**If you chose your start date or your window after seeing which one looked
better, and do not say so, you lose all 5 marks for item 2**, whatever the
rest of the page says. The defensible version is three sentences:

> The window was fixed at 7 days before plotting, because the cycle being
> removed is weekly (Part B.1).
> The series is shown from its first recorded day; no start date was
> selected.
> A 28-day version is in the appendix and does not change the direction.

Then apply Week 2's symmetry test to your own write-up: **would you have
made the same choice if it had weakened your conclusion instead of
strengthening it?** If the answer is no, it is not a method. It is an edit.

---

## Part F · Bonus — Week 1's last task, on your own data  (5 marks)

Optional, marked separately, never added into the 100.

In Week 1, Task 5, you were handed `flights.csv` — 144 clean monthly rows —
and asked to separate a rising trend from a repeating within-year cycle.
The last question was left open:

> the seasonal swing gets visibly bigger every year. Is that because the
> seasonality is growing, or just because the airline is growing? Suggest a
> chart that would settle it.

Week 1 asked you to *suggest* one. Now settle it, on data you find
yourself.

1. Find a temporal dataset of **at least 18 months** with a category
   column, from a real source you cite with the date you downloaded it —
   Kaggle, PBS, the State Bank, WHO, your FYP data.
2. Audit it with `tslib.audit_index()` and report what you found.
3. Build three panels: the series with the aspect ratio **banked to 45°**
   and the number stated; a **cycle plot**; and the **residuals of an
   additive and a multiplicative decomposition** side by side.
4. Answer the question in two sentences, with the number that settles it.

Results that disagree with the textbook score full marks when they are
reported honestly and explained.

---

## What you hand in

One ZIP on the LMS, named `W4_<RollNo>.zip`:

```
partA_charts.py            rebuilds all nine, and plots your nine redesigns
partA_diagnosis.pdf        your nine diagnoses, with both figures per case
partB_windows.py           + its printed output
partC_shares.py            + pie_ranking_results.csv and the two stimuli
partD_figure.py            the script
partD_figure.png           the exported 300 dpi figure
partE_justification.pdf    one page
partF_cycle.py             (bonus, optional) + partF_cycle.png + the source
```

Cite your sources. All data in this folder is synthetic and generated for
CDB601220 — say so if you quote a number from it.

---

## Marking guide

| | Weight |
|---|---|
| Part A — mechanisms named and proved from the data, not objections asserted | 36% |
| Part B — the three decisions computed, not eyeballed | 15% |
| Part C — legality tested, the experiment genuinely run, limits stated | 9% |
| Part D — the figure runs, the six faults are handled, four panels earn their place | 25% |
| Part E — parameters, exclusions and the window choice all declared | 15% |

**Automatic deductions:**

- a smoothed line with no window length stated on the figure
- a rolling mean computed on an irregular or unsorted index
- a level resampled with `sum()`, or a flow resampled with `last()`
- missing periods silently filled, or interpolated without being marked
- a partial final period shown unmarked
- a pie or treemap of parts that do not sum to the whole
- negative values drawn as area, or dropped without being reported
- an `Other` bucket whose count and value are not declared
- a dual y-axis, or a truncated bar baseline
- `plt.plot()` / `plt.bar()` instead of `ax` methods
- a required export saved at less than 300 dpi
- invented or implausible experiment results in Part C
- a start date or window chosen after seeing the result and not declared

---

## Readings

- **Wilke**, *Fundamentals of Data Visualization* — Ch. 13 (time series),
  Ch. 10 (proportions), Ch. 11 (nested proportions). Free online.
- **pandas user guide — Time series / date functionality.** Read the
  `resample` and `rolling` tables; they answer most questions in Part B.
- **Cleveland, W. S. & McGill, R. (1984)**, "Graphical Perception",
  *JASA* 79(387), 531–554. The experiment behind the channel ranking you
  are now using for the third week running.
- **Cleveland, W. S. (1993)**, *Visualizing Data* — the banking-to-45°
  rule behind `tslib.banked_figsize()`.
- **Munzner**, *Visualization Analysis and Design*, Ch. 9 and the treemap
  discussion in Ch. 12 — the containment idiom for hierarchies.
- **Shneiderman, B. (1992)**, "Tree visualization with tree-maps". Four
  pages, and it is where treemaps come from.
