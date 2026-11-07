# Week 7 — The dashboard: one screen, six weeks

Weeks 1–6 arrive together again, on four unchecked files — and this time the
reader can touch the result.

← [Back to the course index](../README.md)

| | |
|---|---|
| **What it checks** | Whether a student can turn four unchecked files into one screen that a stranger can filter without being misled — **CLO1 + CLO2** |
| **Format** | Five parts plus a bonus, marked out of 25 |
| **New material** | Only what breaks once there is more than one panel and a control |

## The case

The Federal Transit Authority's board has put a single screen on next
month's agenda, and three people will read it: the Secretary, who has thirty
seconds and reads the top-left panel; the finance director, who will filter
to one mode and screenshot it; and a journalist, who was sent the link.

Four files land on the student's desk — a district register, the route
table, eighteen months of daily control-room returns, and the ministry's
published fare table. Nobody has checked any of them. The Authority's
published headline is that punctuality is improving.

## Contents

| Path | What it is |
|---|---|
| `assignments/TASKS.md` | Five parts, a bonus, the hygiene marks and the deduction list |
| `assignments/selfcheck.py` | Thirty seconds to confirm the toolkits and the data load on this machine |
| `assignments/dashlib.py` | **New this week** — the dashboard toolkit, built on `vizlib` |
| `assignments/vizlib.py` | **Week 3's, unchanged** |
| `assignments/tslib.py` | **Week 4's, unchanged** |
| `assignments/geolib.py` | **Week 5's, unchanged** |
| `assignments/data/` | Four CSVs, one GeoJSON, and `DATA_DICTIONARY.md` |

## Assignments

| Task | Covers | Marks |
|---|---|---|
| Setup & hygiene | Structure, reproducibility, no hand-edited data | 2 |
| A | **Process** — audit four files, clean them, and a decisions table | 4 |
| B | **The static spine** — four charts, four kinds of question, one of them a normalized map | 4 |
| C | **Interact** — one linked or filterable view, and the interaction contract | 4 |
| D | **The one screen** — headline, reading order, channel plan, and the reversal | 4 |
| E | **The note** — parameters, the counterfactual, the ethics clause | 2 |
| F | *Bonus, reported separately* — real data, or your own screen audited on five readers | 5 |

Full brief in [`assignments/TASKS.md`](assignments/TASKS.md).

## What makes this week different

**A screen is not a figure with more charts on it.** Week 6 asked for one
figure for one reader, and the student controlled everything the reader saw.
This week the reader has controls, and three of them are named in the brief
with different amounts of attention and different motives. What the screen
*allows* is marked as heavily as what it says.

**Three failures that need more than one panel to exist.** Everything
before this week could go wrong inside a single chart. These cannot:

1. **The aggregate moves the other way.** The default view of a dashboard is
   always the aggregate, so a headline that improves while every group
   inside it worsens is the one error a reader cannot see by looking.
2. **The filter double counts.** A route runs through four districts, so a
   by-district filter credits it four times. Each filtered view is right on
   its own; the reader who adds them up is not.
3. **The drill-down does not reconcile.** Children that do not sum to their
   parent, found by the first person who clicks.

**Interactivity is marked as an argument, not a feature.** Task C's fourth
mark is for naming one wrong conclusion the interaction makes easy, and
saying what was done about it. A control is an argument you let the reader
make for themselves, which makes you responsible for the ones it makes easy.

**Plotly is still optional.** `dashlib.LinkedBrush` links two panels in plain
matplotlib, and `simulate()` runs a selection with no event loop so a brush
can be tested headlessly. Nobody is blocked on an install — the same reason
`tslib` shipped its own treemap and `geolib` needs no GIS stack.

## The datasets

Synthetic, fixed seed, generated for CDB601220. The geography is the **same
fictional federation as Weeks 5 and 6** — 24 districts over 66–74°E,
24–36°N — with matching codes, names, populations and areas, and
`regions.geojson` is byte-identical to Week 6's, so anything built in those
weeks still joins.

