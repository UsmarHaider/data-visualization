# Week 7 — The dashboard: one screen, six weeks

**Five parts. Marked out of 25.**

Week 6 asked for **one figure** for one reader. This week asks for **one
screen** for a reader who can touch it — and a screen is not a figure with
more charts on it. It is a set of panels a stranger will read in an order
you chose, filter in a way you allowed, and quote out of context on Monday.

Everything from Weeks 1–6 is in scope and nothing new is being taught except
the three things that only go wrong once there is more than one panel and a
control:

1. **The aggregate moves the other way.** A headline that improves while
   every group inside it gets worse. The default view of a dashboard is the
   aggregate, so this is the error a reader cannot see by looking.
2. **The filter double counts.** A unit in two categories is counted in
   both, so the filtered views add to more than the whole.
3. **The drill-down does not reconcile.** Children that do not sum to their
   parent, found by the first reader who clicks.

| | Marks |
|---|---|
| **Setup & hygiene** | 2 |
| **Task A** — make the four files trustworthy | 4 |
| **Task B** — the static spine: four charts, four questions | 4 |
| **Task C** — make one of them interactive, and write the contract | 4 |
| **Task D** — the one screen | 4 |
| **Task E** — the note | 2 |
| | **20** |
| **Task F** — *bonus, reported separately* | 5 |

Task F is marked out of 5 and reported separately. It is awarded only when
A–E are all at a passing standard, so finish those first.

---

## Where every week returns

This is the integration week, so nothing here is new for its own sake. Each
row is an idea you have already been marked on, and where it is marked again.

| From | The idea | Where it lands this week |
|---|---|---|
| **W1** | The question chooses the chart | Task B — four questions of four different kinds |
| **W1** | Title the finding, not the subject | Task D — the *screen* gets a headline, not just the panels |
| **W1** | Missing is not zero | Task A — the codes, and the days nobody filed |
| **W2** | Preattentive channels, ranked | Task D — the channel plan: one meaning per channel, across the whole screen |
| **W2** | Redundant coding | Task D — identity never by colour alone, on a screen read by someone with deuteranopia |
| **W3** | Declare every parameter | All of it. Still the only rule that cannot be argued with |
| **W3** | A chart can be arithmetically right and still wrong | Task D — the headline that rises while every mode falls |
| **W3** | `vizlib.cvd_report()` | Task D — the palette is checked, not trusted |
| **W4** | Level vs flow; a mean of rates is not a rate | Task A — punctuality is a ratio of two counts |
| **W4** | Windows, partial periods, gaps that are not zeros | Task A and Task B |
| **W4** | Exclusivity before any part-to-whole | Task A and Task C — now as a *filter*, which is where it actually bites |
| **W4** | Hierarchies | Task B — the fare table is a two-level hierarchy |
| **W5** | The channel budget, spent in the reader's order | Task B and Task D |
| **W5** | Normalize, and name the denominator in words | Task B's map, Task E's counterfactual |
| **W5** | A count map is a population map | Task E — and here it is **+0.945** |
| **W6** | Audit before you believe a column | Task A, again, on four files instead of three |
| **W6** | Anything you decide, declare | Everywhere |

---

## Setup

Everything is in this folder. Nothing to download.

```bash
cd week7/assignments
python3 selfcheck.py       # confirms the toolkits and the data load
python3 dashlib.py         # self-tests this week's new toolkit
```

**Requirements:** Python 3.9+, and:

```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels squarify
pip install plotly          # OPTIONAL — see Task C
```

