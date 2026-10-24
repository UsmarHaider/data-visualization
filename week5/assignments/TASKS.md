# Week 5 — Assignments: Multivariate Data & Geospatial Visualization

Five parts covering **Lecture 9** (more variables than axes) and **Lecture
10** (putting data on a map).

| | |
|---|---|
| **L9** | Map high-dimensional datasets using multivariate encodings — position, colour, size and shape; implement parallel coordinates plots — **CLO2 · Competence** |
| **L10** | Construct thematic spatial visualizations — choropleth, proportional symbol and dot density — and avoid population bias, boundary distortion and inappropriate colour scaling — **CLO2 · Competence** |

---

## The point of this week

Week 1 taught you to **see** a chart. Week 2 taught you to **judge** one.
Week 3 taught you to **build** one. Week 4 gave you time and parts.

This week you run out of axes. You have four or five variables and two
positions, so the rest of the data has to go into area, lightness, hue and
shape — a budget, spent in order. Then the frame becomes a **map**, and both
position channels are gone before you have shown a single number.

Week 4's nine charts were broken **upstream of the pixels** — a parse, a
resample, a window, a denominator. This week's nine are broken by **the
encoding or the geography**: the arithmetic is right, the parse is right,
the chart is drawn carefully, and it still says something false.

> **The one thing this week is really testing.** Last week the trap was a
> generic fix. This week the trap is **a chart that is beautiful and wrong**.
> Six of the nine cases below would pass a design review. They are properly
> labelled, colour-blind safe, correctly sourced, and three of them are
> prettier than anything you will produce this term.
>
> You do not get the marks for noticing the chart is ugly. You get them for
> **naming which channel or which boundary is lying, and proving it from the
> data.**

| Part | Covers | Marks |
|---|---|---|
| **A** | Rebuild nine charts, then take them apart | 36 |
| **B** | The five spatial and channel decisions, computed | 15 |
| **C** | The two-map activity, run on real readers | 9 |
| **D** | Build the three health figures | 25 |
| **E** | One page of written justification | 15 |
| | | **100** |
| **F** | *Bonus* — a normalized map on data you found yourself | 5 |

Part F is marked **out of 5 and reported separately**. It is not added into
the 100 and it is not a gate on anything.

---

## Setup

Everything is already in this folder. Nothing to download.

```bash
cd week5/assignments
python3 geolib.py          # self-check: confirms the toolkit works
```

You should get a district count, an exact area check, a Mercator inflation
figure, three classification schemes scored, a greedy axis order, a funnel
width, and a PNG with a choropleth, a proportional-symbol map and a parallel
coordinates plot in it. If that runs, everything else will.

**Requirements:** Python 3.9+, and:

```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn
```

`scikit-learn` is new, and only Part B question 3 needs it (`PCA`).

> **You do not need geopandas.** The boundaries are plain GeoJSON, read with
> the standard-library `json` module, and `geolib` carries the projections,
> the classification schemes and the polygon drawing in about 300 lines.
> Every number in this brief was produced with `geolib`.
>
> If you *do* have `geopandas` and `mapclassify`, you are welcome to use them
> — say so in Part E, and check your class breaks against `geolib.breaks()`.
> Note that `scheme=` in `GeoDataFrame.plot()` is **silently ignored** when
> `mapclassify` is missing, which is slide 49 and a genuinely nasty bug.

| Path | What it is |
|---|---|
| `vizlib.py` | **Week 3's toolkit, unchanged.** Palette, `lie_factor()`, `simulate_cvd()`, `save_fig()` |
| `geolib.py` | This week's toolkit, built on top of `vizlib`. Read it — it is short, and it has no GIS dependency |
| `data/` | Ten files: seven tables and three GeoJSON boundary sets |
| `data/DATA_DICTIONARY.md` | What the columns **mean**. Not what is wrong with them |

There are no starter scripts. Week 3 gave you three skeletons; from Week 4
you write the script yourself, with the toolkit as the only scaffolding.

---

## Carried forward

Nothing from Weeks 1–4 is retired. You are expected to name these ideas by
these names in your write-up.

