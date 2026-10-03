# Week 2 — Assignments: Visual Perception

Five tasks on **how the human brain processes visual information** — and what that forces you to do when you
design a chart.

**CLO1 — Identify how the human brain processes visual information.**

| Task | Topic | Data |
|---|---|---|
| 1 | Preattentive attributes and visual search | `stimuli_search.csv` |
| 2 | Gestalt principles of grouping | `stimuli_gestalt.csv` |
| 3 | Cognitive load and the data-ink ratio | `car_crashes.csv`, `tips.csv` |
| 4 | Channel effectiveness — run the experiment yourself | `channel_trials.csv`, `iris.csv` |
| 5 | Capstone: redesign one chart for the human visual system | `gapminder.csv` or `diamonds.csv` |

**Setup**

```bash
pip install pandas numpy matplotlib seaborn jupyter ipykernel

cd week2/assignments
python3 download_assignment_data.py
```

The script downloads five public datasets **and generates three stimulus files** with a fixed seed
(`SEED = 42`). The stimuli are generated, not downloaded, because preattentive search and Gestalt grouping
need controlled displays where exactly one feature varies at a time — a normal dataset cannot show the
effect. Everyone gets identical stimuli, so your numbers are comparable with a classmate's. **Do not change
the seed.**

**What you hand in:** one Jupyter notebook per task (`task1.ipynb` … `task5.ipynb`), with your code, your
charts, and a markdown cell under each chart explaining *what the eye does and why*. In this week the
explanation is worth **more** than the chart — the whole point is the reasoning about perception. Notebooks
must be submitted **with outputs**, and must run top to bottom.

Tasks 1, 2 and 4 ask you to time or question a **real human being**. One classmate, flatmate or family
member is enough. Record who they were (first name or "a classmate" is fine), what you asked, and what they
said. Invented results are worth zero, and they are obvious — real reaction times are noisy.

---

## The rules

**New in Week 2 — applied to every chart you produce:**

- **Name the attribute.** Whenever you use colour, size, shape or position to carry meaning, say which
  preattentive attribute you are relying on and whether it is suited to the data type.
- **One pop-out per chart.** If everything is highlighted, nothing is. Each chart gets at most one element
  that pops out, and it must be the thing your title claims.
- **Say which Gestalt principle you used.** Grouping, spacing, enclosure and connection are design
  decisions. Name the one you relied on, every time.
- **Count your ink.** For any chart you de-clutter, state what you removed and why it was not carrying
  information.
- **Grey is a colour choice.** Context goes grey; the message gets the one strong colour.
- **A deliberately bad chart must say so.** Put `BAD EXAMPLE` in its title. An unlabelled bad chart is
  marked as a mistake, not as a demonstration.
- **Build every chart with the object-oriented API** — `fig, ax = plt.subplots()`, then methods on `ax`.
  `plt.plot()` and `plt.bar()` are not allowed.

**Still in force from Week 1:**

- The title states your finding, not the axis names.
- Bars start at zero.
- Never two y-axes.
- Colour must mean something, or be removed.
- Label selectively, not every point.
- Say so on the chart if you excluded any rows.

---

## Quick reference

**Preattentive attributes** — processed in under ~250 ms, in parallel, across the whole visual field,
*before* conscious attention arrives. You do not search for them; they arrive.

| Family | Attributes |
|---|---|
| Colour | hue, intensity (saturation / lightness) |
| Form | shape, size, orientation, length, width, curvature, added marks, enclosure |
| Position | 2-D position, spatial grouping |
| Motion | flicker, direction of motion |

Two facts that matter more than the list:

1. **A single preattentive attribute is found in constant time.** Doubling the number of distractors does
   not slow you down. The search is *parallel*.
2. **A conjunction of two attributes is not preattentive.** Finding the item that is both red *and* a circle
   requires serial search, and the time grows with the number of items. This is the single most useful
   result in the whole week, and Task 1 makes you measure it.

