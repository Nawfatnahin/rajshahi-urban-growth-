#!/usr/bin/env python3
"""
Process downloaded GeoTIFFs:
  1. Validate CRS (ensure EPSG:4326)
  2. Set nodata=0
  3. Convert to Cloud Optimized GeoTIFF (COG) with deflate compression
  4. Verify output integrity

Requirements: pip install rasterio rio-cogeo numpy
"""

import os
import sys
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.enums import Resampling as ResamplingEnum
from rio_cogeo.cogeo import cog_translate
from rio_cogeo.profiles import cog_profiles

EPOCHS  = [1990, 1995, 2000, 2005, 2010, 2015, 2020]
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")

def ensure_4326(src_path: str) -> str:
    """If CRS is not EPSG:4326, reproject and return new temp path."""
    with rasterio.open(src_path) as src:
        if src.crs and src.crs.to_epsg() == 4326:
            return src_path

        print(f"  Reprojecting {src.crs} → EPSG:4326 ...")
        transform, width, height = calculate_default_transform(
            src.crs, 'EPSG:4326', src.width, src.height, *src.bounds
        )
        meta = src.meta.copy()
        meta.update(crs='EPSG:4326', transform=transform,
                    width=width, height=height, dtype='float32')

        tmp = src_path + '.reproj.tif'
        with rasterio.open(tmp, 'w', **meta) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs='EPSG:4326',
                    resampling=ResamplingEnum.nearest
                )
        return tmp

def print_summary(path: str):
    with rasterio.open(path) as src:
        data = src.read(1, masked=True)
        nonzero = data.compressed()[data.compressed() > 0]
        total_built_km2 = nonzero.sum() / 1e6
        pct_built = 100 * (nonzero.size / data.compressed().size) if data.compressed().size else 0
        print(f"    CRS:        {src.crs}")
        print(f"    Shape:      {src.shape[0]}×{src.shape[1]} px")
        print(f"    Bounds:     {[round(b,4) for b in src.bounds]}")
        print(f"    Built area: {total_built_km2:.2f} km²  ({pct_built:.1f}% of cells)")

def process(year: int):
    raw  = os.path.join(DATA_DIR, f'ghsl_{year}_raj.tif')
    cog  = os.path.join(DATA_DIR, f'ghsl_{year}_raj.cog.tif')
    tmp  = None

    if os.path.exists(cog):
        print(f"[SKIP] {year}: COG already exists.")
        return

    if not os.path.exists(raw):
        print(f"[MISS] {raw} not found. Please place clipped tile here.")
        return

    print(f"\n── Processing {year} ──")
    working = ensure_4326(raw)
    if working != raw:
        tmp = working

    config = {
        "GDAL_TIFF_INTERNAL_MASK": True,
        "GDAL_TIFF_OVR_BLOCKSIZE": 256,
    }
    cog_translate(
        working,
        cog,
        cog_profiles.get("deflate"),
        overview_resampling="average",
        nodata=0,
        add_mask=True,
        config=config,
        quiet=False
    )

    print(f"[OK]  COG created successfully.")

    print_summary(cog)

    if tmp and os.path.exists(tmp):
        os.remove(tmp)

if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    for yr in EPOCHS:
        process(yr)

    print("\n── Output files ──")
    for yr in EPOCHS:
        p = os.path.join(DATA_DIR, f'ghsl_{yr}_raj.cog.tif')
        exists = os.path.exists(p)
        size = f"{os.path.getsize(p) // 1024} KB" if exists else "MISSING"
        status = "✓" if exists else "✗"
        print(f"  {status} ghsl_{yr}_raj.cog.tif  {size}")
