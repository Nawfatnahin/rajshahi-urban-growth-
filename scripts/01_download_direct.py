#!/usr/bin/env python3
"""
Automated downloader for GHS-BUILT-S R2023A (100m, EPSG:4326).
Since the full global ZIP files are massive (~1-2 GB each), this script:
1. Attempts to use Rasterio's Virtual File System (/vsicurl/) to stream only the Rajshahi bounding box directly from the JRC servers without downloading the entire global file.
2. If remote clipping fails or the URL format changes, it provides the exact manual fallback instructions.

Run: python3 scripts/01_download_direct.py
"""

import os
import rasterio
from rasterio.mask import mask
from shapely.geometry import box

EPOCHS = [1990, 1995, 2000, 2005, 2010, 2015, 2020]
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
BBOX = [88.45, 24.28, 88.75, 24.52]  # [lon_min, lat_min, lon_max, lat_max]

def get_jrc_vsi_url(year):
    """
    Constructs the Rasterio Virtual File System URL to read directly inside the remote ZIP.
    JRC Open Data exact path structure for R2023A 3 arcsec WGS84, Tile R7_C27 (Rajshahi).
    """
    base = "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_S_GLOBE_R2023A"
    folder = f"GHS_BUILT_S_E{year}_GLOBE_R2023A_4326_3ss"
    filename = f"{folder}_V1_0_R7_C27"
    zip_url = f"{base}/{folder}/V1-0/tiles/{filename}.zip"
    tif_name = f"{filename}.tif"
    
    # Prefix with zip+ and suffix with !filename.tif for Rasterio VFS
    return f"zip+{zip_url}!{tif_name}"

def download_and_clip_epoch(year):
    out_file = os.path.join(DATA_DIR, f"ghsl_{year}_raj.tif")
    if os.path.exists(out_file):
        print(f"[SKIP] {year}: {out_file} already exists.")
        return True

    print(f"\n── Fetching and clipping {year} directly from JRC servers ──")
    vsi_url = get_jrc_vsi_url(year)
    geom = [box(*BBOX).__geo_interface__]

    try:
        # Open remote ZIP and clip bounding box on the fly
        with rasterio.open(vsi_url) as src:
            out_img, out_transform = mask(src, geom, crop=True, nodata=0)
            out_meta = src.meta.copy()
            out_meta.update({
                "driver": "GTiff",
                "height": out_img.shape[1],
                "width": out_img.shape[2],
                "transform": out_transform,
                "nodata": 0
            })
            
            with rasterio.open(out_file, "w", **out_meta) as dest:
                dest.write(out_img)
        print(f"[OK] Successfully saved {out_file}")
        return True
    
    except Exception as e:
        print(f"[ERROR] Failed to fetch {year} via VFS: {e}")
        return False

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    all_success = True
    
    for yr in EPOCHS:
        success = download_and_clip_epoch(yr)
        if not success:
            all_success = False

    if not all_success:
        print("\n" + "="*80)
        print("⚠ MANUAL DOWNLOAD REQUIRED ⚠")
        print("The JRC server URL format may have changed, or VFS streaming timed out.")
        print("Please follow these steps to download manually:")
        print("1. Go to: https://ghsl.jrc.ec.europa.eu/download.php")
        print("2. Product: GHS-BUILT-S")
        print("3. Resolution: R100m, CRS: EPSG:4326 (WGS84)")
        print("4. Select the tile covering Rajshahi (88.6°E, 24.4°N)")
        print("5. Download the files for the missing epochs into this 'data' folder.")
        print("6. Run 'python3 scripts/01_clip_direct.py <downloaded.tif> <output_raj.tif>'")
        print("="*80)