**Gestalt principles of grouping** — the brain's default rules for deciding what belongs with what.

| Principle | The brain assumes… |
|---|---|
| Proximity | things placed close together belong together |
| Similarity | things that look alike belong together |
| Enclosure | things inside a shared boundary belong together |
| Closure | an incomplete familiar shape is completed |
| Continuity | items along a smooth path belong to that path |
| Connection | things joined by a line belong together — this **beats** proximity and similarity |

**Cognitive load** (Sweller). Working memory holds roughly **4 ± 1** chunks at once. Three kinds of load:

| Type | What it is | What you do about it |
|---|---|---|
| Intrinsic | difficulty inherent in the data itself | cannot be removed; can be sequenced |
| Extraneous | load added by your design — chart junk, legends, decoding work | **remove it. This is your job.** |
| Germane | effort that goes into actually understanding | protect it; it is the point |

**Data-ink ratio** (Tufte):

```
                   ink used to show the data
data-ink ratio = ─────────────────────────────
                     total ink in the graphic
```

Maximise it — but not past the point where the chart becomes hard to read. Removing a gridline that was
helping the reader compare is not a saving.

**Channel effectiveness** for *quantitative* data, best → worst:

```
position  >  length  >  angle  >  area  >  volume  >  colour
```

This ranking is not taste. It comes from Cleveland & McGill's experiments measuring how accurately people
judge ratios. Task 4 makes you reproduce it.

**The template every chart starts from**

```python
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(df["x"], df["y"], color="#bbbbbb")          # context in grey
ax.scatter(hit["x"], hit["y"], color="#ee6677")        # one pop-out, in colour
ax.set_title("Finding goes here, not 'y by x'", loc="left")
ax.set_xlabel("...")
ax.set_ylabel("...")
for side in ("top", "right"):
    ax.spines[side].set_visible(False)                 # extraneous ink
fig.savefig("chart.png", dpi=300, bbox_inches="tight")
```

---

## Task 1 — Preattentive attributes and visual search (`stimuli_search.csv`)

2,430 rows describing **90 trials**. One row per item on screen.

Columns: `trial`, `condition`, `set_size`, `target_present`, `item_index`, `x`, `y`, `colour`, `shape`,
`is_target`.

Three conditions, and the difference between them is the whole task:

| Condition | Target | Distractors |
|---|---|---|
| `colour` | red circle | blue circles — differ by **hue only** |
| `shape` | blue square | blue circles — differ by **shape only** |
| `conjunction` | red circle | red squares **and** blue circles — every distractor shares *exactly one* of the target's two features |

Set sizes are 9, 16, 25, 36 and 49, with target present and absent, three repeats each.

**Do this:**

1. **Render the trials.** Write one function that takes a `trial` number and draws it on an `ax`: items at
   `x`/`y`, coloured and shaped as the columns say, no axes, no ticks, no title. Verify it by drawing one
   trial from each condition at `set_size=25` in a 1×3 figure.
2. **Run the experiment on a real person.** Pick **18 trials** — two per (condition × set_size) cell, one
   target-present and one target-absent. Show each trial, ask "is the target there, yes or no?", and record
   their response time with `time.perf_counter()` and whether they were correct. Put the results in a
   DataFrame and save it as `search_results.csv`. Tell them the target before each block, not during.
3. **Plot response time against set size**, one line per condition, target-present trials only. Use the
   object-oriented API. This is the chart the whole task exists for.
4. **Read your own slopes.** Fit a straight line to each condition (`numpy.polyfit`, degree 1) and report
   the slope in **milliseconds per additional item**. State which conditions are flat and which rises. A
   flat slope means parallel, preattentive processing; a rising slope means serial search.
5. **Explain the conjunction result.** In your own words, why can the eye find "red" instantly and "circle"
   instantly, but not "red *and* circle"? Then name one chart you have made — in Week 1 or anywhere — where
   you asked a reader to do a conjunction search without realising it.