| From | The idea | Where it returns this week |
|---|---|---|
| **W1** | The question chooses the chart | Case 2 and case 8; slide 31's three tests before you draw a map at all |
| **W1** | Title states the finding | Every figure, every part |
| **W1** | Bars start at zero; never two y-axes | Case 8's redesign is a sorted bar chart beside the map |
| **W2** | Channel ranking: position > length > angle > area | **The whole of Part 1.** It is now a budget, spent in order |
| **W2** | One pop-out per chart; grey for context | Part D2's brushing — grey everything, bold one region |
| **W2** | Angle and area are read badly | Case 1 (area) and case 9 (angle, in a radar chart) |
| **W2** | Experiments run on real readers | **Part C.** Invented results still score zero |
| **W3** | `fig, ax = plt.subplots()`, always | Every figure. No `plt.plot()` |
| **W3** | Sequential colormap, dark means more, never rainbow | Part D3 and case 5 |
| **W3** | Declare every parameter that changes the picture | Part E — the scaling, the axis order, the breaks, the projection |
| **W3** | Colour-blind-safe palette, proved not claimed | `vizlib.PALETTE` is already in `geolib` |
| **W4** | A denominator is a modelling decision | **Case 2, Part C, Part D3.** Slide 38 |
| **W4** | State every row you removed, with rule and count | Part E, and the suppression clause |
| **W4** | An `Other` bucket declares what it hides | Part D1 — regions beyond seven |

---

## The rules

**New in Week 5 — applied to every figure you produce:**

- **Area means area.** If a value drives a mark's size, it drives the
  **area**, so the radius goes as the square root. `ax.scatter(s=...)`
  already takes area in points²; anything that takes a radius does not.
  Slide 10.
- **Every size channel gets a legend.** Three reference circles with real
  values. `geolib.size_legend()`. Without it, area is decoration. Slide 11.
- **Hue carries identity, lightness carries amount.** Never a rainbow for a
  quantity, and at most about seven hues for categories. Slide 40.
- **Say what you scaled and in which order.** A parallel coordinates plot
  without its scaling method and axis order stated on the figure scores
  nothing for the scaling or the order. Slides 22 and 24.
- **Normalize, or publish a population map.** A choropleth of a raw count is
  a population map. Put the denominator in the **legend title**, in words.
  Slide 37.
- **Print the class breaks.** How many classes and where they fall, in the
  legend. Slide 39.
- **Project before you measure or colour an area.** Never compute an area, a
  distance or a buffer in degrees. Slide 33.
- **Name the boundaries and the date.** Which units, from which source, from
  which year. Slide 50 step 6.
- **Say what you suppressed.** If you merged or hid a unit because its count
  was too small, the rule and the count go on the figure. Slides 45 and 48.

---

## Part A · Rebuild nine charts, then take them apart  (36 marks)

Nine analysts published nine claims. You get their data and the recipe each
of them followed. **Build the chart, then work out why it is wrong.**

Every one of these charts is arithmetically correct. No number has been
fiddled and no axis is truncated unless the recipe says so.

### What to hand in for each of the nine

Four marks each.

| | Marks |
|---|---|
| **Rebuild it.** Your chart reproduces the published claim from the recipe, and hits the self-check number | 1 |
| **The conclusion and the decoy.** The conclusion the chart invites, in one sentence — plus the first objection you thought of and *why it does not hold here*, ruled out with evidence from the data | 1 |
| **The mechanism.** Which channel or which boundary is lying, named precisely, with the number that demonstrates it | 1 |
| **The redesign.** The honest chart, actually plotted, not described | 1 |

"The colours are bad" scores **zero** on the mechanism mark for case 5, in
the same way "the dates are wrong" scored zero last week. Say *which*
decision, *which* units it affects, and show the number that changes.

---

### 1 · "Population and healthcare access are unrelated — the large countries are spread right across the range"
`health_indicators.csv`

> Scatter `healthcare_access` against `gdp_pc` on a log x-axis, one mark per
> country, with the mark size carrying population:
> `ax.scatter(df.gdp_pc, df.healthcare_access, s=df.pop_m**2)`.

