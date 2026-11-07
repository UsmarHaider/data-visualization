# Data dictionary

All data here is **synthetic**, generated for CDB601220 Week 7 from a fixed
seed, so every student works from identical files. The scenario is
illustrative; the defects in the files are not.

The geography is the **same fictional federation as Weeks 5 and 6** — 24
districts over 66–74°E, 24–36°N, no real place — this time as the Federal
Transit Authority holds it. District codes, names, populations and areas
match those weeks, and `regions.geojson` is byte-identical to Week 6's, so
anything you built then still joins. Boundaries are plain **GeoJSON**,
readable with the standard-library `json` module; you do not need
`geopandas`.

This dictionary tells you what the columns **mean** and what unit they are
in. It does not tell you what is wrong with them. That is Task A.

---

## The one distinction the whole week turns on

**A boarding is not a journey.**

- A **boarding** (a *leg*) is one person entering one vehicle. A passenger
  who rides a bus to a metro station and then takes the metro produces
  **two** boardings and **one** journey.
- A **journey** (a *trip*, in the fare system's language) is one person
  travelling from where they started to where they were going, however many
  vehicles that took.

`ridership_daily.csv` and the two `boardings_annual` columns count
**boardings**. `fare_revenue.csv` counts **journeys**. The two files are
therefore both correct and not comparable without saying which unit you are
in. Every chart you draw must say which one it is counting, in words, on the
figure.

## Codes, not blanks

These are operator returns, and an operator return records *why* a number is
absent with a code rather than an empty cell. A value that cannot occur in
the real world — a negative length, a percentage above 100, a zero where a
zero is impossible — is a code, not a measurement. Week 1's rule applies:
missing is not zero, and a code is not a value.

## Published tables

`fare_revenue.csv` is a published ministry table, reproduced verbatim. A
publisher files whatever rows it chooses to file, in whatever order it likes.
Before you sum a column, check that the rows you are adding up are all the
same kind of thing.

---

## `district_transit.csv` — the district register

The Authority's register of the districts it serves, exported from the asset
system.

| Column | Type | Unit | Meaning |
|---|---|---|---|
| `code` | text | — | `D01` … `D24`. The join key to `regions.geojson` |
| `district` | text | — | District name as typed into the register |
| `population` | int | people | Resident population |
| `households` | int | households | Households |
| `area_km2` | float | km² | Land area |
| `lon`, `lat` | float | degrees | A point inside the district |
| `income_pc_usd` | int | USD/person/year | Income per head |
| `stops` | int | stops | Transit stops inside the district |
| `road_km` | float | km | Surfaced road length, from the last survey |
| `boardings_annual` | int | boardings | Boardings **attributed to this district** over the 12 months ending **2026-08-31** |
| `fare_concession_pct` | float | % | Share of journeys made at a concession fare |
| `vehicles_registered` | int | vehicles | Private vehicles registered to addresses in the district |

`area_km2` is in km²; `lon`/`lat` are in degrees. Degrees are not a distance
and never an area — Week 5's rule, and `geolib` has the projections.

## `routes.csv` — one row per route

The network as the operations team holds it. Thirty-six routes.

| Column | Type | Unit | Meaning |
|---|---|---|---|
| `route_id` | text | — | `R001` … , unique |
| `mode` | text | — | The vehicle type the route is run with, as the operations team typed it |
| `corridor` | text | — | `C1` … `C6`, the planning corridor the route belongs to |
| `length_km` | float | km | Route length, one direction |
| `stops` | int | stops | Stops served |
| `fleet` | int | vehicles | Vehicles assigned |
| `districts_served` | text | — | The districts the route runs through, `;`-separated. A route is listed under **every** district it serves |
| `boardings_annual` | int | boardings | Boardings on this route over the 12 months ending **2026-08-31** |
| `punctuality_pct` | float | % | Share of this route's departures that ran on time, from the AVL feed |
| `crowding_index` | float | ratio | Mean peak-hour passengers ÷ seated-plus-standing capacity. 1.0 is exactly at capacity; above 1.0 is over it |
| `cost_recovery_pct` | float | % | Fare revenue ÷ operating cost |
| `subsidy_pkr_per_trip` | float | PKR/journey | Public subsidy per journey carried |

`districts_served` is a list, not a category. A route that runs through four
districts appears in four districts' worth of any by-district breakdown you
build from this file.

## `ridership_daily.csv` — one row per mode per reporting day

What each mode's control room filed, for around eighteen months.

| Column | Type | Unit | Meaning |
|---|---|---|---|
| `date` | text | — | The reporting day, as the control room wrote it |
| `mode` | text | — | Metro, BRT, Bus or Ferry |
| `trips_scheduled` | int | departures | Departures in the published timetable for that day |
| `trips_operated` | int | departures | Departures actually run |
| `trips_on_time` | int | departures | Of those run, how many arrived inside the on-time window |
| `boardings` | int | boardings | Boardings that day. A **flow**: a count of events during the day, not a reading on anything |
| `delay_minutes` | int | minutes | Total delay accumulated across late departures that day |

Punctuality is `trips_on_time / trips_operated`. It is a **ratio of two
counts**, so it is computed by summing both columns over whatever period you
want and then dividing. A mean of daily percentages is not a punctuality
rate; it weights a Sunday with 300 departures the same as a Tuesday with
3,000.

A row is a day a control room **filed a return**. A day with no row is a day
nobody filed, which is not the same thing as a day with no service — and not
the same thing as zero boardings.

## `fare_revenue.csv` — one row per month per mode per fare product

The ministry's published fare table, eighteen months.

| Column | Type | Unit | Meaning |
|---|---|---|---|
| `month` | text | — | `YYYY-MM` |
| `mode` | text | — | Metro, BRT, Bus or Ferry |
| `ticket_type` | text | — | The fare product, as published |
| `trips` | int | **journeys** | Journeys sold against that product that month — transfer-linked, so not comparable with `boardings` |
| `revenue_pkr` | int | PKR | Revenue collected |

A monthly fare table is built from what was sold in that month. If the last
month of a file is not a whole month, it is not comparable with the months
before it, and a chart that draws it at the same visual weight says something
untrue — Week 4's rule, unchanged.

## `regions.geojson` — the boundaries

A `FeatureCollection` of 24 `Polygon` features. Each has `properties.code`
(`D01` … `D24`) and `properties.name`. Byte-identical to Week 6's file.

Read it with `geolib.read_geojson()`, which returns the ring and the
properties and needs no GIS stack.

---

All data in this folder is synthetic and generated for CDB601220. Do not
cite any number in it outside this course.