**Watch out for:** target-*absent* trials are slower than target-present ones even in the preattentive
conditions, because the reader has to satisfy themselves nothing is there. Keep the two separate; do not
average them together. Your `n` is small, so do not over-claim — report the slope and say it is one reader.

**The question to answer:** your colour and shape slopes should be near zero, and your conjunction slope
clearly positive. If a slope came out the "wrong" way, say so honestly and give a reason (too few trials,
the reader learned the layout, a cluttered display). A result that disagrees with the theory and is
explained is worth more than a tidy result you massaged.

---

## Task 2 — Gestalt principles of grouping (`stimuli_gestalt.csv`)

284 rows across **six panels**, one per principle. Columns: `panel`, `group`, `x`, `y`, `colour`, `shape`,
`size`, `connector`.

The data is deliberately almost the same in every panel. What changes is the *arrangement*, so any grouping
a reader sees is produced by your layout, never by the numbers.

| Panel | Items | Groups | How grouping is signalled |
|---|---|---|---|
| `proximity` | 48 | 4 | four separated clumps, identical styling |
| `similarity` | 48 | 4 | one uniform cloud, grouped by colour alone |
| `enclosure` | 48 | 4 | four clumps — **you** draw the boundaries |
| `continuity` | 48 | 2 | items along two crossing curves |
| `closure` | 44 | 2 | two arcs with a deliberate gap |
| `connection` | 48 | 24 pairs | pairs joined by `connector`; the two in a pair are *different colours* and not necessarily close |

**Do this:**

1. **Draw all six panels** in one 2×3 figure. For `enclosure`, add the four boundaries yourself with
   `matplotlib.patches.Rectangle` (no fill, grey edge). For `connection`, draw a line between the two items
   sharing each `connector` value. Give each panel the name of its principle as the title.
2. **Ask a real person, panel by panel:** "how many groups do you see?" Record their answer against the
   true group count from the `group` column. Build a small table: panel, principle, true groups, perceived
   groups, match (yes/no).
3. **Make the principles fight each other.** The `connection` panel is built so that connection
   (the line) opposes both similarity (the two ends are different colours) and proximity (partners are not
   the nearest item). Draw it twice — once with the connecting lines, once without — and ask your reader to
   group it both times. Which principle won? **Connection should beat both.** Report what actually happened.
4. **Find the Gestalt principle in a real chart.** Using `tips.csv`, draw one chart where you use
   **proximity** to group (for example a grouped bar chart where the within-group gap is smaller than the
   between-group gap). Then redraw it with the two gaps made equal. Explain what the reader loses in the
   second version — the data has not changed at all.
5. **Name where each principle already lives in a chart you know.** One sentence each for all six:
   proximity, similarity, enclosure, closure, continuity, connection. Use real chart features — legends,
   small multiples, axis bands, a line chart's line, a highlighted region, a table's rules.

**Watch out for:** the `closure` panel has 44 items, not 48 — the gap *is* the stimulus. Do not "fix" it.
And in `similarity`, do not also separate the colours spatially: if you do, you have tested proximity
instead, and the panel no longer shows anything.

**The question to answer:** a legend forces the reader to hold a colour in working memory, carry it across
the chart, and match it. Which Gestalt principle does direct labelling use instead, and why is that cheaper
for the brain? Answer in terms of load, not preference.

---

## Task 3 — Cognitive load and the data-ink ratio (`car_crashes.csv`, `tips.csv`)

`car_crashes.csv`: 51 rows (50 states + DC). Columns: `total`, `speeding`, `alcohol`, `not_distracted`,
`no_previous`, `ins_premium`, `ins_losses`, `abbrev`.

**Do this:**

1. **Build an overloaded chart on purpose.** Draw all 51 states as a bar chart of `total`, and pile on the
   extraneous load: every bar a different colour, all 51 labels rotated, heavy gridlines in both directions,
   a box frame, a legend with 51 entries, a drop shadow or 3-D effect if your backend will do it, and a
   title that names the axes. Title it `BAD EXAMPLE`. Save it.
