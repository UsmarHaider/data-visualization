# Week 6 — Class Task: the integration checkpoint

One dataset, one lab session, and everything from Weeks 1–5 at once.

← [Back to the course index](../README.md)

| | |
|---|---|
| **What it checks** | Whether a student can take an unchecked dataset, make it trustworthy, and turn it into a figure somebody can act on — **CLO1 + CLO2** |
| **Format** | In-class task, three tasks plus a bonus, marked out of 25 |
| **New material** | None. This is the checkpoint, not a new topic |

## The case

The federation's **National Grid Authority** is splitting a reliability
budget across 24 districts, and the communications office wants a line about
rooftop solar for the same board meeting.

Three files land on the student's desk — a district register, seventeen
months of daily returns from six supply zones, eighteen months of published
generation mix — and nobody has checked any of them. The board has asked
*where is supply least reliable* and *is the shift to renewables real*, and
will accept one figure.

## Contents

| Path | What it is |
|---|---|
| `assignments/TASKS.md` | Three tasks, a bonus, the hygiene marks and the deduction list |
| `assignments/selfcheck.py` | Thirty seconds to confirm the toolkits and the data load on this machine |
| `assignments/vizlib.py` | **Week 3's toolkit, unchanged** |
| `assignments/tslib.py` | **Week 4's, unchanged** |
| `assignments/geolib.py` | **Week 5's, unchanged** |
| `assignments/data/` | Three CSVs, one GeoJSON, and `DATA_DICTIONARY.md` |

Nothing new was written for this week on purpose. The three toolkits arrive
byte-identical to the weeks they came from, which is the point: the student
has the tools already, and what is being marked is whether they reach for
the right one unprompted.

## Assignments

| Task | Covers | Marks |
|---|---|---|
| Setup & hygiene | Structure, reproducibility, no hand-edited data | 5 |
| A | **Process** — audit, clean, and a decisions table with rules and counts | 5 |
| B | **Visualize** — three charts answering three different kinds of question | 5 |
| C | **Decide** — one figure for the board, normalized, with the counterfactual | 5 |
| D | *Bonus, reported separately* — make it interactive, or do it again on real data | 5 |

Full brief in [`assignments/TASKS.md`](assignments/TASKS.md).

## What makes this week different

**The brief does not say what to build.** Weeks 1–5 named the chart, the
denominator and the window. This one names the audience and the question and
stops. The student chooses the questions, the chart types, the denominators,
the windows, the breaks, the projection and the rows to discard — and the
deciding is what carries the marks. The one rule that survives is Week 3's:
anything you decide, declare.

**Processing is marked as heavily as drawing.** Task A is worth the same as
Task C. Every previous week handed over data that was wrong in a known way;
this one hands over data that is wrong in eleven ways at once, mixed
together, in files of three different shapes.

**There is no reader experiment.** Weeks 2 and 5 asked students to time a
real person or run a two-map activity on five readers. This task does not,
and nothing in it is marked on what another student understood. It is a
single-session, single-handed task.

## The datasets

Synthetic, fixed seed, generated for CDB601220. The geography is the **same
fictional federation as Week 5** — 24 districts over 66–74°E, 24–36°N —
with matching names, populations and areas, so anything built in Week 5
still joins.

| File | Rows | What it carries |
|---|---|---|
| `district_grid.csv` | 25 | 24 districts: population, households, income, electrification, rooftop solar, interruptions and interruption minutes |
| `grid_daily.csv` | 3,061 | Six supply zones × ~17 months of daily returns: a cumulative energy meter, a daily peak load, interruption minutes |
| `generation_mix.csv` | 162 | 18 months × a four-level-over-eight generation hierarchy, as the ministry publishes it |
| `regions.geojson` | 24 | The boundaries, plain GeoJSON — no `geopandas` needed |

The register is 25 rows for a reason, and `grid_daily.csv` is shuffled for a
reason. Neither reason is written down where a student can read it.

## Expected results

Recomputed from the committed files before this brief was written. The full
set, with the processing confirmations, is in `TASKS.md` beside the task it
belongs to.

| Check | Expected |
|---|---|
| Rows in the cleaned register / population / households | **24** / **57,857,000** / **8,908,512** |
| Persons per household after cleaning | **5.70 – 7.36** across all 24 |
| Zone-days kept, of 529 × 6 = 3,174 slots | **3,046**, with **128** never reported |
| Energy in P1, June 2026 — differenced vs summed | **1,200,239 MWh** vs **574,845,315 MWh** (**479×**) |
| Zone-days where the meter reading falls | **1** |
| Every row of the generation file summed | exactly **200.0%** of the energy generated |
| Generation 2025-04 → 2026-09, and solar over the same span | **−5.0%**, while solar runs **+82.1%** in MWh and **4.1% → 7.9%** of the mix |
| r(interruptions, households) | **+0.991** |
| r(interruptions per 1,000 households, households) | **+0.175** |
| Top 3 by count / by rate | D17, D13, D24 / D12, D11, D13 — **one** district on both |
| National pooled rate | **43.7** interruptions per 1,000 households |
| The 5 most populous districts | **12.6%** of the land, **59.9%** of the people |

The one district on both lists is the finding. It is there because of what
it earns, not because of how many people live in it, and a student who
reports the overlap without saying why has done the arithmetic and stopped.

## Carried forward

Everything, which is the point. The three load-bearing ideas:

- **Week 4's denominator lesson** — "per what?" is a modelling decision, not
  a formatting one. It is the whole of Task C, and the count map and the
  rate map send the budget to different districts.
- **Week 4's level-versus-flow distinction** — the daily file ships a
  *counter*, not a quantity. Summing it is wrong by 479×, and the error is
  invisible on the chart because the shape of the curve looks fine.
- **Week 3's declaration rule** — a parameter that changes the picture and
  is not written down is a deduction whatever value it was given. With no
  prescribed parameters this week, it is the only thing holding the
  decisions accountable.

## Teacher material

The generator, the defect list and the model answers are **not** in this
repository, and `.gitignore` blocks `*TEACHER*`, `*_KEY*`, `*ANSWER*`,
`solution/` and `make_task.py` from ever being committed here. The eleven
defects are recoverable from the Expected results table above, which is why
that table gives confirmations rather than mechanisms.

## One sentence to leave with

A figure is only as honest as the audit nobody will ever see — so do the
audit, write down what you decided, and say what your number is *per*.
