# Week 5 — Multivariate Data & Geospatial Visualization

Datasets, toolkit and assignments for Week 5.

← [Back to the course index](../README.md)

| Lecture | Topic | Outcome | CLO | 3C |
|---|---|---|---|---|
| **L9** | More variables than axes — bubble charts, size, hue, shape, overplotting, SPLOM, parallel coordinates, PCA | Map high-dimensional datasets using multivariate encodings; implement parallel coordinates plots | CLO2 | Competence |
| **L10** | Putting data on a map — projections, choropleths, normalization, classification, MAUP, ethics | Construct thematic spatial visualizations and avoid population bias, boundary distortion and inappropriate colour scaling | CLO2 | Competence |

## The case

A global health organization is tracking a regional outbreak alongside four
socio-economic indicators: GDP per capita, healthcare access, urban density
and age distribution.

Separate two-variable charts mask the interactions between those indicators.
Worse, the regional map plots **raw case counts** — so every densely
populated district lights up, every week, whatever the actual risk.

You are the data visualizer. By the end of the week you produce three
figures from scripts that run the same way every time: a four-variable
bubble chart with a size legend that lets a reader convert area back into
people; a parallel coordinates plot whose scaling and axis order you chose
on purpose and wrote on the figure; and a **normalized** choropleth that
shows regional risk instead of showing where the people are.

Along the way you take apart **nine more charts that are wrong** — and this
time six of them would pass a design review.

No setup needed beyond the libraries; the data is already in
`assignments/data/`.

## Contents

| Path | What it is |
|---|---|
| `assignments/TASKS.md` | Five parts, a bonus, the rules and the marking guide |
| `assignments/vizlib.py` | **Week 3's toolkit, unchanged** — palette, Lie Factor, CVD simulation, `save_fig` |
| `assignments/geolib.py` | This week's toolkit, built on top of `vizlib` — **and it needs no GIS install** |
| `assignments/data/` | Seven tables, three GeoJSON boundary sets, and `DATA_DICTIONARY.md` |

> **You do not need `geopandas`.** Boundaries ship as plain GeoJSON, read
> with the standard-library `json` module, and `geolib` carries the
> projections, the classification schemes (including an exact Jenks) and the
> polygon drawing in about 300 lines. Every number in `TASKS.md` was produced
> with it. If you have `geopandas` and `mapclassify`, use them and say so.
>
> There are **no starter skeletons**, as from Week 4. The toolkit is the
> scaffolding — read `geolib.py` before you start, not after.
>
> Model answers are **not** in this repository. `.gitignore` blocks
> `*TEACHER*`, `*_KEY*`, `*ANSWER*` and `solution/` from ever being
> committed here.

## Assignments

| Part | Covers | Marks |
|---|---|---|
| A | Rebuild nine charts, then diagnose — conclusion, decoy, mechanism, redesign | 36 |
| B | The five channel and spatial decisions, computed rather than asserted | 15 |
| C | The two-map activity, run on at least five real readers | 9 |
| D | **Hands-on:** the three health figures, exported at 300 dpi | 25 |
| E | One page of written justification, including the counterfactual | 15 |
| F | *Bonus, marked separately* — a normalized map on data you find | 5 |

Full briefs in [`assignments/TASKS.md`](assignments/TASKS.md).

## What makes this week different

Week 3's nine broken charts were broken by a **drawing** decision — a bin
width, a truncated axis, a rainbow colormap. Week 4's nine were broken
**before any drawing happened** — a parse, a resample, a window, a
denominator.

Week 5's nine are broken by **the encoding or the geography**. The
arithmetic is right, the parse is right, the chart is carefully drawn, and
six of the nine are prettier than anything you will produce this term. The
lie is in which channel carried which variable, or in which boundaries were
used to carve the land up.

The nine mechanisms, one per deck idea:

| # | Mechanism | Slide |
|---|---|---|
| 1 | A value driving a mark's **radius** instead of its area | 10 |
| 2 | A raw-count choropleth, which is always a population map | 37 |
| 3 | Min–max scaling flattened by one outlier | 22 |
| 4 | A parallel coordinates axis order that separates the related pair | 24 |
| 5 | Five quantile classes painted over a 7% spread | 39 |
| 6 | A small-denominator rate read as a hotspot | 45 |
| 7 | A correlation quoted at the wrong areal scale | 44 |
| 8 | Area read as people — big districts owning the map | 46 |
| 9 | A radar chart whose enclosed area depends on axis order | 26 |

