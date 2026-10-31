# Week 6 — Class Task: the integration checkpoint

**One lab session. Three tasks. Marked out of 25.**

No new idea is introduced this week. Weeks 1–5 arrive together, on one
dataset, and two things are being marked:

1. **How you process data** — what you check before you believe a column.
2. **How you visualize it** — what you decide, and whether you declared it.

| | Marks |
|---|---|
| **Setup & hygiene** | 5 |
| **Task A** — make the files trustworthy | 5 |
| **Task B** — three charts, three different questions | 5 |
| **Task C** — the figure the board will actually see | 5 |
| | **20** |
| **Task D** — *bonus, reported separately* | 5 |

Task D is marked out of 5 and reported separately. It is awarded only when
A, B and C are all at a passing standard, so finish those first.

---

## Why this brief is short

Every week so far has told you which chart to build, which column to
normalize and which window to use. This week it does not.

You choose the questions. You choose the chart types, the denominators, the
windows, the class breaks, the projection, the scaling, and which rows you
throw away. **The deciding is the thing being marked.**

The only rule about a decision is the one from Week 3, and it has not
changed: **anything you decide, declare on the figure or in your note.** A
parameter that changes the picture and is not written down is a deduction
whatever value you gave it.

> **There is no reader experiment this week.** Weeks 2 and 5 asked you to
> time a real person or run a two-map activity. This task does not. Nothing
> here needs another student, and nothing here is marked on what somebody
> else understood. Your work, your file, your session.

---

## Setup

Everything is in this folder. Nothing to download.

```bash
cd week6/assignments
python3 selfcheck.py       # confirms the toolkits and the data load
```

You should get library versions, the columns of all three CSVs, 24 GeoJSON
features, a five-class Jenks map and a 300 dpi PNG. If that runs, everything
below will.

**Requirements:** Python 3.9+, and:

```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels squarify
```

`statsmodels` is only needed if you decompose a series; `squarify` only if
you draw a treemap with `tslib.treemap()`.

| Path | What it is |
|---|---|
| `vizlib.py` | **Week 3's toolkit, unchanged** — palette, `lie_factor()`, `simulate_cvd()`, `save_fig()` |
| `tslib.py` | **Week 4's, unchanged** — `audit_index()`, `window_report()`, `exclusivity_check()`, `rollup_other()`, `treemap`, `cycle_plot` |
| `geolib.py` | **Week 5's, unchanged** — projections, Jenks `breaks()`, `choropleth`, `prop_symbols`, `pcp`, `funnel_limits` |
| `data/` | Three CSVs and one GeoJSON |
| `data/DATA_DICTIONARY.md` | What the columns **mean** and what unit they are in |

Nothing new was written for this week on purpose. You already have the
tools; the point is whether you reach for the right one unprompted.
`tslib.audit_index()` will do most of the daily file's audit in one call,
once you have given it an index it can read. Week 4's exclusivity test — do
the parts sum to the whole, and is every unit in exactly one part? — is the
generation file's audit, but that one you write yourself.

> `python3 tslib.py` and `python3 geolib.py` still self-test, but their demo
> blocks look for the Week 4 and Week 5 data folders. Run them from those
> weeks. Here, run `selfcheck.py`.

---

## The case

You work for the federation's **National Grid Authority**. The board meets
next week to split a reliability budget across 24 districts, and the
communications office wants a line about rooftop solar for the same meeting.

Three files land on your desk: the district register, seventeen months of
daily returns from six supply zones, and eighteen months of published
generation mix. Nobody has checked any of them.

The board has asked two questions and will accept one figure:

- **Where is supply least reliable?** Not where are there most interruptions
  — where is service worst.
- **Is the shift to renewables real, or is it arithmetic?**

---

## Before you plot anything

The three CSVs carry **eleven kinds of deliberate defect**: four in the
district register, six in the daily returns, one in the generation file. The
counts are published. The list is not — finding them is Task A, and it is
the half of this task where most marks are lost.

Counts of *kinds*, not of rows: one of the eleven affects a single district,
another affects a hundred and twenty-eight zone-days. The table at the end
of Task A tells you when you have found them all.

Two things worth knowing:

- `district_grid.csv` is 25 rows. It is short enough to read, and some of
  its defects can be found by reading it.
- `grid_daily.csv` is three thousand rows in no particular order. None of
  its defects can be found by reading it. Every one of them is found by
  computing something.

None of the eleven is exotic. Each one is a mechanism you were shown in
Weeks 3, 4 or 5, which is why they are not listed.

---

## Task A · Make the files trustworthy  (5 marks)

Write **one script** that reads the three raw CSVs and the GeoJSON, audits
them, fixes what it finds, and writes cleaned copies to `clean/`.

What is marked:

| | |
|---|---|
| The script runs top to bottom on the raw files, with no hand-edited CSV anywhere in your submission | 1 |
| An audit is **printed** — per file: dtypes, key uniqueness, duplicate keys, calendar gaps, sentinel values, join misses, and the ranges of anything you will divide by | 1 |
| Defects found, and the fixes are correct | 2 |
| A decisions table: one row per decision, with **what**, **how you detected it**, **the rule you applied**, and **the number of rows affected** | 1 |

The decisions table is the deliverable the marker reads first. Four columns,
one row per decision, as `partA_decisions.md` or printed by the script —
either is fine. A fix with no rule behind it ("looked wrong, dropped it") is
not a decision, it is an edit.

Two things to be careful about, because they are judgement and not
arithmetic:

- **Dropping a row and repairing a row are different claims.** Repair when
  you can state the true value and why; drop when you cannot. Say which you
  did and count them.
- **Missing is not zero, and a code is not a value.** If a field carries an
  operator's not-available code, it is missing data, and the chart has to
  say so — Week 1's last rule.

### If your processing is right, these come out

Every number below was recomputed from the committed files. They confirm the
clean; they do not tell you what was wrong.

| Check | Expected |
|---|---|
| Rows in the cleaned district register | **24**, one per `code` |
| Population / households across the 24 | **57,857,000** / **8,908,512** |
| Persons per household, min–max | **5.70 – 7.36**. Any district outside that range is still broken |
| `electrification_pct` after parsing | numeric, **66.6 – 90.3**, with **3** genuinely missing |
| Districts with a usable `outage_minutes` | **22** of 24, mean interruption **77 – 214** minutes |
| Interruptions, all districts | **388,879** |
| Zone-days kept in the daily file | **3,046** |
| Reporting span | **2025-04-01 → 2026-09-11** = 529 days × 6 zones = **3,174** slots |
| Zone-days never reported | **128** (and they are not evenly spread) |
| Unusable `peak_load_mw` readings | **46** |
| Zone-days where the meter reading goes **down** | exactly **1** |
| Energy delivered in zone **P1**, June 2026 | **1,200,239 MWh** |
| … the same month, if you `sum()` the column instead | **574,845,315 MWh** — **479×** too big |
| Rows in the generation file that are **parts** | **144** = 18 months × 8 categories |
| Parts summed against the published total | agree to within **2 MWh** in every month |
| Every row in the file summed | exactly **200.0%** of the energy generated |
| GeoJSON features joined to districts | **24** matched, **0** unmatched |

---

## Task B · Three charts, three different questions  (5 marks)

Three charts from your cleaned data, answering **three different kinds of
question**. Week 1's table is the list of kinds — comparison, trend,
distribution, relationship, composition, hierarchy — and you pick which
three.

Two constraints, and they are the only ones:

- At least one chart uses `grid_daily.csv`, so a **time axis** is marked.
- At least one chart uses `generation_mix.csv`, so a **part-to-whole or
  hierarchy** is marked.

Everything else is your call: which zone, which months, which window, which
aggregation, whether you facet, whether you show one series or six.

Each chart carries a one-line caption saying **what decision it supports**.
A chart that supports no decision is decoration, however good it looks.

| | |
|---|---|
| Three different question types, and the chart type fits each | 2 |
| The craft rules hold — finding in the title, zero baseline on bars, no second y-axis, colour that means something, selective labels, source note | 2 |
| Every parameter that changed the picture is declared on the figure: the aggregation, the window, the period, any `Other` bucket, anything excluded | 1 |

### Two anchors for the generation file

| Check | Expected |
|---|---|
| Generation, 2025-04 → 2026-09 | **−5.0%** |
| Solar, over the same months | **+82.1% in MWh**, and **4.1% → 7.9% of the mix** |

Both of those are true at once. Which of them your chart says is your
decision, and the board is going to read whichever one you draw.

---

## Task C · The figure the board will actually see  (5 marks)

**One** figure, one message, for one named reader, answering the board's
first question: *where is supply least reliable?*

You decide what the figure is. A normalized choropleth, a proportional
symbol map, a map beside a sorted bar chart, a bubble chart of four
variables, a parallel coordinates plot with one district brushed — all of
these can earn full marks, and so can a combination. What cannot earn marks
is a figure that leaves the reader to do the arithmetic.

Whatever quantity you encode, the figure must state **what it is per**.

Alongside it, **half a page** — `partC_note.md`:

| | |
|---|---|
| The figure runs from a script and exports at 300 dpi with a source note | 1 |
| The quantity is normalized, and the denominator is named **in words** in the legend or axis title | 1 |
| The message in one sentence, and the reader it is for | 1 |
| Your parameters, each with a reason: the denominator, and whichever of class breaks / scheme / projection / scaling / axis order / window your figure used | 1 |
| **The counterfactual** — what the raw-count version of this figure would have shown instead, and **which districts it would have pointed at** | 1 |

### Anchors for the reliability question

