"""
vizlib — the small toolkit for the Week 3 task.

Four things live here, and you are expected to import all four:

    PALETTE / style_defaults()   the course palette and rcParams, set once
    lie_factor()                 Tufte's Lie Factor, computed instead of guessed
    simulate_cvd()               prove a palette is colour-blind safe, don't claim it
    match_stats()                force a dataset to exact target statistics

Week 2 told you to use a colour-blind-safe palette and to compute a Lie Factor
by hand. This week you do both in code, which means you can do them on every
figure you produce instead of on the one you were marked on.

Everything here is plain numpy + matplotlib. No new installs.
"""

from __future__ import annotations

import numpy as np

# --------------------------------------------------------------------- palette
# Three categorical hues from Okabe-Ito. This exact three-slot set passes all
# six checks of the course palette validator on a light surface with every
# pair compared (not just adjacent ones): lightness band, chroma floor,
# colour-vision-deficiency separation, normal-vision separation, and 3:1
# contrast against the surface.
#
#   worst all-pairs CVD  dE 11.0 (deuteranopia)
#   worst all-pairs normal dE 18.7
#
# A fourth hue (#CC79A7) is provided for the cases that genuinely need one. It
# drops the CVD margin to dE 7.6 and falls below 3:1 contrast, so whenever you
# use it the chart MUST carry direct labels or a table view. State that in your
# write-up rather than hoping nobody checks.
PALETTE = {
    "series": ["#0072B2", "#D55E00", "#009E73"],
    "series_4th": "#CC79A7",
    "highlight": "#D55E00",
    "muted": "#9AA7B4",
    "ink": "#16202E",
    "ink_soft": "#5B6573",
    "grid": "#DFE6EE",
    "surface": "#FFFFFF",
    # sequential: one hue, light to dark. Never a rainbow.
    "sequential": "Blues",
    # diverging: two hues with a neutral midpoint, for anything with a sign.
    "diverging": "RdBu_r",
}

# Marker shapes, so identity is never carried by colour alone (Week 2,
# redundant coding — Wilke ch. 20).
MARKERS = ["o", "s", "^", "D"]


def style_defaults(dpi: int = 150) -> None:
    """Set the look once, at the top of a script. Slide 26, in one call."""
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "figure.dpi": dpi,
        "savefig.dpi": 300,
        "figure.facecolor": PALETTE["surface"],
        "axes.facecolor": PALETTE["surface"],
        "font.size": 10,
        "font.family": "DejaVu Sans",
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 10,
        "axes.labelsize": 10,
        "axes.labelcolor": PALETTE["ink_soft"],
        "axes.edgecolor": PALETTE["grid"],
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": PALETTE["grid"],
        "grid.linewidth": 0.8,
        "xtick.color": PALETTE["ink_soft"],
        "ytick.color": PALETTE["ink_soft"],
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.frameon": False,
        "legend.fontsize": 9,
        "lines.linewidth": 2.0,
        "lines.markersize": 5,
        "text.color": PALETTE["ink"],
    })


def save_fig(fig, path, note: str | None = None) -> str:
    """
    Export the way slide 27 says to: 300 dpi, tight bbox, white facecolor.

    Pass `note` and it is stamped in the bottom-left as a source line. Every
    figure you submit needs one — it is where n, the data source and any
    exclusion rule go.
    """
    if note:
        # Sit the source line BELOW the figure box. bbox_inches="tight" grows
        # the canvas to include it, so it can never land on the x-label.
        fig.text(0.01, -0.035, note, fontsize=7, color=PALETTE["ink_soft"],
                 ha="left", va="top")
    fig.savefig(path, dpi=300, bbox_inches="tight",
                facecolor=PALETTE["surface"])
    return str(path)


# ----------------------------------------------------------------- lie factor
def lie_factor(value_start, value_end, ink_start, ink_end, ink_dimension=1):
    """
    Tufte's Lie Factor = (effect shown in the graphic) / (effect in the data).

        effect = (final - initial) / initial

    `ink_dimension` is 1 when the quantity is encoded by a length (a bar), and
    2 when it is encoded by an area (a scaled icon, a bubble sized by radius).
    This is the argument people forget, and forgetting it is what makes a
    1.5x icon read as a 2.25x increase.

    Honest is 1.0. Tufte accepts 0.95-1.05. Above that the graphic exaggerates;
    below it, the graphic understates — which is also a distortion, just a less
    popular one.

    Returns (lie_factor, data_effect, graphic_effect).
    """
    if value_start == 0 or ink_start == 0:
        raise ValueError("Lie Factor is undefined when the initial value is 0 "
                         "— and so is the chart. Use a different baseline.")
    data_effect = (value_end - value_start) / value_start
    ink_ratio = (ink_end / ink_start) ** ink_dimension
    graphic_effect = ink_ratio - 1.0
    if data_effect == 0:
        raise ValueError("The data did not change, so any visible change is "
                         "pure distortion and the Lie Factor is infinite.")
    return graphic_effect / data_effect, data_effect, graphic_effect


