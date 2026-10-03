"""
Prepare the Week 2 assignment data.

Run this once from inside the assignments/ folder:

    python3 download_assignment_data.py

Two things happen:

1. Five free, public datasets are downloaded into data/. They are the same five
   used by the Week 3 brief, so the two weeks share one download.

2. Three perception stimulus files are generated into data/. These are not
   downloaded - they are built here with a fixed random seed so that every
   student gets identical stimuli and your answers can be compared with a
   classmate's. Do not regenerate them with a different seed.

The generated files exist because preattentive search and Gestalt grouping
cannot be demonstrated on a normal tabular dataset: they need controlled
stimuli where exactly one feature varies at a time.
"""

import sys
import urllib.request
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
SEED = 42

SOURCES = {
    # Tasks 3 and 5 - 53,940 diamonds: ordinal grades and continuous measures.
    "diamonds.csv": (
        "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv"
    ),
    # Tasks 2 and 5 - 142 countries x 12 years, a balanced panel.
    "gapminder.csv": (
        "https://raw.githubusercontent.com/resbaz/r-novice-gapminder-files/"
        "master/data/gapminder-FiveYearData.csv"
    ),
    # Tasks 3 and 4 - 244 restaurant bills, several categorical columns.
    "tips.csv": (
        "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
    ),
    # Tasks 4 and 5 - 150 flowers, four numeric columns and one grouping.
    "iris.csv": (
        "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
    ),
    # Task 3 - 51 US states, seven numeric columns. Dense table to de-clutter.
    "car_crashes.csv": (
        "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/car_crashes.csv"
    ),
}


def download(name: str, url: str) -> None:
    target = DATA_DIR / name
    if target.exists():
        print(f"  {name:<26} already present ({target.stat().st_size:,} bytes) - skipping")
        return
    with urllib.request.urlopen(url, timeout=30) as response:
        payload = response.read()
    target.write_bytes(payload)
    print(f"  {name:<26} downloaded ({len(payload):,} bytes)")


# --------------------------------------------------------------------------
# Generated stimuli
# --------------------------------------------------------------------------

def make_search_trials(rng):
    """Visual-search trials for Task 1.

    Three conditions:
      colour      - target differs from distractors by hue only      (preattentive)
      shape       - target differs by shape only                     (preattentive)
      conjunction - target is the only item that is BOTH red AND a circle;
                    every distractor shares one of those two features (serial)

    Set size varies so you can plot response time against set size. A
    preattentive feature gives a flat line; a conjunction gives a rising one.
    """
    rows = []
    trial = 0
    for condition in ("colour", "shape", "conjunction"):
        for set_size in (9, 16, 25, 36, 49):
            for target_present in (True, False):
                for _ in range(3):              # 3 repeats per cell
                    trial += 1
                    side = int(set_size ** 0.5)
                    coords = [(c, r) for r in range(side) for c in range(side)]
                    rng.shuffle(coords)
                    coords = coords[:set_size]
                    t_index = rng.randrange(set_size) if target_present else -1

                    for i, (cx, cy) in enumerate(coords):
                        is_target = i == t_index
                        # jitter inside the cell so the grid is not perfectly regular
                        x = cx + rng.uniform(0.25, 0.75)
                        y = cy + rng.uniform(0.25, 0.75)

                        if condition == "colour":
                            colour = "red" if is_target else "blue"
                            shape = "circle"
                        elif condition == "shape":
                            colour = "blue"
                            shape = "square" if is_target else "circle"
                        else:  # conjunction
                            if is_target:
                                colour, shape = "red", "circle"
                            else:
                                # half red squares, half blue circles:
                                # each distractor shares exactly one target feature
                                colour, shape = (
                                    ("red", "square") if i % 2 == 0 else ("blue", "circle")
                                )

                        rows.append(
                            f"{trial},{condition},{set_size},"
                            f"{'yes' if target_present else 'no'},{i},"
                            f"{x:.4f},{y:.4f},{colour},{shape},"
                            f"{'yes' if is_target else 'no'}"
                        )
    header = ("trial,condition,set_size,target_present,item_index,"
              "x,y,colour,shape,is_target")
    return header, rows