**Self-check:** 60 marks. The largest mark is drawn **589×** the area of the
smallest, and **9** countries with populations under 2.0 M are smaller than
a single point.

### 2 · "The outbreak is concentrated in the three districts around the capital"
`district_health.csv` + `districts.geojson`

> Join on `code`, colour each district by `cases` with five natural breaks
> and a sequential blue ramp, and list the top three.

**Self-check:** 24 districts, **30,564** cases, population **57,857,000**.
The top three by count are **D17, D13, D09**.

### 3 · "GDP per capita barely varies across the sample"
`health_indicators.csv`

> Min–max scale all five numeric columns to 0–1 and draw a parallel
> coordinates plot. Observe that the `gdp_pc` axis is almost flat along the
> bottom.

**Self-check:** after min–max scaling, **58 of the 60** countries sit below
**0.10** on the `gdp_pc` axis and the median lands at **0.017**.

### 4 · "Healthcare access and case rate are unrelated — there is no crossing pattern between them"
`health_indicators.csv`

> Draw a parallel coordinates plot with the columns in the order they appear
> in the file, min–max scaled, and read the gaps between adjacent axes.

**Self-check:** five axes in file order. The `healthcare_access` and
`cases_per_100k` axes are **three apart**, with `urban_pct` and `median_age`
between them.

### 5 · "There is a clear five-level gradient in incidence across the federation"
`case05_flat_rates.csv` + `districts.geojson`

> Compute `cases / population * 1e5`, classify into five **quantile**
> classes, and colour with a five-step sequential ramp.

**Self-check:** 24 districts. The rate runs **31.07 to 33.40** per 100,000 —
a total spread of **7.2%** of the mean.

### 6 · "Unit U32 is a hotspot — it is running at nearly five times the national rate"
`smallarea_cases.csv`

> Compute `cases / population * 1e5` per unit, rank them, and map or bar-chart
> the result. Report the worst unit against the pooled national rate.

**Self-check:** 40 units. Pooled rate **8.72** per 100,000. U32 reads
**40.9** — **4.7×** the national rate — from **9 cases in 22,000 people**.
Meanwhile the **10** units with populations over 100,000 all fall between
**5.5** and **12.0**.

### 7 · "District income and case rate are only weakly related — r is about −0.31"
`district_health.csv`

> Correlate `income_pc_usd` against `cases / population * 1e5` across the 24
> districts and report the coefficient.

**Self-check:** r = **−0.308** across 24 districts.

### 8 · "This is a rural outbreak — look how much of the map is dark"
`district_health.csv` + `districts.geojson`

> Choropleth the rate with five natural breaks, then describe the map by how
> much of it is in the top two classes.

**Self-check:** the five most populous districts are **12.6%** of the land
area and **59.9%** of the population.

### 9 · "Region A is the stronger of the two — its profile encloses visibly more area"
`region_profiles.csv`

> Radar chart, six axes in the order the file gives them, both profiles on
> one pair of axes, filled with transparency. Compare the enclosed areas.

**Self-check:** the two means are **62.3** and **62.0** — a difference of
**0.33** on a 0–100 scale. In the file's axis order the enclosed areas are
**9,933** and **9,433**.

---

### Three things that will save you an afternoon

- **`geolib.read_geojson()` needs no GIS install.** It returns plain dicts
  with a `ring` of `(lon, lat)` tuples. `geolib.choropleth()` takes those
  features and a dict of values keyed by `code`.
- **Check the join before you plot.** Count the rows that failed to match.
  A district that silently fails to join is a white hole in your map, and
  on a 24-district map you will not necessarily notice one.
- **Two of the nine are not fixed by changing the chart type.** The redesign
  is the same chart with a different *decision* inside it. Work out which
  two before you start redrawing.

---

## Part B · The five decisions, computed  (15 marks)

Three marks each. Every answer is a number or a short table, printed by your
script — not an opinion.

**1 · The size range.** For `health_indicators.csv`, pick the `sizes=(lo,
hi)` you will use in Part D1 and justify both ends: the smallest mark that
is still readable, and the largest that does not swallow its neighbours.
Report the **diameter** ratio your choice implies, and show that you used
area and not radius.