2. **Count the load.** List every element in that chart and classify each one as **intrinsic**,
   **extraneous** or **germane**. Then estimate its data-ink ratio: count the marks that encode a number,
   count the total marks, and show the fraction. An estimate with its working shown is fine; a number on its
   own scores zero.
3. **Strip it down, one step at a time.** Produce a **five-panel** figure showing the same data getting
   lighter at each step. Suggested order — justify yours if it differs:
   remove the legend → remove the frame and one gridline axis → drop to a single hue → sort the bars →
   label only what matters. Under each panel, state what you removed and which kind of load it was.
4. **Respect the 4 ± 1 limit.** Working memory holds about four chunks. Redraw the 51 states so the reader
   never has to hold more than four things at once — group into regions, show the top five and pool the
   rest as "other 46 states", or use a small multiple. Say which chunking you chose and what it costs: every
   chunking hides something, and you must name what.
5. **Over-strip it.** Remove too much — no axis labels, no tick values, no units — and show why the
   data-ink ratio is not something to maximise blindly. Title it `BAD EXAMPLE`. Then state the stopping
   rule you would give a colleague in one sentence.

**Watch out for:** sorting bars is the single highest-value edit on this chart, and it adds no ink at all.
Notice that in your write-up. Also note that `total`, the percentage columns and the dollar columns are in
three different units — putting them on one axis is a Week 1 violation, not a load problem.

**The question to answer:** using `tips.csv`, find one chart where **adding** ink lowers cognitive load.
(Think about a reference line, a direct label, or an annotation that saves the reader a calculation.) Draw
it, and explain why "maximise data-ink" is a heuristic rather than a rule.

---

## Task 4 — Channel effectiveness, measured (`channel_trials.csv`, `iris.csv`)

30 rows: 5 channels × 6 true ratios. Columns: `trial`, `channel`, `true_ratio`, `value_large`,
`value_small`, `reader_estimate` (blank — you fill it), `absolute_error` (blank — you compute it).

You are going to reproduce Cleveland & McGill's result on a very small scale.

**Do this:**

1. **Encode each trial five ways.** For a given pair of values, write five tiny chart functions that show
   that pair using one channel each:

   | Channel | Encoding |
   |---|---|
   | `position` | two dots on a common scale |
   | `length` | two bars from a common zero baseline |
   | `angle` | two wedges of a pie |
   | `area` | two circles, **area** proportional to value |
   | `colour` | two squares, lightness proportional to value |

   No axis labels, no tick values, no numbers anywhere — the reader must judge from the channel alone.
2. **Run all 30 trials on a real person.** Show each chart and ask: "the smaller one is what percentage of
   the larger?" Record their answer in `reader_estimate`. Shuffle the trial order so they cannot learn the
   pattern, and do not tell them the true answers until the end.
3. **Compute the error** as `absolute_error = abs(reader_estimate/100 - true_ratio)` and save the completed
   file as `channel_results.csv`.
4. **Rank the channels by mean absolute error** and plot the ranking — one bar per channel, sorted, zero
   baseline, error shown. Compare your ranking against
   `position > length > angle > area > volume > colour`. Where does yours agree, and where does it not?
5. **Apply it.** Using `iris.csv`, draw the same finding twice: once encoding `petal_length` by a
   **high-ranking** channel and once by a **low-ranking** one. Same data, same message, two channels. State
   which one you would publish and why — in terms of how accurately a reader can decode it, not which looks
   nicer.

**Watch out for:** in `ax.scatter`, the `s` argument is **area**, not radius. If you set `s` proportional to
the value you have encoded area correctly; if you set it proportional to the square of the value you have
accidentally built the classic area lie. Say which you did. For the colour channel, use a sequential
lightness ramp — a rainbow has no perceptual order and would test something else entirely.

**The question to answer:** with six ratios and one reader you have 30 data points and no statistical power.
State plainly what your experiment can and cannot support. Then say why the published ranking is still worth
following even when your own small sample disagrees with it.