| Check | Expected |
|---|---|
| r(interruptions, households) across the 24 districts | **+0.991** |
| r(interruptions per 1,000 households, households) | **+0.175** |
| Top 3 districts by **count** | **D17, D13, D24** |
| Top 3 by **rate per 1,000 households** | **D12, D11, D13** |
| Districts on both lists | **1** — and the reason it is on both is the finding |
| National pooled rate | **43.7** interruptions per 1,000 households |
| The 5 most populous districts | **12.6%** of the land, **59.9%** of the people |

The last row is Week 5's warning, unchanged: a choropleth gives the people
in those five districts a twelfth of the ink.

### The ethics clause

A raw-count map of outages, like a raw-count map of disease or crime, names
the largest city every time. You are splitting a budget with this figure. If
the count map sends the money to the biggest districts and the rate map
sends it somewhere else, say so in the note, and say which districts the
first version would have taken money **away** from.

If you suppressed or merged any district because its numbers were too small
or too uncertain to publish, say which, say the rule, and say the count.
`geolib.funnel_limits()` is there if you want to argue it with a number.

---

## Task D · Bonus  (5 marks, reported separately)

Pick **one**.

**D1 — Make it interactive.** Rebuild one of your Task B charts in Plotly so
the reader can hover a value, filter a category or zoom a date range. Say in
one sentence what the interaction lets a reader do that your static version
cannot — and in a second sentence, what it lets them do that you would
rather they did not.

**D2 — Do it again on real data.** Find a real dataset with a date column or
a geographic key — World Bank, WHO, NEPRA, the Pakistan Bureau of
Statistics, a state electricity board, your FYP data — and run the same
pipeline: audit, clean, decisions table, one figure. Cite the source and the
date you downloaded it. One defect you found in the real file, named, is
worth more than a pretty chart.

| | |
|---|---|
| It works, and it is your own | 3 |
| The one-sentence justification, or the citation and the named defect | 2 |

---

## Setup & hygiene  (5 marks)

Marked, not awarded. These were warned about in writing after Week 2.

| | |
|---|---|
| The submitted folder has the structure below, with the names below | 1 |
| Every script runs from a clean checkout of your folder, with no absolute path from your machine in it | 1 |
| `requirements.txt` or a line in the README naming the libraries and versions you used | 1 |
| A `README.md` of ten lines: what you ran, in what order, and what it writes | 1 |
| Cleaned data is **written by your script**, never edited by hand, and the raw files are unmodified | 1 |

---

## What you hand in

One ZIP, uploaded before the end of the session.

```
README.md                 ten lines: what to run, in what order
requirements.txt          or the same information in the README
partA_process.py          raw -> audit -> clean/
partA_audit.txt           the printed audit
partA_decisions.md        what, how detected, rule, rows affected
clean/                    written by partA_process.py
partB_charts.py           + partB_1.png  partB_2.png  partB_3.png
partC_figure.py           + partC_figure.png
partC_note.md             half a page
partD_*                   bonus, optional
```

Do not re-commit the files in `data/` — they are unchanged, and that is the
point. All data in this folder is synthetic and generated for CDB601220.

---

## Automatic deductions

Carried forward, and all of them have been on a brief before:

- a hand-edited CSV, or a cleaning step done outside the script
- a row dropped with no rule and no count
- a date column sorted or plotted as text
- a series plotted against row number, so unreported days vanish
- a **level or a counter** summed, resampled with `sum()`, or averaged across
  a gap as if the gap were not there
- an operator code (`-1`, `999`, `N/A`) treated as a number
- a partial final period drawn at the same visual weight as a complete one
- parts that are not mutually exclusive drawn as one whole
- a share quoted without the direction of its total
- a count mapped to colour over an area, or a legend title with no
  denominator
- class breaks not printed, or a rainbow colormap for a quantity
- an area, a distance or a density computed in degrees
- a value driving a mark's radius instead of its area, or a size channel with
  no legend
- a truncated bar axis, a second y-axis, or a palette that fails
  `vizlib.cvd_report()`
- `plt.plot()` / `plt.scatter()` instead of `ax` methods
- an export below 300 dpi, or a figure with no source note
- a join whose unmatched rows were never counted
- any parameter that changed the picture and was not declared

---

## Readings

Nothing new. If you are stuck, the section you want is one of:

- **Wilke**, *Fundamentals of Data Visualization* — Ch. 29, "Telling a story
  and making a point". The whole of Task C is this chapter.
- **Week 4's `tslib` docstrings** — `audit_index`, `window_report` and
  `exclusivity_check` are each three lines of reading and most of Task A.
- **Week 5's `TASKS.md`, Part D3** — the six-step recipe for a normalized
  map, if that is the route you pick for Task C.
- **Tufte**, *The Visual Display of Quantitative Information* — Ch. 2 on
  graphical integrity, for the counterfactual paragraph.