**2 · Overplotting.** Load `scatter_dense.csv` (9,000 points). Produce the
same scatter four ways — opaque, transparent, hexbin, and a 2-D KDE — and
report, for each, whether the **800-point cluster at (3.1, 3.0)** is
visible. Then state which you would publish and why. Name the `alpha` and
the `gridsize` you used; they are parameters, so they get declared.

**3 · Scaling and dimension reduction.** Scale the five numeric columns of
`health_indicators.csv` three ways — min–max, z-score and percentile rank —
and report what each does to the `gdp_pc` axis, in numbers. Then run `PCA`
on the standardised columns and report the **explained variance ratio** of
the first two components. State how much of the data a two-axis picture of
this dataset is missing.

**4 · Project before you measure.** Compute the land area of all 24
districts two ways: with `geolib.polygon_area_km2()` (spherical) and with a
plain shoelace on the raw lon/lat coordinates. Report the **share of total
area** held by the four northernmost districts under each method, and the
single district whose share is most distorted. Then report the **Mercator
area inflation** factor across the federation, and say in one sentence why
that number is the reason slide 34 says a choropleth needs an equal-area
projection.

**5 · Small-area stability.** For `smallarea_cases.csv`, build a funnel
plot: observed rate against population, with 95% Poisson limits that widen
as population falls (`geolib.funnel_limits()`). Report **how many of the 40
units fall outside the limits**, and state what that tells you about the
map in case 6. Then state the minimum population at which a rate of 9 per
100,000 could be distinguished from 18 per 100,000 at all.

---

## Part C · The two-map activity, on real readers  (9 marks)

The slide 52–53 activity, with a real file behind it and real readers in
front of it.

`data/county_crime.csv` holds 20 counties with `crimes_reported` and
`population`.

**1 · Build both maps (3 marks).** Map A: counties coloured by
`crimes_reported`. Map B: counties coloured by crimes per 100,000 residents.
Same boundaries, same five-class scheme, same ramp. The *only* difference is
the denominator. Join on `code` to `districts.geojson`, which carries the
geometry for `D01`–`D24`; the 20 counties use `D01`–`D20`, so **four
polygons will not match and you should leave them out and say so.**

**2 · Run it on at least five readers (4 marks).** One at a time, and **in
this order**:

1. Show them **Map A only**. Ask: *"Which three counties would you send
   extra police to, and why?"* Write their three down.
2. Then show **Map B**. Ask the same question. Write their three down.
3. Do not let them revise answer 1.

Record one row per reader: their three from A, their three from B, and the
**overlap count**. Save it as `partC_reader_results.csv`.

**3 · Report it (2 marks).** The mean overlap across your readers, and one
sentence on what each map is actually a map of.

**Self-check:** r(`crimes_reported`, `population`) = **+0.935**. The top
three by count are **Dunmere, Pellbrook, Grimsby**; by rate they are
**Hollowfield, Netherby, Elmsworth** — an overlap of **zero**. Seven of the
twenty counties move **three or more places** between the two rankings, and
two of them — **Elmsworth** (22,000 people) and **Hollowfield** (12,000) —
go from the bottom of the count map to the top of the rate map.

> **Five readers is the minimum and they must be real.** Fabricated or
> implausible results score zero for the whole part, exactly as in Week 4.
> If your readers all pick the same three from both maps, that is a result —
> report it and say what you think happened.

---

## Part D · Build the three health figures  (25 marks)

The application task from slides 54 and 57, with real files behind it.

A global health organization is tracking a regional outbreak alongside four
socio-economic indicators. Separate two-variable charts mask the
interactions, and the regional map plots **raw case counts**, so every
densely populated district lights up every week whatever the actual risk.

Produce **three figures**, each exported at 300 dpi with
`bbox_inches="tight"` — `vizlib.save_fig()` does both.

### D1 · The four-variable bubble chart (8 marks)

`health_indicators.csv`. Two positions, area and hue:

