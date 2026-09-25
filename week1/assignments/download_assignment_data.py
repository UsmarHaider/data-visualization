"""
Download the five assignment datasets.

Run this once from inside the assignments/ folder:

    python3 download_assignment_data.py

Each dataset is paired with one task in TASKS.md. They were chosen so that
between them they need every chart type covered in the Week 1 lecture, and
so that none of them is the Titanic dataset used in the lecture itself.
"""

import sys
import urllib.request
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

SOURCES = {
    # Task 1 - 13 datasets with near-identical summary statistics.
    "datasaurus.csv": (
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/"
        "master/data/2020/2020-10-13/datasaurus.csv"
    ),
    # Task 2 - 142 countries x 12 years, a balanced panel with no missing values.
    "gapminder.csv": (
        "https://raw.githubusercontent.com/resbaz/r-novice-gapminder-files/"
        "master/data/gapminder-FiveYearData.csv"
    ),
    # Task 3 - 344 penguins, three species, some missing measurements.
    "penguins.csv": (
        "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
    ),
    # Task 4 - 398 cars, 1970-1982, fuel economy and engine specs.
    "mpg.csv": (
        "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv"
    ),
    # Task 5 - monthly airline passengers, 1949-1960. A clean time series.
    "flights.csv": (
        "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/flights.csv"
    ),
}


def download(name: str, url: str) -> None:
    target = DATA_DIR / name
    if target.exists():
        print(f"  {name:<16} already present ({target.stat().st_size:,} bytes) - skipping")
        return

    with urllib.request.urlopen(url, timeout=30) as response:
        payload = response.read()
    target.write_bytes(payload)
    print(f"  {name:<16} downloaded ({len(payload):,} bytes)")


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading into {DATA_DIR}")
    failed = False
    for name, url in SOURCES.items():
        try:
            download(name, url)
        except Exception as exc:  # noqa: BLE001 - surface any network problem plainly
            print(f"  {name:<16} FAILED: {exc}", file=sys.stderr)
            failed = True
    if failed:
        return 1
    print("Done. Open TASKS.md and pick your task.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
