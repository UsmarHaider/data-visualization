# Data dictionary

All data here is **synthetic**, generated for CDB601220 Week 6 from a fixed
seed, so every student works from identical files. The scenario is
illustrative; the defects in the files are not.

The geography is the **same fictional federation as Week 5** — 24 districts
over 66–74°E, 24–36°N, no real place — this time as the national electricity
operator holds it. Populations, areas and district names match Week 5's
files, so anything you built then still joins now. Boundaries are plain
**GeoJSON**, readable with the standard-library `json` module; you do not
need `geopandas`.

This dictionary tells you what the columns **mean** and what unit they are
in. It does not tell you what is wrong with them. That is the task.

---

## `district_grid.csv` — one row per district

The operator's district register, exported from the asset system.

| Column | Type | Unit | Meaning |
|---|---|---|---|
| `code` | text | — | `D01` … `D24`. The join key to `regions.geojson` |
| `district` | text | — | District name as typed into the register |
| `zone` | text | — | `P1` … `P6`. The supply zone the district belongs to, and the key to `grid_daily.csv` |
| `population` | int | people | Resident population |
| `households` | int | households | Billed domestic connections |
| `area_km2` | float | km² | Land area |
| `lon`, `lat` | float | degrees | A point inside the district |
| `income_pc_usd` | int | USD/person/year | Income per head |
| `electrification_pct` | — | % | Share of households connected to the grid |
| `solar_kw_installed` | int | kW | Rooftop solar capacity registered in the district |
| `outages` | int | interruptions | Supply interruptions recorded on district feeders, 12 months |
| `outage_minutes` | int | minutes | Total interruption duration over the same 12 months |

`outages` and `outage_minutes` cover the same twelve months, so
`outage_minutes / outages` is a mean interruption length in minutes.

---

## `grid_daily.csv` — one row per supply zone per reporting day

What each zone's control room filed. Six zones, around seventeen months.

| Column | Type | Unit | Meaning |
|---|---|---|---|
| `date` | text | — | The reporting day, as the control room wrote it |
| `zone` | text | — | `P1` … `P6`, joins to `district_grid.zone` |
| `cumulative_mwh` | float | MWh | The **reading on the zone's energy meter** at the end of that day. A meter counts up from the day it was installed |
| `peak_load_mw` | float | MW | The highest instantaneous demand seen that day |
| `outage_minutes` | int | minutes | Interruption minutes filed for that zone that day |

A meter reading is not a quantity of energy. Energy delivered over a period
is the **change** in the reading across that period, in MWh. `peak_load_mw`
is an instantaneous maximum, so it has no total — only a mean, a median or
a maximum over whatever period you choose.

Where the SCADA peak reading failed, the field carries the operator's
not-available code rather than a blank. The code is a number.

---

## `generation_mix.csv` — one row per month per generation category

How the energy was generated, as published monthly.

| Column | Type | Unit | Meaning |
|---|---|---|---|
| `month` | text | `YYYY-MM` | Calendar month |
| `source` | text | — | Top level of the generation hierarchy |
| `subsource` | text | — | Second level |
| `mwh` | int | MWh | Energy generated in that month in that category |

The file is published exactly as the ministry publishes it, including the
rows the ministry puts in it. Eighteen months, and every month carries the
same set of rows.

---

## `regions.geojson` — the boundaries

Twenty-four districts, each a simple polygon, tiling the federation exactly
(the 24 areas sum to the bounding box to the square metre). Identical
geometry to Week 5's `districts.geojson`.

| Property | Meaning |
|---|---|
| `code` | `D01` … `D24` — the join key |
| `name` | District name |

Coordinates are **degrees**, longitude first. An area, a distance or a
density computed in degrees is wrong by a factor that changes with latitude:
project first. `geolib.polygon_area_km2()` and `geolib.equal_area_xy()` are
already there.