def make_gestalt_panels(rng):
    """Six panels for Task 2, one per Gestalt principle.

    Each panel holds the SAME 48 items. Only the layout or styling changes, so
    the grouping a reader perceives comes from the arrangement, never the data.
    """
    rows = []
    n_per_group = 12

    def add(panel, group, x, y, colour, shape, size, connector):
        rows.append(
            f"{panel},{group},{x:.4f},{y:.4f},{colour},{shape},{size},{connector}"
        )

    # 1. proximity - four spatially separated clumps, all identical styling
    for g, (ox, oy) in enumerate([(0, 0), (6, 0), (0, 6), (6, 6)]):
        for _ in range(n_per_group):
            add("proximity", f"g{g}", ox + rng.uniform(0, 2), oy + rng.uniform(0, 2),
                "grey", "circle", 60, "none")

    # 2. similarity - one uniform cloud, grouped by colour alone
    for g, colour in enumerate(["#4477aa", "#ee6677", "#228833", "#ccbb44"]):
        for _ in range(n_per_group):
            add("similarity", f"g{g}", rng.uniform(0, 8), rng.uniform(0, 8),
                colour, "circle", 60, "none")

    # 3. enclosure - same cloud, groups defined by a drawn boundary (see box_* cols)
    for g, (ox, oy) in enumerate([(0, 0), (5, 0), (0, 5), (5, 5)]):
        for _ in range(n_per_group):
            add("enclosure", f"g{g}", ox + rng.uniform(0.3, 2.7),
                oy + rng.uniform(0.3, 2.7), "grey", "circle", 60, "none")

    # 4. continuity - two gently bowed paths that CROSS in the middle, so the
    #    eye must follow each one through the intersection (good continuation)
    import math as _math
    for g in range(2):
        for i in range(2 * n_per_group):
            t = i / (2 * n_per_group - 1) * 8
            bow = 0.9 * _math.sin(t / 8 * _math.pi)
            y = (1 + 6 * (t / 8) + bow) if g == 0 else (7 - 6 * (t / 8) - bow)
            add("continuity", f"g{g}", t, y, "grey", "circle", 45, "none")

    # 5. closure - items trace an incomplete rectangle; the eye completes it
    import math
    for g in range(2):
        for i in range(2 * n_per_group):
            ang = i / (2 * n_per_group) * 2 * math.pi
            if 1.9 < ang < 2.6:        # deliberate gap
                continue
            add("closure", f"g{g}", 4 + (3 - g) * math.cos(ang),
                4 + (3 - g) * math.sin(ang), "grey", "circle", 45, "none")

    # 6. connection - pairs joined by a line; connection beats both colour and proximity
    for i in range(2 * n_per_group):
        x1, y1 = rng.uniform(0, 8), rng.uniform(0, 8)
        add("connection", f"pair{i}", x1, y1, "#4477aa", "circle", 60, f"pair{i}")
        add("connection", f"pair{i}", x1 + rng.uniform(-1.5, 1.5),
            y1 + rng.uniform(-1.5, 1.5), "#ee6677", "circle", 60, f"pair{i}")

    header = "panel,group,x,y,colour,shape,size,connector"
    return header, rows


def make_channel_trials(rng):
    """Ratio-estimation trials for Task 4 (Cleveland & McGill style).

    Each trial gives you a true ratio between two values. You encode the pair
    with one channel, show it to a reader, record their estimate, then compute
    the error. Position should beat length, length should beat angle, and area
    and colour should be worst.
    """
    rows = []
    channels = ("position", "length", "angle", "area", "colour")
    ratios = (0.15, 0.25, 0.40, 0.55, 0.70, 0.85)
    trial = 0
    for channel in channels:
        for ratio in ratios:
            trial += 1
            base = rng.randrange(40, 90)
            smaller = round(base * ratio, 2)
            rows.append(
                f"{trial},{channel},{ratio:.2f},{base},{smaller:.2f},,"
            )
    header = ("trial,channel,true_ratio,value_large,value_small,"
              "reader_estimate,absolute_error")
    return header, rows


def write_csv(name: str, header: str, rows: list) -> None:
    target = DATA_DIR / name
    target.write_text(header + "\n" + "\n".join(rows) + "\n")
    print(f"  {name:<26} generated ({len(rows):,} rows, seed={SEED})")


def main() -> int:
    import random

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Target folder: {DATA_DIR}\n")

    print("Downloading public datasets")
    failed = False
    for name, url in SOURCES.items():
        try:
            download(name, url)
        except Exception as exc:  # noqa: BLE001 - surface any network problem plainly
            print(f"  {name:<26} FAILED: {exc}", file=sys.stderr)
            failed = True

    print("\nGenerating perception stimuli")
    rng = random.Random(SEED)
    write_csv("stimuli_search.csv", *make_search_trials(rng))
    write_csv("stimuli_gestalt.csv", *make_gestalt_panels(rng))
    write_csv("channel_trials.csv", *make_channel_trials(rng))

    if failed:
        print("\nSome downloads failed - see the errors above.", file=sys.stderr)
        return 1
    print("\nDone. Open TASKS.md and start with Task 1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
