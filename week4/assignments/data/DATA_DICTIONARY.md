# Data dictionary

All data here is **synthetic**, generated for CDB601220 Week 4 from a fixed
seed, so every student works from identical files. The scenarios are
illustrative; the failure modes they demonstrate are not.

Every file has something wrong with it. This dictionary tells you what the
columns **mean**. It does not tell you what is wrong — that is the task.

---

## `sessions_hourly.csv` — the primary dataset (Part D)

Hourly web traffic for the e-commerce platform on slide 5, from April 2024.

| Column | Type | Unit | Meaning |
|---|---|---|---|
| `ts` | text | — | Timestamp of the hour, **as two loggers wrote it** |
| `sessions` | int | sessions/hour | Visits beginning in that hour |
| `orders` | int | orders/hour | Orders placed in that hour |
| `revenue_pkr` | int | PKR | Gross revenue booked in that hour |
| `device` | text | — | Device class, as the tag fired |

**Three notes the file itself cannot give you:**

- `sessions`, `orders` and `revenue_pkr` are **flows** — they count things
  that happened *during* the hour. Slide 12: a flow resamples with `sum()`,
  never `last()`. There is no level column in this file.
- The platform serves Pakistan only, so there is **no daylight-saving
  transition** anywhere in the range. Every real day has exactly 24 hours.
  If a day does not, something happened to the collector, not to the clock.
- The extract was taken part-way through a month. That is a fact about the
  extract, not about the business.

---

## `revenue_catalogue.csv` — the hierarchy (Part D)

One row per SKU, covering the same window as `sessions_hourly.csv`.
Four categories, eight sub-categories.

| Column | Type | Unit | Meaning |
|---|---|---|---|
| `category` | text | — | Top level of the hierarchy |
| `subcategory` | text | — | Second level |
| `sku` | text | — | Stock-keeping unit identifier |
| `sku_name` | text | — | Short display name |
| `revenue_pkr_m` | float | PKR m | Gross revenue over the period |
| `units` | int | units | Units sold |
| `margin_pct` | float | % | Gross margin |
| `returns_pkr_m` | float | PKR m | Value returned over the period |
| `net_revenue_pkr_m` | float | PKR m | `revenue_pkr_m − returns_pkr_m` |

**Two notes:**

- A hierarchy chart needs a **tree**: every child has exactly one parent, and
  children sum to the parent (slide 42). Check that before you draw.
- `net_revenue_pkr_m` is the measure the treemap should use, and it is the
  one that can go below zero. Slide 49: negatives have no area.

---

## `shares_eight.csv` — the pie-ranking stimulus (Part C)

The eight largest sub-categories of the same catalogue, as shares.

| Column | Type | Unit | Meaning |
|---|---|---|---|
| `slice` | text | — | `A`–`H`, the label used in the experiment |
| `subcategory` | text | — | Which sub-category each letter is |
| `share_pct` | float | % | Share of the eight-category total. Sums to exactly 100 |

The letters are **not** in rank order. That is deliberate — a pie cannot be
reordered without changing what it looks like it means (slide 34).

---

## The nine Part A cases

Each file backs one published claim. The recipe each analyst followed is in
`TASKS.md`.

### `case01_orders_stringdate.csv` — 24 rows
| Column | Type | Meaning |
|---|---|---|
| `month` | text | Calendar month, written `YYYY-M` with no zero padding |
| `orders` | int | Orders placed that month |
| `branch` | text | Branch name — constant |

### `case02_shop_closed.csv` — 69 rows
| Column | Type | Meaning |
|---|---|---|
| `date` | text | Trading date, `YYYY-MM-DD`. **Only trading days are recorded** |
| `sales_pkr_k` | int | Sales that day, PKR thousands |

### `case03_bandwidth_levels.csv` — 1,237 rows
| Column | Type | Meaning |
|---|---|---|
| `ts` | text | Hour, `YYYY-MM-DD HH:MM:SS` |
| `concurrent_users` | int | Users connected **at that instant** — a level, not a count of arrivals |
| `bytes_served` | int | Bytes served **during** that hour — a flow |

### `case04_intervention_lag.csv` — 214 rows
| Column | Type | Meaning |
|---|---|---|
| `date` | text | Calendar day |
| `conversion_pct` | float | Sessions converting to an order, % |

### `case05_revenue_window.csv` — 36 rows
| Column | Type | Meaning |
|---|---|---|
| `month` | text | `YYYY-MM`, 2023-01 to 2025-12, complete |
| `revenue_pkr_m` | float | Revenue that month, PKR millions |

### `case06_monthly_partial.csv` — 284 rows
| Column | Type | Meaning |
|---|---|---|
| `date` | text | Calendar day |
| `orders` | int | Orders placed that day |

### `case07_stacked_products.csv` — 36 rows
| Column | Type | Meaning |
|---|---|---|
| `month` | text | `YYYY-MM`, 2023-01 to 2025-12, complete |
| `product_a` … `product_d` | float | Revenue by product line, PKR millions |

The four products are exclusive and exhaustive: every rupee is in exactly
one of them, so a stacked chart of them is at least *legal*.

### `case08_channel_attrib.csv` — 4,000 rows
| Column | Type | Meaning |
|---|---|---|
| `customer_id` | text | One row per customer |
| `touch_search` … `touch_direct` | bool | Whether that channel touched this customer at any point before purchase |
| `revenue_pkr` | int | What the customer spent |

### `case09_premium_share.csv` — 8 rows
| Column | Type | Meaning |
|---|---|---|
| `quarter` | text | `2024Q1` … `2025Q4` |
| `total_revenue_pkr_m` | float | All revenue that quarter, PKR millions |
| `premium_revenue_pkr_m` | float | The premium line's part of it |

---

## Citing this data

Everything here was generated for **CDB601220 Data Visualization, Week 4,
Superior University Lahore**. If you quote a number from it in a report, say
that it is synthetic course data. Do not present it as a finding about any
real business.
