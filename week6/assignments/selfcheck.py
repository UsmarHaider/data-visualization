"""
Week 6 self-check — run this first, once, and read nothing into the output.

It proves the three toolkits import, the four data files are readable, and
matplotlib can draw a projected map on this machine. It deliberately reports
**nothing about the contents** of the files: the audit is Task A.

    python3 selfcheck.py

`geolib.py` and `tslib.py` have self-checks of their own, but they look for
the Week 4 and Week 5 data folders, so run them from those weeks, not here.
"""
from __future__ import annotations

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import geolib
import tslib
import vizlib

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
FILES = ["district_grid.csv", "grid_daily.csv", "generation_mix.csv",
         "regions.geojson"]

print(__doc__.strip().splitlines()[0])
print("-" * 68)
print(f"python {sys.version.split()[0]}  pandas {pd.__version__}  "
      f"numpy {np.__version__}  matplotlib {matplotlib.__version__}")

# ---- the toolkits ------------------------------------------------------
print(f"vizlib  palette      series {vizlib.PALETTE['series']}, "
      f"sequential '{vizlib.PALETTE['sequential']}'")
print(f"tslib   on top of it {['audit_index', 'window_report', 'treemap']} "
      f"and {len([n for n in dir(tslib) if not n.startswith('_')])} names")
print(f"geolib  on top of it {['breaks', 'choropleth', 'pcp']} "
      f"and {len([n for n in dir(geolib) if not n.startswith('_')])} names")

# ---- the files are readable -------------------------------------------
for name in FILES:
    path = os.path.join(D, name)
    if not os.path.exists(path):
        raise SystemExit(f"missing: data/{name}")
    if name.endswith(".csv"):
        cols = list(pd.read_csv(path, nrows=5).columns)
        print(f"{name:<20} readable, {len(cols)} columns: {', '.join(cols)}")
    else:
        n = len(json.load(open(path))["features"])
        print(f"{name:<20} readable, {n} features")

# ---- matplotlib can project and draw ----------------------------------
feats = geolib.read_geojson(os.path.join(D, "regions.geojson"))
area = {f["code"]: geolib.polygon_area_km2(f["ring"]) for f in feats}
assert len(feats) == 24, len(feats)

vizlib.style_defaults()
fig, ax = plt.subplots(figsize=(5.2, 5.6))
edges = geolib.choropleth(ax, feats, area, scheme="natural", k=5,
                          legend_title="land area (km²)")
ax.set_title("Land area, not a finding — this map is only here to prove\n"
             "the toolkit draws on your machine", loc="left", fontsize=10)
out = vizlib.save_fig(fig, os.path.join(HERE, "_selfcheck.png"),
                      note="Self-check only. Synthetic data, CDB601220 Week 6.")
plt.close(fig)
print(f"geolib.choropleth    5 Jenks classes, "
      f"{edges[0]:,.0f}–{edges[-1]:,.0f} km², equal-area projection")
print(f"vizlib.save_fig      wrote {os.path.basename(out)} at 300 dpi")
print("-" * 68)
print("If that ran, everything in TASKS.md will run. Now open TASKS.md.")
