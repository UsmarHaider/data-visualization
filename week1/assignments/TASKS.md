# Week 1 — Assignments

Five datasets, five tasks. Each task practises a specific lesson from the Week 1 lecture.

**Setup**

```bash
cd assignments
python3 download_assignment_data.py
```

**What you hand in:** one Jupyter notebook per task, containing your code, your charts, and a short
markdown cell under each chart explaining *why you chose that chart type*. The explanation is worth as
much as the chart.

**The rules from the lecture apply to every chart you produce:**

- The title states your finding, not the axis names.
- Bars start at zero.
- Never two y-axes.
- Colour must mean something, or be removed.
- Label selectively — not every point.
- Say so on the chart if you excluded any rows.

---

## Task 1 — Prove why we visualize (`datasaurus.csv`)

1,846 rows, 3 columns: `dataset`, `x`, `y`. It contains **13 different datasets** of 142 points each.

**Do this:**

1. Compute the mean of `x`, mean of `y`, standard deviation of both, and the correlation between them —
   **for each of the 13 datasets**. Present it as one table.
2. Look at your table. Write down what you would conclude if the table were all you had.
3. Now plot all 13 as a grid of scatter plots.
4. Write a short paragraph on what you actually found.

**The question to answer:** we saw this effect with Anscombe's 4 datasets. Does having 13 datasets, and
142 points each instead of 11, make the summary statistics any more trustworthy? Why or why not?

---

## Task 2 — Trends, and the spaghetti problem (`gapminder.csv`)

1,704 rows: 142 countries × 12 years (1952–2007, every 5 years). Columns: `country`, `continent`, `year`,
`lifeExp`, `pop`, `gdpPercap`. No missing values — this one is clean, so there is nowhere to hide.

**Do this:**

1. **Make the messy chart on purpose.** Plot life expectancy over time as one line per country — all 142,
   with a legend. Keep it in your notebook and write down everything wrong with it.
2. **Fix it two different ways:**
   - **(a)** Aggregate — one line per continent instead of per country.
   - **(b)** Highlight — keep all 142 lines, but grey them out and colour only 3 countries you find
     interesting. Label those 3 directly on the chart, with no legend.
3. Compare (a) and (b) in writing. What can each one show that the other cannot?
4. Build **one** chart that answers: *has the gap between the richest and poorest countries narrowed
   since 1952?* You choose the chart type — justify it.

**Watch out for:** `gdpPercap` is extremely skewed. Plot a histogram of it and you will see why. Find out
what a log scale does to that chart and decide whether to use one.

---

## Task 3 — Distributions and relationships (`penguins.csv`)

344 penguins from 3 species on 3 islands. Columns: `species`, `island`, `bill_length_mm`, `bill_depth_mm`,
`flipper_length_mm`, `body_mass_g`, `sex`.

**This dataset has missing values** — 2 penguins are missing all four measurements and 11 are missing
`sex`. Find them first, decide what to do, and **state your decision on the charts**.

**Do this:**

1. One chart showing the **distribution** of body mass. What shape is it? Is it one hump or more?
2. Redraw it split by species. Does that explain the shape you saw in step 1?
3. One **scatter plot** of bill length against bill depth, coloured by species. Something strange happens
   here: across *all* penguins the two measurements look negatively related, but *within* each species
   they are positively related. Draw it, then explain what is going on.
4. One chart comparing average body mass across species **and** sex.

**Step 3 is the important one.** The effect has a name — look up "Simpson's paradox" once you have drawn
it — and it is the best possible argument for why you plot your groups separately.

---

## Task 4 — Pick the right chart, five times (`mpg.csv`)

398 cars from 1970–1982. Columns: `mpg`, `cylinders`, `displacement`, `horsepower`, `weight`,
`acceleration`, `model_year`, `origin`, `name`. `horsepower` is missing for 6 cars.

For **each** question below, choose a chart type, draw it, and write one sentence justifying the choice.
Different questions should not all get the same chart.

1. Did cars get more fuel-efficient between 1970 and 1982?
2. Do American, European and Japanese cars differ in fuel efficiency?
3. What is the relationship between a car's weight and its fuel efficiency?
4. How is the number of cylinders distributed across the fleet?
5. Is the improvement in question 1 explained by question 3? (i.e. did cars get lighter?)

**Then:** take whichever of your five charts you think is the weakest and redraw it. Say what you changed.

---

## Task 5 — A real time series (`flights.csv`)

144 rows: monthly airline passenger totals from 1949 to 1960. Columns: `year`, `month`, `passengers`.

Small and clean, so all the difficulty is in the chart design.

**Do this:**

1. Plot passengers over time as a single line. You will need to combine `year` and `month` into one
   ordered time axis first — this is the real work of the task.
2. Your chart shows **two** patterns at once: a long-term rise and a repeating within-year cycle.
   Build a second chart that isolates the seasonal cycle alone (hint: one line per year, months on the
   x-axis).
3. Which month is consistently busiest? Build a chart that makes this obvious at a glance.
4. Write down which of your three charts you would put in a report, and why the other two do not belong
   in the same report.

**Question to answer in writing:** the seasonal swing gets visibly bigger every year. Is that because the
seasonality is growing, or just because the airline is growing? Suggest a chart that would settle it.

---

## Marking guide

| | Weight |
|---|---|
| Chart type fits the question, and the justification is sound | 30% |
| Each chart carries one clear message, stated in its title | 25% |
| Correct data processing — including honest handling of missing values | 25% |
| Craft: labels, zero baselines, readable colour, no chart junk | 20% |

**Automatic deductions:** a dual y-axis, a truncated bar baseline presented without comment, a pie chart
with more than four slices, or a legend with more entries than a reader could use.