| Path | What it is |
|---|---|
| `vizlib.py` | **Week 3's, unchanged** — palette, `lie_factor()`, `simulate_cvd()`, `cvd_report()`, `save_fig()` |
| `tslib.py` | **Week 4's, unchanged** — `audit_index()`, `window_report()`, `exclusivity_check()`, `rollup_other()`, `treemap`, `cycle_plot` |
| `geolib.py` | **Week 5's, unchanged** — projections, Jenks `breaks()`, `choropleth`, `prop_symbols`, `pcp`, `funnel_limits` |
| `dashlib.py` | **New this week**, built on `vizlib` the same way the other two are |
| `data/` | Four CSVs and one GeoJSON |
| `data/DATA_DICTIONARY.md` | What the columns **mean** and what unit they are in |

### What is new in `dashlib`

Four checks and four drawing helpers. Read the docstrings; they are three
lines each and they are most of Tasks C and D.

| Function | What it does |
|---|---|
| `rate_decomposition(...)` | Splits a change in a headline rate into the **within-group** part and the **mix** part. Exact: the two sum to the change. Sets `reversal=True` when the aggregate moved one way and every group moved the other |
| `overlap_factor(...)` | Does summing by category double count? Week 4's exclusivity test, for a filter |
| `drilldown_check(...)` | Do the children sum to the parent, and is a published total hiding among the parts? |
| `channel_conflicts(...)` | One meaning per channel, across the whole screen. Positional channels are reported, not flagged |
| `dashboard_grid(...)` | A named panel grid with a headline band |
| `kpi_tile(...)` | One number, said once — with an arrow and a sign, never colour alone |
| `callout(...)` | An annotation with a leader line and a halo |
| `shared_scale(...)` | One scale across small multiples, and the sentence that says so |
| `LinkedBrush` / `select_in_rect(...)` | Brushing in plain matplotlib — no browser, no install. `simulate()` runs a selection with no event loop, which is how you test one |

---

## The case

You work for the federation's **Federal Transit Authority**. Four files land
on your desk — a district register, the route table, eighteen months of
daily control-room returns, and the ministry's published fare table. Nobody
has checked any of them.

The Authority's board has put a single screen on the agenda for next month
and three people will read it:

- The **Secretary**, who has thirty seconds and will read the top-left panel
  and nothing else.
- The **finance director**, who will filter to one mode and screenshot it.
- A **journalist**, who was sent the link by someone on the board.

The questions on the agenda are:

- **Is service getting better or worse?** The Authority's published headline
  says punctuality is improving.
- **Where should the next corridor go?** Four districts have asked.
- **Is the fare box recovering?** Revenue is up; the finance director wants
  to know whether that is ridership or fares.

---

## Before you plot anything

The four CSVs carry **fourteen kinds of deliberate defect**: five in the
district register, three in the route table, five in the daily returns, one
in the fare table. The counts are published. The list is not — finding them
is Task A, and it is where most marks are lost.

Counts of *kinds*, not of rows: one of the fourteen affects two rows,
another affects three hundred and eighty-five.

Three things worth knowing:

- `district_transit.csv` is 25 rows. It is short enough to read, and some of
  its defects can be found by reading it.
- `routes.csv` is 36 rows, and one of its defects is visible in a
  `value_counts()`.
- `ridership_daily.csv` is two thousand rows in no particular order. None of
  its defects can be found by reading it. Every one is found by computing
  something.

None of the fourteen is exotic. Each is a mechanism from Weeks 3, 4, 5 or 6,
which is why they are not listed. Four of them are mechanisms you have met
twice already.

---

## Task A · Make the four files trustworthy  (4 marks)

Write **one script** that reads the four raw CSVs and the GeoJSON, audits
them, fixes what it finds, and writes cleaned copies to `clean/`.

| | |
|---|---|
| The script runs top to bottom on the raw files, with no hand-edited CSV anywhere in your submission | 1 |
| An audit is **printed** — per file: dtypes, key uniqueness, duplicates, calendar gaps, impossible values, join misses, and the range of anything you will divide by | 1 |
| Defects found, and the fixes are correct | 1 |
| A decisions table: one row per decision, with **what**, **how you detected it**, **the rule you applied**, and **the number of rows affected** | 1 |

