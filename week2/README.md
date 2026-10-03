# Week 2 — Visual Perception

Datasets and assignments for Week 2: preattentive attributes, Gestalt principles, and cognitive load.

**CLO1 — Identify how the human brain processes visual information.**

← [Back to the course index](../README.md)

## Run the assignments

```bash
cd week2/assignments
python3 download_assignment_data.py
jupyter notebook
```

Requires `pandas`, `numpy`, `matplotlib`, `seaborn`, `jupyter`, `ipykernel`.

## Contents

| Path | What it is |
|---|---|
| `assignments/TASKS.md` | Five student tasks and the marking guide |
| `assignments/download_assignment_data.py` | Downloads five datasets **and generates three stimulus files** |
| `assignments/data/` | Created by the script — see the two tables below |

## Assignments

| Task | Topic | Data | Practises |
|---|---|---|---|
| 1 | Preattentive attributes | `stimuli_search.csv` | Parallel vs serial search; why a conjunction is not preattentive |
| 2 | Gestalt principles | `stimuli_gestalt.csv` | Six grouping principles, and which one wins when they conflict |
| 3 | Cognitive load | `car_crashes.csv`, `tips.csv` | Intrinsic / extraneous / germane load; data-ink ratio; the 4 ± 1 limit |
| 4 | Channel effectiveness | `channel_trials.csv`, `iris.csv` | Reproducing the Cleveland & McGill ranking by experiment |
| 5 | Capstone redesign | `gapminder.csv` or `diamonds.csv` | A full perception audit, before and after |

Full briefs and the marking guide are in [`assignments/TASKS.md`](assignments/TASKS.md).

Tasks 1, 2 and 4 require the student to **time or question one real person**. That is deliberate: this week
is about how a brain behaves, and the result is more convincing when it comes out slightly messy.

## The data

**Downloaded** — five free, public datasets:

| File | Rows | Used by | Why this one |
|---|---|---|---|
| `diamonds.csv` | 53,940 | 5 | Large enough to overplot badly, so sampling must be declared |
| `gapminder.csv` | 1,704 | 5 | The classic spaghetti chart — 142 lines to de-clutter |
| `tips.csv` | 244 | 2, 3 | Several categorical columns for proximity grouping |
| `iris.csv` | 150 | 4 | Four numeric columns, clean, good for channel comparisons |
| `car_crashes.csv` | 51 | 3 | Dense table in three different units — the de-cluttering target |

**Generated** — three stimulus files, built with `SEED = 42`:

| File | Rows | Used by | What it holds |
|---|---|---|---|
| `stimuli_search.csv` | 2,430 | 1 | 90 visual-search trials: colour, shape and conjunction conditions at five set sizes |
| `stimuli_gestalt.csv` | 284 | 2 | Six panels — proximity, similarity, enclosure, closure, continuity, connection |
| `channel_trials.csv` | 30 | 4 | 5 channels × 6 ratios, with blank columns for the reader's estimates |

These three are generated rather than downloaded because preattentive search and Gestalt grouping need
controlled displays where exactly one feature varies at a time — no real-world dataset can isolate that. The
fixed seed means every student gets identical stimuli, so results are comparable across the class.

## The ideas being tested

| Idea | Where it appears |
|---|---|
| Preattentive attributes — colour, form, position, motion | Task 1, Task 5 audit |
| Parallel search is constant-time; conjunction search is not | Task 1, steps 3–5 |
| Gestalt grouping, and connection beating proximity and similarity | Task 2 |
| Intrinsic vs extraneous vs germane load | Task 3, steps 2–3 |
| Data-ink ratio, and why maximising it blindly fails | Task 3, steps 2 and 5 |
| Working memory ≈ 4 ± 1 chunks | Task 3, step 4 |
| Channel effectiveness: position > length > angle > area > volume > colour | Task 4 |
| One chart, one pop-out, one message | Task 5 |