| File | Rows | What it carries |
|---|---|---|
| `district_transit.csv` | 25 | The district register: population, households, stops, road length, attributed boardings, concession share, registered vehicles |
| `routes.csv` | 36 | The network: mode, corridor, length, fleet, the districts each route serves, boardings, punctuality, crowding, cost recovery |
| `ridership_daily.csv` | 2,159 | Four modes × ~18 months of control-room returns: departures scheduled, operated and on time, boardings, delay minutes |
| `fare_revenue.csv` | 288 | 18 months × four modes × the published fare products: journeys and revenue |
| `regions.geojson` | 24 | The boundaries, plain GeoJSON — no `geopandas` needed |

The register is 25 rows for a reason, the route table repeats district codes
for a reason, and the daily file is shuffled for a reason. None of those
reasons is written down where a student can read it.

**Fourteen kinds of defect** are spread across the four files — five, three,
five and one. The counts are published in `TASKS.md`; the list is not.

## The distinction the week turns on

**A boarding is not a journey.** A boarding is one person entering one
vehicle; a journey is one person getting where they were going, however many
vehicles that took. The daily returns and both `boardings_annual` columns
count boardings. The fare table counts journeys. Over this file the ratio is
**1.30** — every 1,000 journeys produce about 1,300 boardings — so the two
can never go on one axis. It is in the data dictionary, in those words, and it is
still the line most likely to be missed.

## Expected results

Recomputed from the committed files before the brief was written. The full
set, grouped by the task it belongs to, is in `TASKS.md`.

| Check | Expected |
|---|---|
| District register, rows in / out | **25** / **24** |
| Population / households | **57,857,000** / **8,908,512** |
| GeoJSON features matched on the register's key, as filed / after repair | **22** / **24** |
| Boardings attributed to districts, after repair | **873,564,130** |
| Route boardings summed | **873,564,820** — the two files agree to within **700** |
| … attributed to every district each route serves | **2,704,739,571** = **3.096×** |
| Daily rows in / after de-duplication | **2,159** / **2,129** |
| Slots nobody ever filed, of 548 days × 4 modes | **63**, worst a **14-day** block |
| Boardings, 12 months to 2026-08-31 | **845,531,940** — **96.8%** of what the register claims |
| Fare table, summing every row | exactly **200.0%** |
| Boardings ÷ journeys | **1.30** |
| **Network on-time, 2025 Q2 → 2026 Q2** | **78.87% → 80.60%**, **+1.73 pts** |
| **… while every one of the four modes falls** | −0.85 to −1.31 pts |
| … decomposed | within **−1.10** pts, mix **+2.82** pts |
| r(boardings, population) / r(rate, population) | **+0.945** / **+0.249** |
| Top 3 by count / by rate | D17, D09, D13 / D12, D21, D09 — **one** district on both |
| The 5 most populous districts | **12.6%** of the land, **59.9%** of the people |

The Authority did not get better at running buses. It ran fewer buses, and
the metro it ran instead is punctual. A student who reports the headline
without the decomposition has done the arithmetic and stopped.

## Carried forward

Everything, which is the point — `TASKS.md` opens with a table mapping every
Week 1–6 idea to the task where it returns. The three load-bearing ones:

- **Week 4's exclusivity test**, which stops being a check on a stacked bar
  and becomes a check on a *filter*. That is where it actually bites, and
  here it is worth **3.096×**.
- **Week 4's level-versus-flow care**, generalised: punctuality is a ratio of
  two counts, so a mean of daily percentages is not a punctuality rate.
- **Week 5 and 6's denominator lesson**, unchanged and still the ethics
  clause: a count map is a population map, and this one correlates with
  population at **+0.945**.

## Teacher material

The generator, the defect list and the model answers are **not** in this
repository, and `.gitignore` blocks `*TEACHER*`, `*_KEY*`, `*ANSWER*`,
`solution/` and `make_task.py` from ever being committed here. The fourteen
defects are recoverable from the Expected results table above, which is why
that table gives confirmations rather than mechanisms.

## One sentence to leave with

A dashboard does not show the reader your conclusion; it hands them the
controls — so the only question that matters is what it lets them conclude
when you are not in the room.
