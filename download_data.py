"""
Week 1 - download the datasets used in the lecture notebook.

Run this once before opening the notebook:

    python3 download_data.py

Two datasets, two jobs:
  anscombe.csv  - Anscombe's quartet, used to answer "why visualise at all?"
  titanic.csv   - the raw Kaggle-style Titanic passenger list, used for
                  everything else (cleaning, aggregating, chart choice).
"""

import sys
import urllib.request
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

SOURCES = {
    "anscombe.csv": "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/anscombe.csv",
    "titanic.csv": "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv",
}


def download(name: str, url: str) -> None:
    target = DATA_DIR / name
    if target.exists():
        print(f"  {name:<14} already present ({target.stat().st_size:,} bytes) - skipping")
        return

    print(f"  {name:<14} downloading from {url}")
    with urllib.request.urlopen(url, timeout=30) as response:
        payload = response.read()
    target.write_bytes(payload)
    print(f"  {name:<14} saved ({len(payload):,} bytes)")


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading into {DATA_DIR}")
    for name, url in SOURCES.items():
        try:
            download(name, url)
        except Exception as exc:  # noqa: BLE001 - surface any network problem plainly
            print(f"  {name:<14} FAILED: {exc}", file=sys.stderr)
            return 1
    print("Done. You can now run week1_visualization.ipynb")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
