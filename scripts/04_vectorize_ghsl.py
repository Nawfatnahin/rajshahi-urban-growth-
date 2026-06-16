#!/usr/bin/env python3
import os
import json
import rasterio
from rasterio.features import shapes
from shapely.geometry import shape, mapping
from shapely.ops import unary_union

EPOCHS = [1990, 1995, 2000, 2005, 2010, 2015, 2020]
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")

def vectorize_epoch(year):
    tif_path = os.path.join(DATA_DIR, f"ghsl_{year}_raj.tif")
    out_path = os.path.join(DATA_DIR, f"ghsl_{year}_raj.geojson")
    
    if not os.path.exists(tif_path):
        print(f"[SKIP] {tif_path} not found.")
        return
        
    print(f"Vectorizing {year}...")
    with rasterio.open(tif_path) as src:
        image = src.read(1)
        # Create a mask for built-up areas. Ignore nodata (0).
        # We can also filter out very low density to make the city concept clearer.
        # But let's just use > 0 to capture all urban footprint.
        mask = image > 0
        
        results = (
            {'properties': {'value': v}, 'geometry': s}
            for i, (s, v) in enumerate(
                shapes(image, mask=mask, transform=src.transform)
            )
        )
        
        polygons = []
        for geom_dict in results:
            polygons.append(shape(geom_dict['geometry']))
            
        if not polygons:
            print(f"[WARN] No urban polygons found for {year}")
            return

        # Union to create a single multipolygon, then buffer to smooth
        # 0.0005 deg is approx 50 meters at equator
        unified = unary_union(polygons)
        smoothed = unified.buffer(0.0005).simplify(0.0002)
        
        feature = {
            "type": "Feature",
            "properties": {"year": year},
            "geometry": mapping(smoothed)
        }
        
        geojson = {
            "type": "FeatureCollection",
            "features": [feature]
        }
        
        with open(out_path, "w") as f:
            json.dump(geojson, f)
            
    print(f"[OK] Saved {out_path}")

if __name__ == "__main__":
    for yr in EPOCHS:
        vectorize_epoch(yr)