---

## Task 5 — Capstone: redesign one chart for the human visual system

Take **one** chart and rebuild it so that every design decision is justified by something from this week.
Use `gapminder.csv` (142 countries × 12 years) or `diamonds.csv` (53,940 rows — sample it, and say so).

**Do this:**

1. **Start from a genuinely bad chart.** Either reuse your `BAD EXAMPLE` from Task 3, or build a new one:
   a spaghetti line chart of all 142 countries, or all 53,940 diamonds plotted raw. Title it `BAD EXAMPLE`
   and state the one question a reader should be able to answer from it.
2. **Write a perception audit of that chart** as a markdown table, before you fix anything:

   | Row | What to write |
   |---|---|
   | Preattentive | which attributes are in play, and whether any is doing useful work |
   | Pop-out | what pops out, and whether it is what the title claims |
   | Gestalt | which principle the layout triggers, and whether it groups the right things |
   | Cognitive load | each element classified intrinsic / extraneous / germane |
   | Channels | each variable's channel, and its rank for that data type |
   | Working memory | how many chunks the reader must hold at once |

3. **Rebuild it.** One figure, one message. Required:
   - exactly **one** pop-out element, carrying the message in the title;
   - context in grey, message in a single strong colour;
   - **one named Gestalt principle** doing the grouping — say which in the notebook;
   - the most important variable on the **highest-ranking channel** available;
   - no information carried by colour alone;
   - `n`, and any excluded or missing rows, declared on the figure.
4. **Fill in the same audit table for your redesign**, so the before and after sit side by side.
5. **Test it on a human.** Show the redesign — not the original — to someone who has not seen the data, and
   ask them to say in one sentence what it shows. Write their sentence down verbatim. Does it match your
   title? If not, say which part of the design misled them and what you would change next.
6. **Export** `perception_redesign.png` at **300 DPI** with `bbox_inches="tight"`.

**Self-audit**

- [ ] Every chart built with `fig, ax` (no `plt.plot` / `plt.bar`)
- [ ] Exactly one pop-out element, and it carries the title's message
- [ ] The Gestalt principle used is named in the notebook
- [ ] Most important variable on the highest-ranking available channel
- [ ] Every element classified as intrinsic / extraneous / germane
- [ ] Reader never holds more than ~4 chunks at once
- [ ] No information carried by colour alone
- [ ] Context greyed, message coloured
- [ ] `n` and exclusions declared on the figure
- [ ] Title states a finding
- [ ] A real reader's one-sentence reading is recorded verbatim

**The question to answer:** name one thing your redesign makes *harder* to see. Every design decision
trades something away — greying the context, chunking the categories, or choosing one message all hide
something that was visible before. A redesign with no stated cost has not been thought through.

---

## Marking guide

| | Weight |
|---|---|
| Perception reasoning: preattentive attributes, Gestalt and load named correctly and used to justify decisions | 30% |
| Experiments actually run on a real reader, with results reported honestly — including results that disagree | 25% |
| Cognitive load and data-ink: elements classified, clutter removed, chunking justified | 20% |
| Correct technique: object-oriented API, five-panel and multi-panel figures, 300 DPI export | 15% |
| Craft: titles that state findings, one pop-out, grey for context, clear labels | 10% |

**Automatic deductions:**

- invented or implausible experiment results (reaction times with no noise, errors that are all zero)
- `plt.plot()`, `plt.bar()` or other implicit-pyplot drawing instead of `ax` methods
- more than one pop-out element in a final chart
- a Gestalt principle used but not named
- a data-ink ratio stated without its working
- colour as the only carrier of meaning
- a bad example that is not labelled `BAD EXAMPLE`
- a rainbow palette used for ordered data in a final chart
- excluded or missing rows not declared on the chart
- a dual y-axis, or a truncated bar baseline
- a required export saved at less than 300 DPI
- changing `SEED` in `download_assignment_data.py`
