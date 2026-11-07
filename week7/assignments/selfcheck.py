"""
Week 7 self-check — run this first, once, and read nothing into the output.

It proves the four toolkits import, the five data files are readable, and
matplotlib can draw a dashboard grid and link two panels on this machine. It
deliberately reports **nothing about the contents** of the files: the audit
is Task A.

    python3 selfcheck.py

`tslib.py` and `geolib.py` have self-checks of their own, but they look for
the Week 4 and Week 5 data folders, so run those from those weeks.
`python3 dashlib.py` self-tests here, on made-up numbers.
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

import dashlib
import geolib
import tslib
import vizlib

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
FILES = ["district_transit.csv", "routes.csv", "ridership_daily.csv",
         "fare_revenue.csv", "regions.geojson"]

print(__doc__.strip().splitlines()[0])
print("-" * 70)
print(f"python {sys.version.split()[0]}  pandas {pd.__version__}  "
      f"numpy {np.__version__}  matplotlib {matplotlib.__version__}")
print(f"plotly installed: {dashlib.has_plotly()}  "
      f"(optional — Task C can be done without it)")

# ---- the toolkits ------------------------------------------------------
print(f"vizlib   palette      series {vizlib.PALETTE['series']}, "
      f"sequential '{vizlib.PALETTE['sequential']}'")
print(f"tslib    Week 4's     {['audit_index', 'window_report', 'treemap']}")
print(f"geolib   Week 5's     {['breaks', 'choropleth', 'pcp']}")
print(f"dashlib  new this week {dashlib.__all__[:6]}")

# ---- the files are readable -------------------------------------------
for name in FILES:
    path = os.path.join(D, name)
    if not os.path.exists(path):
        raise SystemExit(f"missing: data/{name}")
    if name.endswith(".csv"):
        cols = list(pd.read_csv(path, nrows=5).columns)
        n = sum(1 for _ in open(path)) - 1
        print(f"{name:<22} readable, {n:>5,} rows, {len(cols)} columns: "
              f"{', '.join(cols)}")
    else:
        n = len(json.load(open(path))["features"])
        print(f"{name:<22} readable, {n} features")

# ---- the furniture draws, and two panels link -------------------------
feats = geolib.read_geojson(os.path.join(D, "regions.geojson"))
assert len(feats) == 24, len(feats)
area = {f["code"]: geolib.polygon_area_km2(f["ring"]) for f in feats}

rng = np.random.default_rng(0)
demo = pd.DataFrame({"a": rng.normal(0, 1, 120), "b": rng.normal(0, 1, 120)})

vizlib.style_defaults()
fig = plt.figure(figsize=(10.5, 5.0))
axd = dashlib.dashboard_grid(
    fig, [["kpi", "map", "scatter"]],
    headline="Self-check only — land area and random numbers",
    standfirst="Nothing on this screen is a finding. It is here to prove the "
               "toolkits draw on your machine.")
dashlib.kpi_tile(axd["kpi"], "districts", len(feats), delta=0.0,
                 good="neutral", note="features in regions.geojson",
                 delta_fmt="{:+.0f}")
edges = geolib.choropleth(axd["map"], feats, area, scheme="natural", k=5,
                          legend_title="land area (km²)")
axd["map"].set_title("Land area, not a finding", fontsize=10)
axd["scatter"].scatter(demo.a, demo.b, s=18, color=vizlib.PALETTE["muted"],
                       edgecolor=vizlib.PALETTE["surface"], lw=0.5)
axd["scatter"].set_title("Random numbers, brushed", fontsize=10)

state = {"artist": None, "n": 0}


def repaint(mask):
    if state["artist"] is not None:
        state["artist"].remove()
    state["n"] = int(mask.sum())
    state["artist"] = axd["scatter"].scatter(
        demo.a[mask], demo.b[mask], s=22, color=vizlib.PALETTE["highlight"],
        edgecolor=vizlib.PALETTE["surface"], lw=0.5, zorder=5)


brush = dashlib.LinkedBrush(axd["scatter"], demo, "a", "b", on_select=repaint)
brush.simulate((0.0, 0.0, 3.5, 3.5))
out = vizlib.save_fig(fig, os.path.join(HERE, "_selfcheck.png"),
                      note="Self-check only. Synthetic data, CDB601220 Week 7.")
plt.close(fig)

print(f"geolib.choropleth      5 Jenks classes, "
      f"{edges[0]:,.0f}–{edges[-1]:,.0f} km², equal-area projection")
print(f"dashlib.dashboard_grid 3 named panels + headline band")
print(f"dashlib.LinkedBrush    a drag selected {state['n']} of {len(demo)} points")
print(f"vizlib.save_fig        wrote {os.path.basename(out)} at 300 dpi")
print("-" * 70)
print("If that ran, everything in TASKS.md will run. Now open TASKS.md.")