Each case carries a **self-check number** so you know your rebuild is
faithful before you start diagnosing it.

Two of the nine are not fixed by changing the chart type: the redesign is
the same chart with a different *decision* inside it.

## Carried forward

Nothing from Weeks 1–4 is retired, and `TASKS.md` opens with the table that
maps each idea to where it returns. The three load-bearing ones:

- **Week 2's channel ranking** (position > length > angle > area) stops
  being a ranking and becomes a **budget**: two positions, then area, then
  lightness, then hue, spent in the order the reader needs to compare.
- **Week 2's "experiments run on real readers"** returns as Part C. The
  two-map activity is a genuine reader experiment, and invented results
  still score zero.
- **Week 4's denominator lesson** — "per what?" is a modelling decision, not
  a formatting one — is now the single most load-bearing idea in the week.
  It is case 2, it is Part C, and it is 8 of Part D's 25 marks.

## The datasets

| File | Rows | What it carries |
|---|---|---|
| `health_indicators.csv` | 60 | Six regions, five numeric indicators, population. Parts D1–D2 |
| `districts.geojson` | 24 | The boundaries. Tiles exactly — the 24 areas sum to the bounding box to the square metre |
| `district_health.csv` | 24 | Cases, population, area, income, zone. Part D3 |
| `districts_coarse.geojson` | 6 | The same land in six zones, with a `members` list |
| `districts_alt.geojson` | 24 | The same land, 24 units, lines in different places |
| `county_crime.csv` | 20 | Crimes and population for the Part C activity |
| `smallarea_cases.csv` | 40 | Forty small units that all share one true rate |
| `case05_flat_rates.csv` | 24 | A nearly-flat set of rates, waiting to be classified |
| `region_profiles.csv` | 6 | Six same-scale ratings for two regions |
| `scatter_dense.csv` | 9,000 | Nine thousand marks with an 800-point cluster in them |

The geography is a **fictional federation** at 66–74°E, 24–36°N — roughly
real district sizes (16,746 to 95,678 km², a 5.7× spread) and no real place.
All data is synthetic, generated from a fixed seed for CDB601220.

## Expected results

Every figure below was recomputed from the committed files before this brief
was written. The full set is in `TASKS.md` beside the task it belongs to.

| Check | Expected |
|---|---|
| `r(cases, population)` across the 24 districts | **+0.986** — the count map *is* a population map |
| `r(rate, population)` | **−0.000** — and the rate is not |
| Top 3 districts by count / by rate | D17, D13, D09 / D19, D20, D21 — **overlap zero** |
| National pooled rate | 52.8 per 100,000, from 30,564 cases |
| `r(crimes, population)`, Part C | **+0.935**, and 7 of 20 counties move ≥3 places |
| `r(healthcare_access, cases_per_100k)` | **−0.799** — the X-shaped waist |
| Greedy axis order by \|r\| | access → cases → urban → median age → GDP |
| Income vs rate, by district / by zone | **−0.308** / **−0.889** |

## The five traps

1. **Case 1 · area is a square relationship.** Population spans 589× in
   `health_indicators.csv`, so a *correct* area encoding makes the largest
   bubble only **24×** the smallest across. Setting `s=pop**2` makes it 589×
   in area and sinks nine countries below one point.

2. **Case 2 · the two league tables do not intersect at all.** Top three by
   count and top three by rate share **no** districts. The count districts
   hold 6.3–11.0 M people; the rate districts hold 0.7–1.8 M.

3. **Case 5 · five classes will fit anything.** The rates span **7.2%** of
   their mean, and a five-class quantile scheme still paints a confident
   gradient across the whole federation. Classification cannot tell you
   whether there is a pattern; only the spread can.

4. **Case 6 · the hotspot is nine cases.** U32 reads 4.7× the national rate
   from **9 cases in 22,000 people**, while every unit over 100,000 people
   sits between 5.5 and 12.0. Every unit in that file has the same true
   rate.

5. **Case 8 · half the country is a twelfth of the map.** The five most
   populous districts are **12.6%** of the land area and **59.9%** of the
   population. A choropleth gives them a twelfth of the ink, and no amount
   of careful colouring fixes that — only a different chart does.

## One sentence to leave with

Say which channel carries which variable, and say what your map is *per* —
because a map can be arithmetically perfect and still do harm, since it
points at a place where people live.
