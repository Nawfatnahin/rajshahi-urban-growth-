#!/usr/bin/env python3
"""
Clip a GHSL global tile to the Rajshahi bbox.
Method B: Direct Download (No GEE Account)
"""
import rasterio
from rasterio.mask import mask
from shapely.geometry import box
import json, sys, os

BBOX = [88.45, 24.28, 88.75, 24.52]  # [lon_min, lat_min, lon_max, lat_max]

def clip_to_rajshahi(input_tif, output_tif):
    geom = [box(*BBOX).__geo_interface__]
    with rasterio.open(input_tif) as src:
        out_img, out_transform = mask(src, geom, crop=True, nodata=0)
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": out_img.shape[1],
            "width": out_img.shape[2],
            "transform": out_transform,
            "nodata": 0
        })
        with rasterio.open(output_tif, "w", **out_meta) as dest:
            dest.write(out_img)
    print(f"Clipped: {output_tif}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        clip_to_rajshahi(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python3 01_clip_direct.py <global_tile.tif> <output_raj.tif>")