The decisions table is the deliverable the marker reads first. Four columns,
one row per decision, as `partA_decisions.md` or printed by the script. A fix
with no rule behind it ("looked wrong, dropped it") is not a decision, it is
an edit.

Three things that are judgement, not arithmetic:

- **Dropping a row and repairing a row are different claims.** Repair when
  you can state the true value and why; drop when you cannot. Say which, and
  count them.
- **A row that is not wrong can still not belong.** Some rows are perfectly
  accurate and still must not be in the sum. Deciding that is your job, and
  the rule you write down is the mark.
- **Two files disagreeing is a finding, not an error to smooth over.** When
  a total computed one way does not match the same total computed another
  way, the difference is a number with a meaning. Report it.

### If your processing is right, these come out

Every number below was recomputed from the committed files. They confirm the
clean; they do not tell you what was wrong.

**The district register**

| Check | Expected |
|---|---|
| Rows in, rows out | **25** in, **24** out, one per `code` |
| GeoJSON features matched on the register's key, as filed / after repair | **22** / **24** of 24 |
| Population / households across the 24 | **57,857,000** / **8,908,512** |
| Population if the extra register row is kept | **60,747,000** — which is not the federation's population |
| `boardings_annual` before repair | **3** districts read as **under 1 boarding per resident per year** |
| `boardings_annual` after repair, all 24 | **873,564,130** |
| Boardings per 1,000 residents | **4,683 – 30,655**, national pooled **15,099** |
| `fare_concession_pct` after repair | **20.9 – 42.6**, with **4** rows repaired |
| `road_km` usable | **22** of 24 |

**The route table**

| Check | Expected |
|---|---|
| Rows / distinct `mode` labels as filed / after repair | **36** / **6** / **4** |
| Routes per mode after repair | Bus **22**, BRT **6**, Metro **4**, Ferry **4** |
| `punctuality_pct` usable | **33** of 36, range **62.9 – 98.8** |
| `cost_recovery_pct` rows that are a code, not a measurement | **2** |
| `boardings_annual` summed over routes | **873,564,820** — the register and the route table agree to within **700 boardings** |
| The same figure, attributed to every district each route serves | **2,704,739,571** = **3.096×** the network total |
| Routes serving more than one district | **28** of 36; mean **2.56**, max **4** |

**The daily returns**

| Check | Expected |
|---|---|
| Rows as filed | **2,159** |
| Rows whose `date` is not in the file's main format | **385** |
| … of those, rows that **fail** a month-first parse | **230** |
| … and rows a month-first parse would **silently accept as a different day** | **155** |
| Rows that are an exact re-submission | **30**, all one mode, all one month |
| Rows after de-duplication | **2,129** |
| Rows describing something that cannot happen | **7** |
| Reporting span | **2025-04-01 → 2026-09-30** = 548 days × 4 modes = **2,192** slots |
| Slots nobody ever filed | **63**, and they are **not** evenly spread: Ferry **22**, Bus **19**, Metro **18**, BRT **4** |
| The longest single gap | **14 consecutive days**, one mode, **2026-02-09 → 2026-02-22** |
| Slots filed from **2026-09-22** onward | **18** of 36 — two modes stopped filing |
| Boardings, 12 months to 2026-08-31 | **845,531,940** |
| … the same figure with the re-submitted rows left in | **864,127,819**, **+2.20%** |
| … that month for that mode, with and without | exactly **2.00×** |
| The register's annual total vs what the returns actually account for | **873,564,130** vs **845,531,940** — the returns cover **96.8%**, and the missing **3.2%** is the days nobody filed |

**The fare table**

| Check | Expected |
|---|---|
| Rows | **288** = **216** parts + **72** that are not parts |
| Summing **every** row | exactly **200.0%** of the journeys and of the revenue |
| Parts checked against the published summary | agree **exactly**, every month, every mode |
| Journeys and revenue over the 18 months | **934,051,014** journeys, **36,669,953,119 PKR** |
| Mean fare per journey | **39.3 PKR** |
| Boardings ÷ journeys, over the whole file | **1.30** — 1.301 to 1.305, depending on whether you drop or repair the seven impossible rows |