| Channel | Variable | Watch for |
|---|---|---|
| x | `gdp_pc`, **log scale** | the spread is multiplicative |
| y | `healthcare_access` | 0–100, so the axis has real bounds |
| area | `pop_m` | **area**, not radius; `sizes=(lo, hi)` from Part B1 |
| hue | `region` | six categories — identity, not amount |

Draw the **size legend**. Direct-label the three or four countries you will
talk about rather than relying on a legend of sixty. Decide what to do about
the `gdp_pc` outlier and say what you decided on the figure.

### D2 · The parallel coordinates plot (8 marks)

Same file, the five numeric columns. Three decisions, all declared on the
figure:

1. **The scaling** — min–max, z-score or rank, with the reason.
2. **The axis order** — computed, not eyeballed. `geolib.corr_chain()`
   implements slide 24's greedy rule; if you order them differently, say why.
3. **The clutter control** — grey everything, then brush one region.

Then name **two relationships you can actually see** in it, and say which
pair of adjacent axes shows each.

**Self-check:** the greedy chain by absolute correlation is
`healthcare_access → cases_per_100k → urban_pct → median_age → gdp_pc`, and
r(`healthcare_access`, `cases_per_100k`) = **−0.799** — the X-shaped waist
from slide 23.

### D3 · The normalized choropleth (9 marks)

`district_health.csv` + `districts.geojson`. The six-step recipe from
slide 50:

1. **Project** — equal-area, because colour over an area makes area the
   encoding channel.
2. **Join** on `code`, and **count the rows that failed**.
3. **Normalize** — cases per 100,000 residents, and the denominator goes in
   the **legend title in words**.
4. **Classify** — five classes, scheme chosen and named, breaks printed.
5. **Colour** — one sequential hue, dark means more, colour-blind safe.
6. **Caption** — units, source, extraction date, projection, and anything
   you suppressed.

Then put the **count** back on as proportional symbols, or as a sorted bar
chart beside the map. Slide 47 row 3.

**Self-check:** 24 districts join with **0** failures. The national pooled
rate is **52.8** per 100,000 from **30,564** cases. The top three districts
by **rate** are **D19, D20, D21**; by **count** they are **D17, D13, D09** —
an overlap of **zero**, and r(`cases`, `population`) = **+0.986**.

### Marking

| | Marks |
|---|---|
| The script runs from a clean environment and produces all three PNGs | 5 |
| D1 — four channels, correct area scaling, size legend, outlier handled | 6 |
| D2 — scaling, axis order and brushing all chosen and declared | 6 |
| D3 — normalized, classified, projected, captioned; join checked | 8 |

### Three things that lose marks every year

- **A size legend that is missing, or that shows scaled numbers instead of
  real ones.** The legend exists so the reader can convert area back into
  people.
- **A parallel coordinates plot with no stated scaling.** The axes are
  unitless by construction. Four words — "axes min–max scaled" — are the
  difference between a chart and a picture.
- **A choropleth legend reading "cases".** It is `cases per 100,000
  residents`, or it is a population map with a misleading label.

---

## Part E · The written justification  (15 marks)

One page. The questions are from slide 57 Part B, and the marks follow them.

| | Marks |
|---|---|
| **Which variable got which channel, and why** — ranked by how precisely the reader must compare them, per slide 8's budget | 4 |
| **The parallel coordinates decisions** — the scaling and the axis order you chose, and one relationship the chart revealed that a pairwise scatter matrix would not have | 4 |
| **The spatial decisions** — your denominator, your classification scheme and your projection, each with a sentence of justification | 4 |
| **The counterfactual** — one paragraph on what your raw-count map would have shown instead, and **who it would have pointed at** | 3 |

### The ethics clause — read this one twice

The counterfactual paragraph is not a formality, and it is where slide 48
lands.

A raw-count map of disease, crime or poverty names the largest city every
time. Published often enough, that becomes a reputation the data never
supported — and the cost falls on the people living in the place you
coloured dark, not on you. Your Part C results are evidence about how
readers actually behave with these two maps; use them.

If you suppressed or merged any unit because its count was too small to
publish, **say which, say the rule, and say the count**. Four cases in one
village is a health record with a map reference. Aggregating up is the
honest move and it is also the one that loses you the most interesting
pattern on the map — say that too.