def lie_verdict(lf: float) -> str:
    """The one-word reading of a Lie Factor, so your audit table is consistent."""
    if 0.95 <= lf <= 1.05:
        return "honest"
    if lf > 1.05:
        return f"exaggerates {lf:.2f}x"
    return f"understates ({lf:.2f})"


# ------------------------------------------------------- colour-vision deficiency
# Machado, Oliveira & Fernandes (2009) severity-1.0 matrices, applied in
# LINEAR RGB. Applying them to gamma-encoded sRGB is the usual mistake and it
# makes every palette look better than it is.
_CVD = {
    "protan": np.array([[0.152286, 1.052583, -0.204868],
                        [0.114503, 0.786281, 0.099216],
                        [-0.003882, -0.048116, 1.051998]]),
    "deutan": np.array([[0.367322, 0.860646, -0.227968],
                        [0.280085, 0.672501, 0.047413],
                        [-0.011820, 0.042940, 0.968881]]),
    "tritan": np.array([[1.255528, -0.076749, -0.178779],
                        [-0.078411, 0.930809, 0.147602],
                        [0.004733, 0.691367, 0.303900]]),
}


def _srgb_to_linear(c):
    c = np.asarray(c, dtype=float)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _linear_to_srgb(c):
    c = np.clip(np.asarray(c, dtype=float), 0.0, 1.0)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def simulate_cvd(rgb, kind="deutan"):
    """
    Simulate colour-vision deficiency on an RGB array or a list of hex colours.

    `rgb` may be:
      - an (H, W, 3) or (H, W, 4) float array in 0..1  (a rendered figure)
      - a list of '#rrggbb' strings                     (a palette)

    `kind` is 'protan', 'deutan' (the common one, ~6% of men) or 'tritan'.

    Returns the same shape/type, transformed. Use it on your own exported PNG:
    if two series become the same colour, the chart fails and no amount of
    "but the palette is from a paper" fixes it.
    """
    if kind not in _CVD:
        raise ValueError(f"kind must be one of {sorted(_CVD)}")
    m = _CVD[kind]

    if isinstance(rgb, (list, tuple)) and rgb and isinstance(rgb[0], str):
        out = []
        for h in rgb:
            h = h.lstrip("#")
            v = np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])
            lin = _srgb_to_linear(v)
            sim = _linear_to_srgb(m @ lin)
            out.append("#{:02X}{:02X}{:02X}".format(
                *(int(round(x * 255)) for x in sim)))
        return out

    arr = np.asarray(rgb, dtype=float)
    if arr.max() > 1.0:
        arr = arr / 255.0
    alpha = None
    if arr.shape[-1] == 4:
        alpha, arr = arr[..., 3:], arr[..., :3]
    lin = _srgb_to_linear(arr)
    sim = _linear_to_srgb(lin @ m.T)
    return sim if alpha is None else np.concatenate([sim, alpha], axis=-1)


def cvd_report(hexes, kind="deutan"):
    """Print each colour beside its simulated twin. Three lines, no excuses."""
    sim = simulate_cvd(list(hexes), kind)
    print(f"{kind} simulation")
    for a, b in zip(hexes, sim):
        print(f"  {a}  ->  {b}")
    return sim


# ------------------------------------------------------------------- OKLab
# Distance in sRGB is not a perceptual metric: two colours 30 units apart can
# look identical or obviously different depending on where they sit. OKLab
# (Ottosson, 2020) is near-uniform, so Euclidean distance in it means roughly
# the same thing everywhere. That is what makes a numeric threshold possible.
_M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929],
                [0.2119034982, 0.6806995451, 0.1073969566],
                [0.0883024619, 0.2817188376, 0.6299787005]])
_M2 = np.array([[0.2104542553,  0.7936177850, -0.0040720468],
                [1.9779984951, -2.4285922050,  0.4505937099],
                [0.0259040371,  0.7827717662, -0.8086757660]])


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])


def to_oklab(colour):
    """'#rrggbb' or an RGB triple in 0..1 -> (L, a, b) in OKLab."""
    rgb = _hex_to_rgb(colour) if isinstance(colour, str) else np.asarray(colour, float)
    lms = _M1 @ _srgb_to_linear(rgb)
    return _M2 @ np.cbrt(lms)


