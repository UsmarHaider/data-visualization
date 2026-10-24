# Data dictionary

All data here is **synthetic**, generated for CDB601220 Week 5 from a fixed
seed, so every student works from identical files. The scenarios are
illustrative; the failure modes they demonstrate are not.

The geography is a **fictional federation** of 24 districts covering
66–74°E, 24–36°N — roughly the extent and the district sizes of a real South
Asian country, but no real place. Boundaries are plain **GeoJSON**, readable
with the standard-library `json` module. You do **not** need `geopandas`:
`geolib.read_geojson()` loads them, and `geolib` carries the projections, the
classification schemes and the drawing.

This dictionary tells you what the columns **mean**. It does not tell you
what is wrong with them — that is the task.

---

## `health_indicators.csv` — the country table (Parts D1–D3; cases 1, 3, 4)

Sixty countries across six fictional regions. This is the file for the bubble
chart and the parallel coordinates plot.

| Column | Type | Unit | Meaning |
|---|---|---|---|
| `country` | text | — | Country name |
| `region` | text | — | One of six regions — a **category**, not an amount |
| `gdp_pc` | int | USD/person/year | GDP per capita |
| `healthcare_access` | float | index 0–100 | Composite access rating, higher is better |
| `urban_pct` | float | % | Share of population living in urban areas |
| `median_age` | float | years | Median age of the population |
| `pop_m` | float | millions of people | Population |
| `cases_per_100k` | float | cases per 100,000 | Annual incidence — **already a rate** |

**Four notes the file cannot give you:**

- `cases_per_100k` is **already normalized**. Do not divide it by anything.
  The normalization lesson lives in the district files, not here.
- `pop_m` spans **0.6 to 353.4** — a factor of **589**. Any size channel you
  map it to will need `sizes=(lo, hi)` chosen on purpose, and area is a
  square relationship, so the largest mark is only **24×** the smallest in
  diameter. Slide 10.
- `gdp_pc` spans **$283 to $120,219**, and the largest value is **9.2× the
  second largest**. That is one country, and it is a real kind of country.
  What it does to a min–max scaled axis is case 3.
- The columns are stored in the order above. That order is **not** a
  recommendation — slide 24 is about exactly this.

---

## `districts.geojson` — the boundaries (Part D4; cases 2, 5, 7, 8)

Twenty-four districts, each a simple polygon, tiling the federation exactly
(the 24 areas sum to the bounding box to the square metre).

| Property | Meaning |
|---|---|
| `code` | `D01` … `D24` — the join key |
| `name` | District name |

Coordinates are **lon, lat in degrees**, CRS84, as GeoJSON requires. Degrees
are a storage format, not an analysis format: see `geolib.equal_area_xy()`
and slide 33.

## `districts_coarse.geojson` — the same land, 6 units (case 7)

The same 24 districts merged into **six zones**, four districts each. The
`members` property lists which district codes each zone contains, so you can
aggregate without a spatial join.

## `districts_alt.geojson` — the same land, 24 different units (case 7)

A second 24-unit partition of the same area with the lines in different
places. Same scale, different zoning. Codes are `A01` … `A24`.

---

## `district_health.csv` — the outbreak (Part D4; cases 2, 7, 8)

One row per district. Joins to `districts.geojson` on `code`.

| Column | Type | Unit | Meaning |
|---|---|---|---|
| `code` | text | — | Join key |
| `district` | text | — | District name |
| `cases` | int | cases | Confirmed cases this period — a **count** |
| `population` | int | people | Resident population |
| `area_km2` | float | km² | Land area, already computed on the sphere |
| `lon`, `lat` | float | degrees | Vertex mean of the polygon |
| `income_pc_usd` | int | USD/person/year | District income per head |
| `zone` | text | — | Which of the six coarse zones this district is in |

**Three notes the file cannot give you:**

- `cases` is a **count**, and `population` varies **23×** across districts.
  Slide 37 is about what happens next.
- `area_km2` was computed with spherical excess, not from the raw degree
  coordinates. `geolib.polygon_area_km2()` reproduces it to 0.000%, and
  Part B question 4 asks you to compute it the wrong way on purpose.
- The districts differ in area by **5.7×** (16,746 to 95,678 km²) and in
  population density by **6 to 327 people/km²**. Slide 46.

---

## `case05_flat_rates.csv` — a different outbreak (case 5)

Same 24 district codes, a different and unrelated set of counts. One row per
district: `code`, `district`, `cases`, `population`.

> This is **not** a second period of `district_health.csv`. It is a separate
> scenario that exists to be classified.

---

## `smallarea_cases.csv` — forty small units (case 6; Part B q5)

Forty sub-district units, `U01` … `U40`, with `cases` and `population`.
Populations run from a few thousand to 268,500.

> One fact about this file is given to you, because the task is impossible
> without it and trivial with it: **every unit has the same true underlying
> rate.** What you see is what Poisson noise looks like on a map.

---

## `county_crime.csv` — the two-map activity (Part C)

Twenty counties, `county`, `crimes_reported`, `population`. This is the
slide 52–53 activity with a real file behind it: the same records, two
denominators, two different league tables.

---

## `region_profiles.csv` — six ratings, two regions (case 9)

| Column | Meaning |
|---|---|
| `indicator` | One of six service indicators, all on the same 0–100 scale |
| `region_a`, `region_b` | The two profiles |

The six indicators are stored in an arbitrary order. That is the case.

---

## `scatter_dense.csv` — nine thousand marks (Part D2; Part B q2)

`x` and `y` only, 9,000 rows. Slide 15: an opaque default is not a neutral
choice.

---

All figures quoted above were recomputed from these committed files before
this dictionary was written. If one of them does not reproduce for you, say
so in your submission with the number you got — that is a finding, not a
failure.