---

## Part F · Bonus — a normalized map on your own data  (5 marks)

Slide 57's Part A, on data you source yourself.

Find a real dataset with a geographic key and a count you can normalize —
World Bank, WHO, the Pakistan Bureau of Statistics, GADM, Natural Earth,
OpenStreetMap, or your FYP data. Produce **one** choropleth of a normalized
rate, with five classes, a stated scheme, an equal-area projection and a
full caption.

| | Marks |
|---|---|
| The map is correct and the rate is genuinely normalized | 2 |
| Both sources cited — the data **and** the boundaries — with the date you downloaded each | 1 |
| The class scheme and projection named and justified | 1 |
| One sentence on what the raw-count version would have shown | 1 |

Marked out of 5, reported separately, never added into the 100.

> Boundary files for Pakistan are free from GADM, Natural Earth and OSM.
> Cite **which** and **which version** — they disagree with each other, and
> the disagreements are themselves political. Slide 48.

---

## What you hand in

One ZIP on the LMS by the announced due date.

```
partA_charts.py            rebuilds all nine, and plots your nine redesigns
partA_diagnosis.pdf        your nine diagnoses, with both figures per case
partB_decisions.py         + its printed output
partC_maps.py              the two maps
partC_reader_results.csv   one row per reader
partD_bubble.py            + partD_bubble.png
partD_pcp.py               + partD_pcp.png
partD_choropleth.py        + partD_choropleth.png
partE_justification.pdf    one page
partF_map.py               (bonus, optional) + partF_map.png + the sources
```

Cite your sources. All data in this folder is synthetic and generated for
CDB601220 — say so if you quote a number from it.

---

## Marking guide

| | Weight |
|---|---|
| Part A — the lying channel or boundary named and proved from the data | 36% |
| Part B — the five decisions computed, not asserted | 15% |
| Part C — both maps built, the experiment genuinely run, overlap reported | 9% |
| Part D — three figures that run, with their decisions declared on them | 25% |
| Part E — channels, scaling, spatial decisions and the counterfactual | 15% |

**Automatic deductions:**

- a value driving a mark's **radius** instead of its area
- a size channel with no legend, or a legend showing scaled numbers
- a parallel coordinates plot with no stated scaling method
- an axis order chosen after seeing the result and not declared
- a choropleth of a **raw count**, or a legend title that omits the
  denominator
- class breaks not printed in the legend
- a rainbow colormap for a quantity, or a diverging ramp with no real
  midpoint
- an area, distance or density computed in degrees
- a choropleth drawn on a non-equal-area projection without saying so
- a small-area rate published with no stability check and no suppression rule
- boundaries used with no source and no year
- `plt.plot()` / `plt.scatter()` instead of `ax` methods
- a required export saved at less than 300 dpi
- invented or implausible reader results in Part C
- a join whose unmatched rows were never counted

---

## Readings

- **Wilke**, *Fundamentals of Data Visualization* — Ch. 12 (associations
  among several quantitative variables), Ch. 15 (geospatial data). Free
  online.
- **geopandas user guide — Mapping and plotting tools.** Choropleths,
  classification schemes, projections. Read it even if you use `geolib`.
- **Monmonier, M. (2018)**, *How to Lie with Maps*, 3rd ed. — Ch. 1–3 and
  the data-maps chapter. Short, readable, and the source of most of Part 4
  of the lecture.
- **Openshaw, S. (1984)**, *The Modifiable Areal Unit Problem*, CATMOG 38.
  The paper behind case 7. Skim the examples if nothing else.
- **Cleveland, W. S. & McGill, R. (1984)**, "Graphical Perception", *JASA*
  79(387), 531–554. The channel ranking, now being used as a budget — third
  week running.
- **Inselberg, A. (1985)**, "The plane with parallel coordinates". Where the
  idiom comes from, and why the crossings mean what they mean.
- **Jenks, G. F. (1967)**, "The data model concept in statistical mapping".
  The natural-breaks algorithm `geolib.breaks()` implements exactly.