def delta_e(c1, c2):
    """
    Perceptual distance between two colours, OKLab x 100.

    The thresholds this course uses, from the palette validator:

        >= 15   fine for readers with normal colour vision
        >= 8    the target for any pair after CVD simulation
        6 - 8   legal ONLY with a second encoding channel: a different marker
                shape, a direct label, a texture, or a gap between the marks
        < 6     the two series are the same colour. Fix the palette.
    """
    return float(np.linalg.norm(to_oklab(c1) - to_oklab(c2)) * 100)


def worst_pair(palette, kind=None):
    """
    The closest pair in a palette, optionally after simulating a CVD.

    Returns (i, j, hex_i, hex_j, delta_e) with 1-based slot numbers, comparing
    EVERY pair — which is the right test for a scatter, a bubble chart or a
    choropleth, where any two series can end up adjacent on screen.
    """
    shown = list(palette) if kind in (None, "normal") else simulate_cvd(list(palette), kind)
    best = None
    for i in range(len(shown)):
        for j in range(i + 1, len(shown)):
            d = delta_e(shown[i], shown[j])
            if best is None or d < best[-1]:
                best = (i + 1, j + 1, palette[i], palette[j], d)
    return best


def verdict(d):
    """The one-word reading of a delta E, so your audit table is consistent."""
    if d >= 15:
        return "clear"
    if d >= 8:
        return "ok"
    if d >= 6:
        return "needs a second channel"
    return "FAILS — same colour"


# ------------------------------------------------- forcing exact statistics
def match_stats(x, y, mean_x, mean_y, sd_x, sd_y, r, jitter=1e-9, seed=0):
    """
    Linearly transform (x, y) so that it has EXACTLY the given mean, standard
    deviation and Pearson correlation — while keeping its shape.

    This is the machinery behind Anscombe's quartet and the Datasaurus Dozen:
    summary statistics do not constrain shape, and this function is the proof.
    Standard deviations are population (ddof=0).

    How it works: standardise x, residualise y against x so the two parts are
    orthogonal, then rebuild y as r*zx + sqrt(1-r^2)*residual. The correlation
    of the result is r by construction, because the residual is uncorrelated
    with zx.
    """
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=float).copy()
    y = np.asarray(y, dtype=float).copy()
    # a shape that is perfectly collinear has no residual to work with
    y = y + rng.normal(0, jitter, size=y.shape)

    zx = (x - x.mean()) / x.std()
    zy = (y - y.mean()) / y.std()
    rho = float(np.corrcoef(zx, zy)[0, 1])
    resid = zy - rho * zx
    resid = (resid - resid.mean()) / resid.std()
    zy_new = r * zx + np.sqrt(max(0.0, 1 - r * r)) * resid
    return mean_x + sd_x * zx, mean_y + sd_y * zy_new


def describe(x, y):
    """The five numbers people report instead of plotting. Returns a dict."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    return {
        "n": len(x),
        "mean_x": float(x.mean()),
        "mean_y": float(y.mean()),
        "sd_x": float(x.std(ddof=0)),
        "sd_y": float(y.std(ddof=0)),
        "r": float(np.corrcoef(x, y)[0, 1]),
    }


if __name__ == "__main__":
    # Self-check: run this once to confirm the toolkit works before you start.
    # The three worked examples below are NOT from the Part B audit — they are
    # made up, so running this file does not do your homework for you.
    print("lie_factor() — three made-up examples, not the Part B charts\n")
    for label, args, kw in [
        ("a bar chart drawn honestly from zero,  10 -> 15, ink 4 -> 6 cm",
         (10, 15, 4.0, 6.0), {}),
        ("the same rise, bars cut at 9,          10 -> 15, ink 1 -> 6 cm",
         (10, 15, 1.0, 6.0), {}),
        ("a smaller rise as a 2-D icon,         10 -> 13, icon 1.0 -> 1.3x",
         (10, 13, 1.0, 1.3), {"ink_dimension": 2}),
    ]:
        lf, de, ge = lie_factor(*args, **kw)
        print(f"  {label}\n      data effect {de:+.3f}   graphic effect "
              f"{ge:+.3f}   LF {lf:6.2f}   {lie_verdict(lf)}")
    print("\nThe first two encode the SAME 50% rise: one honestly, one from a "
          "cut baseline.\nThe third scales an icon in both dimensions, so the "
          "ink grows as the SQUARE\nof the scale \u2014 which is what "
          "ink_dimension=2 is for.\n")
    cvd_report(PALETTE["series"] + [PALETTE["series_4th"]], "deutan")
    print()
    for label, pal in [("course palette, 3 slots", PALETTE["series"]),
                       ("course palette + 4th slot",
                        PALETTE["series"] + [PALETTE["series_4th"]])]:
        i, j, a, b, d = worst_pair(pal, "deutan")
        print(f"{label:28s} worst deutan pair S{i}/S{j}  "
              f"ΔE {d:5.1f}  {verdict(d)}")