That last number is the one to hold on to: **every 1,000 journeys produce
about 1,300 boardings**, because people change vehicles. It is why the two
`boardings_annual` columns and the fare table's `trips` column can never be
put on the same axis.

---

## Task B · The static spine  (4 marks)

**Four charts**, each answering a different kind of question from Week 1's
table — comparison, trend, distribution, relationship, composition,
hierarchy. You pick which four, with three constraints:

- One uses `ridership_daily.csv`, so a **time axis** is marked.
- One uses `fare_revenue.csv` as a **part-to-whole or a hierarchy**.
- One is a **map**, normalized, with the denominator named in words.

Everything else is yours: which mode, which months, which window, which
aggregation, whether you facet, whether you draw one series or four.

Each chart carries a one-line caption saying **what decision it supports**. A
chart that supports no decision is decoration, however good it looks.

| | |
|---|---|
| Four different question types, and the chart type fits each | 1 |
| The craft rules hold — finding in the title, zero baseline on bars, no second y-axis, colour that means something, selective labels, source note, 300 dpi | 1 |
| The map is normalized and its denominator is named in words | 1 |
| Every parameter that changed the picture is declared on the figure: the aggregation, the window, the period, any `Other` bucket, anything excluded | 1 |

### Anchors for the fare file

Over the **complete** months 2025-04 → 2026-08:

| Check | Expected |
|---|---|
| Journeys | **+12.1%** |
| Revenue | **+26.9%** |
| Metro journeys | **+99.5%**, share of journeys **27.8% → 49.4%** |
| Bus journeys | **−39.1%**, share **43.3% → 23.5%** |
| BRT / Ferry journeys | **+8.3%** / **−23.4%** |
| Share of journeys in 2026-08 | Metro **49.4%**, BRT **24.9%**, Bus **23.5%**, Ferry **2.2%** |
| Share of **revenue** in the same month | Metro **58.8%**, BRT **22.9%**, Bus **14.8%**, Ferry **3.4%** |

The last two rows are the same month, the same four modes, and two different
pictures — because a metro journey earns **48.3 PKR** and a bus journey earns
**26.1**. Whichever of them you draw is what the finance director will quote.
Say which one you drew and why, in the caption.

Note also that revenue grew more than twice as fast as journeys. That has
exactly two possible explanations and your data can tell them apart.

---

## Task C · Make it interactive, and write the contract  (4 marks)

Take **one** of your Task B charts and make it interactive. Then write down
what you have let the reader do.

**Either toolchain earns full marks:**

- **Plotly**, if you have it — hover, legend filtering, a date-range zoom.
- **Matplotlib**, if you do not — `dashlib.LinkedBrush` links a selection in
  one panel to highlighting in another, in a notebook with
  `%matplotlib widget` or in any interactive window. Nothing here needs an
  install, which is the point: it is the same reason `tslib` shipped its own
  treemap and `geolib` needs no GIS stack.

Submit a script or notebook that produces the interactive view, **plus a
static PNG of its default state** — a marker with no mouse must still be able
to see what a reader sees first.

### The interaction contract — `partC_contract.md`, half a page

| | |
|---|---|
| The interactive view works, from a script, on a clean checkout | 1 |
| **The default state.** What the view says before anybody touches it, in one sentence — because most readers never touch it | 1 |
| **The controls.** Each one: what it changes, what it does *not* change, and whether the reader can get back. A filter with no reset is a trap | 1 |
| **The thing the control must not invite.** Name one wrong conclusion your interaction makes easy, and say what you did about it | 1 |

That last mark is the week in one box. An interaction is an *argument you let
the reader make for themselves* — so you are responsible for the arguments it
makes easy, not only for the one you intended.

