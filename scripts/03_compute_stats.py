#!/usr/bin/env python3
"""
Compute total urban built-up area (km²) per epoch from GHSL COG files.
Outputs a JSON snippet to embed directly in index.html.
"""

import os, json
import numpy as np
import rasterio

EPOCHS   = [1990, 1995, 2000, 2005, 2010, 2015, 2020]
DATA_DIR = "../data"
THRESHOLD = 500

stats = {}
for year in EPOCHS:
    path = os.path.join(DATA_DIR, f'ghsl_{year}_raj.cog.tif')
    if not os.path.exists(path):
        print(f"[WARN] Missing: {path}")
        stats[year] = None
        continue

    with rasterio.open(path) as src:
        data = src.read(1, masked=True)
        urban_cells = np.sum(data > THRESHOLD)
        area_km2 = round(urban_cells * 0.01, 2)
        total_built_m2 = float(np.sum(data[data > 0]))
        total_built_km2 = round(total_built_m2 / 1e6, 2)
        stats[year] = {
            "urban_cells":      int(urban_cells),
            "area_km2":         area_km2,
            "built_surface_km2": total_built_km2
        }
    print(f"  {year}: {area_km2} km² urban extent, {total_built_km2} km² weighted")

print("\n── Paste into index.html STATS object ──")
js_stats = {}
for yr, s in stats.items():
    if s:
        js_stats[str(yr)] = s['area_km2']
print(f"const URBAN_AREA_KM2 = {json.dumps(js_stats, indent=2)};")
