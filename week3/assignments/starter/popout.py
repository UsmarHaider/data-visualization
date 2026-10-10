"""
Week 1, carried forward into code.  (Optional — 5 bonus marks.)

    python3 starter/popout.py

In Week 1 you counted the 3s in a grid of digits, twice: once where they were
hidden and once where they were coloured. The second round took a fraction of
the time, and that difference is the whole of preattentive processing.

This week you build the experiment instead of sitting in it — and then you
run it on five classmates and chart the result. That last step is the point:
perception is a measurable property of a chart, not an opinion about one.

Panels 1 and 2 are written for you. Panels 3 and 4 are yours.
"""

from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vizlib import PALETTE, save_fig, style_defaults   # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
style_defaults()

ROWS, COLS = 12, 18
TARGET = "3"
N_TARGETS = 9
SEED = 1947


def make_grid(seed=SEED):
    """A grid of digits with exactly N_TARGETS threes, in fixed positions."""
    rng = np.random.default_rng(seed)
    others = [d for d in "0123456789" if d != TARGET]
    grid = np.array([[rng.choice(others) for _ in range(COLS)]
                     for _ in range(ROWS)], dtype=object)
    flat = rng.choice(ROWS * COLS, size=N_TARGETS, replace=False)
    for k in flat:
        grid[k // COLS, k % COLS] = TARGET
    return grid


def draw(ax, grid, title, colour=False, size=False, shape=False):
    """
    Draw one panel.

    colour -> targets get the highlight hue   (a preattentive channel)
    size   -> targets are drawn larger        (another one)
    shape  -> targets get a ring behind them  (a third, and it survives
              greyscale printing and colour blindness)
    """
    ax.set_xlim(-0.5, COLS - 0.5)
    ax.set_ylim(-0.5, ROWS - 0.5)
    ax.invert_yaxis()
    ax.axis("off")
    ax.set_title(title, fontsize=10.5, loc="left")
    for r in range(ROWS):
        for c in range(COLS):
            d = grid[r, c]
            hit = d == TARGET
            if shape and hit:
                ax.add_patch(plt.Circle((c, r), 0.40, fill=False,
                                        edgecolor=PALETTE["ink"], lw=1.6))
            ax.text(c, r, d, ha="center", va="center",
                    fontsize=15 if (size and hit) else 11,
                    fontweight="bold" if (size and hit) else "normal",
                    color=PALETTE["highlight"] if (colour and hit)
                    else PALETTE["ink"])


def main():
    grid = make_grid()
    fig, ax = plt.subplots(2, 2, figsize=(13.0, 8.0))

    # ---- panel 1: no pop-out. Serial search — you read every cell.
    draw(ax[0, 0], grid, "1. No channel — you have to read every cell")

    # ---- panel 2: colour. One preattentive channel; the 3s appear at once.
    draw(ax[0, 1], grid, "2. Colour — the targets appear before you look",
         colour=True)

    # ------------------------------------------------------------- TODO 1
    # Panel 3: make the targets pop out using SIZE ONLY — no colour.
    # Then answer: is size as fast as colour? Wilke ch. 20 says it is not.
    # Time yourself and find out.
    draw(ax[1, 0], grid, "3. TODO — size only, no colour")

    # ------------------------------------------------------------- TODO 2
    # Panel 4: redundant coding — TWO channels at once (colour AND shape).
    # This is the Week 2 accessibility rule in its original perceptual form:
    # a reader with deuteranopia loses panel 2 entirely and keeps panel 4.
    draw(ax[1, 1], grid, "4. TODO — colour AND shape together")

    fig.suptitle(f"Count the {TARGET}s. Same {N_TARGETS} targets in all four "
                 f"panels, same positions.",
                 x=0.006, ha="left", fontsize=13.5, fontweight="bold",
                 color=PALETTE["ink"])
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    out = save_fig(fig, os.path.join(ROOT, "popout_panels.png"),
                   f"{ROWS}x{COLS} grid, {N_TARGETS} targets, seed {SEED}. "
                   f"Week 1 activity, rebuilt in Matplotlib.")
    plt.close(fig)
    print("wrote", out)

    # ------------------------------------------------------------- TODO 3
    # The experiment. Show each panel to FIVE classmates, one at a time, in a
    # different random order for each person, and time how long they take to
    # count the targets. Record seconds and whether they got 9.
    #
    # Then chart it: panel on the x-axis, mean seconds on the y-axis, with the
    # individual times as a strip plot over a faded bar — the
    # "summary plus raw data" pattern from slide 44, which is the right choice
    # for n = 5 because five points is small enough to simply show.
    #
    # Rules for the chart:
    #   - the y-axis starts at zero (it is a bar chart of a magnitude)
    #   - the title states your finding, not "Time by panel"
    #   - the source note carries n = 5 and how you randomised the order
    #
    # Then write three sentences: which channel was fastest, which was
    # slowest, and whether panel 4 cost anything in speed compared with
    # panel 2. (It should not. That is why redundant coding is close to free.)
    print("TODO 3: run the timing experiment on five people and chart it.")


if __name__ == "__main__":
    main()
