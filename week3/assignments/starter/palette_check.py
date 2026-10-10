"""
Part C — starter.

    python3 starter/palette_check.py

Runs as given: it simulates three kinds of colour-vision deficiency on two
palettes and saves a before/after swatch sheet. Your job is to swap in your
own palette, read the result honestly, and answer the four questions in the
brief.

Roughly 1 man in 12 and 1 woman in 200 has some form of colour-vision
deficiency. In a cohort of 60 students that is about three people who cannot
read a red/green chart. They will not tell you. The simulation will.
"""

from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vizlib import (PALETTE, save_fig, simulate_cvd, style_defaults,   # noqa: E402
                    verdict, worst_pair)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
style_defaults()

# ----------------------------------------------------------------- TODO 1
# Replace this with a palette you actually like the look of — matplotlib's
# tab10 first four, Excel's defaults, something from a dashboard you admire.
# Do not pick one you already know is safe; the point is to find out.
MY_PALETTE = ["#1F77B4", "#FF7F0E", "#2CA02C", "#D62728"]   # matplotlib tab10
MY_LABEL = "matplotlib tab10, first four"

COURSE_PALETTE = PALETTE["series"] + [PALETTE["series_4th"]]
KINDS = ["normal", "deutan", "protan", "tritan"]


def swatch_sheet(palettes, path):
    fig, axes = plt.subplots(len(palettes), len(KINDS),
                             figsize=(3.0 * len(KINDS), 2.1 * len(palettes)))
    if len(palettes) == 1:
        axes = axes.reshape(1, -1)
    for row, (pal, label) in enumerate(palettes):
        for col, kind in enumerate(KINDS):
            ax = axes[row, col]
            shown = pal if kind == "normal" else simulate_cvd(pal, kind)
            for i, hexc in enumerate(shown):
                ax.add_patch(plt.Rectangle((i, 0), 0.92, 1, color=hexc))
                ax.text(i + 0.46, -0.22, f"S{i+1}", ha="center", fontsize=8,
                        color=PALETTE["ink_soft"])
            ax.set_xlim(-0.1, len(pal))
            ax.set_ylim(-0.4, 1.1)
            ax.axis("off")
            ax.set_title(kind, fontsize=10)
        axes[row, 0].text(-0.05, 1.42, label, transform=axes[row, 0].transAxes,
                          fontsize=11, fontweight="bold", color=PALETTE["ink"])
    fig.suptitle("Prove it, do not claim it", x=0.006, ha="left",
                 fontsize=13, fontweight="bold", color=PALETTE["ink"])
    fig.tight_layout(rect=[0, 0, 1, 0.9])
    out = save_fig(fig, path,
                   "Machado, Oliveira & Fernandes (2009) severity-1.0 "
                   "matrices, applied in linear RGB.")
    plt.close(fig)
    return out


def audit(pal, label):
    """
    The numbers, not the impression.

    `vizlib.worst_pair` measures every pair in OKLab, which is near-uniform,
    so a single threshold means the same thing for every hue. The thresholds
    are documented on `vizlib.delta_e`.
    """
    print(label)
    rows = []
    for kind in ["normal", "deutan", "protan", "tritan"]:
        i, j, a, b, d = worst_pair(pal, kind)
        rows.append((kind, i, j, a, b, d))
        print(f"  {kind:7s} closest pair  S{i} {a} vs S{j} {b}"
              f"   ΔE {d:5.1f}   {verdict(d)}")
    print()
    return rows


def main():
    out = swatch_sheet([(MY_PALETTE, MY_LABEL),
                        (COURSE_PALETTE, "The course palette")],
                       os.path.join(ROOT, "partC_palette.png"))
    print("wrote", out, "\n")

    audit(MY_PALETTE, MY_LABEL)
    audit(COURSE_PALETTE, "The course palette (3 slots + the 4th)")

    # ----------------------------------------------------------- TODO 2
    # Question 3 of the brief: name the worst pair in YOUR palette and the
    # worst pair in the course palette, with its delta E. Both of them have
    # one. Read the numbers above; do not guess from the swatches.

    # ----------------------------------------------------------- TODO 3
    # Question 4: what rule will you follow for the rest of this course when
    # a chart needs more than three categories?
    #
    # The answer is NOT "find a bigger palette". Look at what happens to the
    # course palette's fourth slot above, then think about what you would add
    # to the chart instead of a colour.
    print("TODO: write your rule for charts with more than three categories.")

    # ----------------------------------------------------------- TODO 4
    # Optional, 2 bonus marks: run vizlib.simulate_cvd on a rendered PNG
    # rather than on a list of hex codes — it accepts an (H, W, 3) array.
    # Load your own partD_figure.png with matplotlib.image.imread, simulate
    # deuteranopia on it, and save the result side by side with the original.
    # If you cannot tell your series apart in the simulated version, the
    # figure fails, whatever the palette audit said.


if __name__ == "__main__":
    main()