Two that are already in this data:

- A filter on `mode` or on `districts_served` invites the reader to add the
  filtered views up. `dashlib.overlap_factor()` gives you the number that
  says what happens if they do — **3.096×**, in this file. If your control
  can double count, the caption has to say so, or the control must not exist.
- A date-range zoom invites the reader to zoom to a window you never looked
  at — including one ending inside the partial final period, and one sitting
  on top of a 14-day gap. Decide what your view does there: grey it, cut it,
  or label it. "The reader chose that window" is not an answer; you built the
  control.

---

## Task D · The one screen  (4 marks)

One figure, **3–6 panels**, exported at 300 dpi, for the three readers named
in the case. `dashlib.dashboard_grid()` lays it out and gives you a headline
band; you decide what goes in which cell and in what order it is read.

| | |
|---|---|
| The **screen** has a headline that states a finding, and a standfirst naming the period, the unit (boardings or journeys) and the denominator | 1 |
| The panels answer the board's questions, in a reading order you can defend in one sentence | 1 |
| **The channel plan** — submit the `channel_conflicts()` output as part of your audit, with no conflicts, and a `cvd_report()` on the palette you actually used | 1 |
| **The reversal is on the screen.** Whatever your headline number is, the panel beside it shows whether it is real | 1 |

### The anchor this part is built on

The Authority's published headline is that punctuality is improving. Over
the two complete quarters **2025 Q2 → 2026 Q2**:

| | 2025 Q2 | 2026 Q2 | Change |
|---|---|---|---|
| **Network on-time** | **78.87%** | **80.60%** | **+1.73 pts** |
| Metro | 96.11% | 94.80% | **−1.31** |
| BRT | 88.09% | 87.24% | **−0.85** |
| Bus | 74.24% | 73.14% | **−1.10** |
| Ferry | 80.97% | 79.78% | **−1.19** |

Every mode got worse. The network got better. Nothing is wrong with any of
those six numbers.

`dashlib.rate_decomposition()` splits it: **within −1.10 points**, **mix
+2.82 points**. The mix moved because Metro went from **10.9%** of departures
to **21.8%** while Bus fell from **71.6%** to **57.6%** — and the metro is
punctual. The Authority did not get better at running buses. It ran fewer
buses.

This holds whichever sensible window you pick — first three complete months
against the last three gives **+2.02** points with all four modes down, first
six against last six gives **+1.52**. You do not have to use the quarters
above; you do have to say which window you used.

A screen whose headline tile says **▲ +1.73 pts** and stops is arithmetically
correct and will mislead all three of your readers. What you do about that is
the mark.

---

## Task E · The note  (2 marks)

Half a page, `partE_note.md`.

| | |
|---|---|
| The message in one sentence, the reader it is for, and your parameters each with a reason — the window, the unit, the denominator, the breaks, the projection, the aggregation | 1 |
| **The counterfactual and the ethics clause** (below) | 1 |

### The counterfactual

The board is choosing where the next corridor goes. Say what the **raw-count**
version of your map would have shown, and **which districts it would have
pointed at instead**.

| Check | Expected |
|---|---|
| r(boardings, population) across the 24 districts | **+0.945** |
| r(boardings per 1,000 residents, population) | **+0.249** |
| Top 3 by **count** | **D17, D09, D13** |
| Top 3 by **rate per 1,000 residents** | **D12, D21, D09** |
| Districts on both lists | **1** — and the reason it is on both is the finding |
| The 5 most populous districts | **12.6%** of the land, **59.9%** of the people |

A count map of boardings is a population map, as a count map of outages was
in Week 6 and a count map of disease was in Week 5. You are siting
infrastructure with this screen: if the count version sends the corridor to
the largest districts and the rate version sends it somewhere else, say so,
and say which districts the first version takes it away from.

