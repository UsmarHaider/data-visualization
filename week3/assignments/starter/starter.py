"""
Part D — starter skeleton.

    python3 starter/starter.py

It runs as given and produces an ugly, wrong figure. That is the point: you
have something on screen in ten seconds, and every TODO below makes it less
wrong. Work top to bottom.

Rule for this course, from slide 15: every figure starts with
`fig, ax = plt.subplots()`. There is no `plt.plot()` anywhere in this file and
there should be none in yours.
"""

from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vizlib import MARKERS, PALETTE, save_fig, style_defaults   # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
style_defaults()          # slide 26: set the look once, not on every chart
C = PALETTE["series"]

# Your audit trail. Every exclusion goes in here with a rule and a count, and
# it gets printed at the end so you can paste it into Part E.
LOG: dict[str, str] = {}


# =============================================================================
#  STEP 0 — look at the data before you plot a single thing
# =============================================================================
def inspect(df):
    """
    Run this once, read the output, then comment the call out.

    Nine things are wrong with this file and none of them is announced.
    Four of them are visible in this output alone.
    """
    print(df.info())
    print(df.describe().T)
    print("\nward values:")
    print(df.ward.value_counts())
    print("\nadmit_date, first 10:")
    print(df.admit_date.head(10).tolist())
    print("\nsuspicious maxima:")
    for col in ["heart_rate", "bmi", "spo2", "los_days"]:
        print(f"  {col:12s} min {df[col].min():>8.1f}   max {df[col].max():>8.1f}")


# =============================================================================
#  STEP 1 — clean it, and write down every rule
# =============================================================================
def clean(df):
    LOG["rows loaded"] = f"{len(df):,}"

    # ---------------------------------------------------------------- TODO 1
    # `ward` is spelled several ways for four real wards. Conform it into a
    # new column `ward_clean` BEFORE anything is grouped — otherwise every
    # groupby splits each ward across its spellings.
    #
    # Hint: .str.strip().str.lower() first, then .map() a dictionary.
    # Check: df.ward_clean.nunique() must be 4, and .isna().sum() must be 0.
    df["ward_clean"] = df.ward          # <- replace this line
    LOG["ward spellings conformed"] = "TODO"

    # ---------------------------------------------------------------- TODO 2
    # `admit_date` arrives in three text formats from three systems. Parse it
    # into a real datetime column `admit_dt`.
    #
    # Do NOT just call pd.to_datetime(df.admit_date). It will either raise or
    # guess row by row, and 03/02/2026 will come back as 2 March.
    # Hint: parse each format with format=..., errors="coerce", then fillna.
    LOG["dates parsed"] = "TODO"

    # ---------------------------------------------------------------- TODO 3
    # `bmi` uses sentinel values for "missing". Find them (look at the max),
    # replace them with np.nan, and record how many and what the mean moves
    # from and to. The change is larger than you expect.
    LOG["bmi sentinels removed"] = "TODO"

    # ---------------------------------------------------------------- TODO 4
    # `heart_rate` contains device faults. Decide a physiologically defensible
    # range, apply it, and LOG THE RULE AND THE COUNT.
    #
    # This is the ethics mark. Removing them is correct. Removing them
    # silently is not. Slide 45, and Part E item 3.
    LOG["heart-rate device faults removed"] = "TODO"

    # ---------------------------------------------------------------- TODO 5
    # One column in this file is computed from two others, so its correlation
    # with them is arithmetic, not a discovery. Find it (slide 46 names the
    # pair) and exclude it from the heatmap in panel 4.
    LOG["derived column excluded"] = "TODO"

    return df


# =============================================================================
#  STEP 2 — lay the figure out BEFORE you draw anything
# =============================================================================
def build_figure(df):
    fig, ax = plt.subplots(2, 2, figsize=(12.6, 8.4))

    # ------------------------------------------------------- panel 1 (0, 0)
    # TODO 6: a distribution of one numeric column.
    #   - try at least three bin counts before you believe one
    #   - one of the columns in this file is bimodal; find it, and make the
    #     two populations visible
    #   - print the chosen bins or binwidth ON the panel
    a = ax[0, 0]
    a.hist(df.systolic)                       # <- no bins argument. Fix that.
    a.set_title("TODO: a title that states the finding, not the column name")

    # ------------------------------------------------------- panel 2 (0, 1)
    # TODO 7: compare a measure across ward_clean.
    #   - one measure in this file is so right-skewed that a linear box plot
    #     collapses to a line. Use a log scale, or report the median.
    #   - do NOT pass showfliers=False without declaring it in Part E.
    #   - sort the wards by their median, not alphabetically.
    b = ax[0, 1]
    sns.boxplot(data=df, x="ward_clean", y="los_days", ax=b)
    b.set_title("TODO")

    # ------------------------------------------------------- panel 3 (1, 0)
    # TODO 8: scatter the ONE pair worth plotting.
    #   Build panel 4 first, read the heatmap, and let it tell you which pair.
    #   That is what a heatmap is for: it is a screening tool, not a result.
    #   - use shape as well as colour if you split by a category
    #   - 10,000 points will be a solid blob; subsample or set alpha
    c = ax[1, 0]
    c.scatter(df.bmi, df.chol_mmol_l)
    c.set_title("TODO")

    # ------------------------------------------------------- panel 4 (1, 1)
    # TODO 9: the correlation heatmap, done to the rules from slides 46-47.
    #   - cmap="RdBu_r", vmin=-1, vmax=1, center=0      (a correlation has a sign)
    #   - mask the upper triangle                        (it says everything twice)
    #   - annot=True, fmt=".2f"
    #   - exclude the derived column you found in TODO 5
    d = ax[1, 1]
    cols = ["age", "systolic", "diastolic", "map_mmhg", "heart_rate",
            "spo2", "bmi", "chol_mmol_l", "glucose_mmol_l", "los_days"]
    sns.heatmap(df[cols].corr(), ax=d)        # <- six arguments missing
    d.set_title("TODO")

    # ------------------------------------------------------------- TODO 10
    # Finish the figure. The last five lines are what make it readable:
    #   - fig.suptitle() stating the overall finding
    #   - spines off on every panel: for p in ax.flat: p.spines[...]...
    #   - fig.tight_layout()
    return fig


# =============================================================================
def main():
    df = pd.read_csv(os.path.join(ROOT, "data", "vitals_10k.csv"))

    inspect(df)            # <- read the output, then comment this out
    df = clean(df)
    fig = build_figure(df)

    # TODO 11: the source note. It must carry n, the exclusion rules with
    # counts, and every parameter you chose. See the reference figure's note.
    note = "TODO: n = ... · ... removed as ... · bins = ... · synthetic data"

    out = save_fig(fig, os.path.join(ROOT, "partD_figure.png"), note)
    plt.close(fig)
    print("\nwrote", out)

    print("\nYour cleaning log — this is Part E item 3:\n")
    for k, v in LOG.items():
        print(f"  {k:<36} {v}")


if __name__ == "__main__":
    main()