If you suppressed or merged a district because its numbers were too small or
too uncertain to publish, say which, say the rule, and say the count.
`geolib.funnel_limits()` is there if you want to argue it with a number.

---

## Task F · Bonus  (5 marks, reported separately)

Pick **one**.

**F1 — Do it again on real data.** Find a real dataset with a date column and
a geographic or categorical key — a transit authority's open data, World
Bank, PBS, NEPRA, your FYP data — and run the same pipeline: audit, clean,
decisions table, one screen. Cite the source and the date you downloaded it.
One defect you found in the real file, named and evidenced, is worth more
than a pretty screen.

**F2 — Audit your own screen for a reader who is not you.** Run your Task D
figure through `vizlib.simulate_cvd()` on the rendered image, not just on the
hex codes. Then hand the static PNG to **five** people, give them twenty
seconds, and write down the one sentence each took away. Report all five,
including the ones who read it wrong, and say what you would change. Weeks 2
and 5 marked you on what a reader understood; this is that, on your own work.

| | |
|---|---|
| It works, and it is your own | 3 |
| The citation and the named defect, or the five readers' sentences and the change | 2 |

---

## Setup & hygiene  (2 marks)

| | |
|---|---|
| The submitted folder has the structure below, with the names below; every script runs from a clean checkout with no absolute path from your machine | 1 |
| `requirements.txt` naming the libraries and versions you used, and a `README.md` of ten lines: what you ran, in what order, and what it writes. Cleaned data is **written by your script**, never edited by hand, and the raw files are unmodified | 1 |

---

## What you hand in

One ZIP.

```
README.md                 ten lines: what to run, in what order
requirements.txt          the libraries and versions you used
partA_process.py          raw -> audit -> clean/
partA_audit.txt           the printed audit, including channel_conflicts() and cvd_report()
partA_decisions.md        what, how detected, rule, rows affected
clean/                    written by partA_process.py
partB_charts.py           + partB_1.png .. partB_4.png
partC_interactive.py      or .ipynb, + partC_default.png
partC_contract.md         half a page
partD_screen.py           + partD_screen.png
partE_note.md             half a page
partF_*                   bonus, optional
```

Do not re-commit the files in `data/` — they are unchanged, and that is the
point. All data in this folder is synthetic and generated for CDB601220.

---

## Automatic deductions

Everything on Week 6's list still applies. In full, and with this week's
additions at the bottom:

- a hand-edited CSV, or a cleaning step done outside the script
- a row dropped with no rule and no count
- a date column sorted or plotted as text, or parsed with a format that
  silently reinterprets part of the file
- a series plotted against row number, so unfiled days vanish
- a level or a counter summed, or a mean taken across a gap as though the
  gap were not there
- **a mean of percentages passed off as a rate**
- an operator code (`-1`, `999`, `0`, `N/A`) treated as a number
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
- **boardings and journeys added together, or drawn on one axis**
- **a filter that invites a sum the data does not support, with nothing said
  about it**
- **a control with no way back to the default view**
- **one visual channel carrying two different variables across the screen**
- **a headline number with no panel beside it saying whether it is real**

---

## Readings

- **Wilke**, *Fundamentals of Data Visualization* — Ch. 29 and Ch. 31, on
  telling a story and on compound figures. Task D is Ch. 31.
- **Few**, *Information Dashboard Design* — the first three chapters, for
  why a dashboard is a reading order and not a collection.
- **Dashlib's docstrings** — `rate_decomposition`, `overlap_factor` and
  `drilldown_check` are three lines each and are most of Tasks A, C and D.
- **Week 4's `TASKS.md`**, the exclusivity section, and **Week 5's Part D3**,
  the six-step recipe for a normalized map.
- **Tufte**, *The Visual Display of Quantitative Information* — Ch. 2, for
  the counterfactual paragraph.

---

## One sentence to leave with

A dashboard does not show the reader your conclusion; it hands them the
controls — so the only question that matters is what it lets them conclude
when you are not in the room.
