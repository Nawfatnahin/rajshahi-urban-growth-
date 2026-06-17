# Rajshahi Urban Growth Observatory 🏙️

> A quantitative, interactive visualization of Rajshahi's expanding urban footprint from **1990 to 2020**, powered by authentic satellite-derived geospatial data.

**[🌐 Live Observatory →](https://nawfatnahin.github.io/rajshahi-urban-growth-/)**

---

## 📖 About

This observatory transforms dense, multi-decade satellite data into an elegant, human-readable web experience. Users can scrub through time and watch Rajshahi's peri-urban sprawl grow — stacked layer by layer — with real-time area calculations for every epoch.

> *Note: This application, including UI design, mapping logic, and data integration, was developed using modern AI-assisted workflows, with custom data integration, visualization design, and project direction by the author.*

---

## 🛰️ Data Source

### Primary Dataset — GHS-BUILT-S R2023A

All geospatial data in this project is sourced exclusively from the **Global Human Settlement Layer (GHSL)**, a flagship open-data initiative of the **European Commission's Joint Research Centre (JRC)**, which is one of the most trusted and peer-reviewed sources of global urban data in the world.

| Field | Detail |
|---|---|
| **Dataset Name** | GHS-BUILT-S (Built-up Surface Grid) |
| **Release** | R2023A (2023 Release A) |
| **Temporal Coverage** | 1975 – 2030 (multitemporal epochs) |
| **Epochs Used Here** | 1990, 1995, 2000, 2005, 2010, 2015, 2020 |
| **Spatial Resolution** | 100 m × 100 m per pixel (3 arc-second) |
| **Coordinate System** | EPSG:4326 — WGS84 Geographic |
| **Tile Used** | R7_C27 (covers Rajshahi, Bangladesh) |
| **Bounding Box Clipped** | 88.45°E – 88.75°E, 24.28°N – 24.52°N |
| **Format** | GeoTIFF → Cloud Optimized GeoTIFF (COG) → GeoJSON |
| **Source Institution** | European Commission — Joint Research Centre (JRC) |
| **Data Portal** | https://ghsl.jrc.ec.europa.eu/download.php |
| **License** | Creative Commons Attribution 4.0 International (CC BY 4.0) |

---

### 📜 Official Citations

If you use this project or its data derivatives in any academic or public work, you **must cite** the following:

#### Dataset Citation
> Pesaresi, M.; Politis, P. (2023). **GHS-BUILT-S R2023A — GHS built-up surface grid, derived from Sentinel-2 composite and Landsat, multitemporal (1975–2030)**. European Commission, Joint Research Centre (JRC).
>
> **DOI:** [`10.2905/9F06F36F-4B11-47EC-ABB0-4F8B7B1D72EA`](https://doi.org/10.2905/9F06F36F-4B11-47EC-ABB0-4F8B7B1d72ea)
>
> **PID:** http://data.europa.eu/89h/9f06f36f-4b11-47ec-abb0-4f8b7b1d72ea

#### Methodology Paper Citation
> Pesaresi, M., Schiavina, M., Politis, P., Freire, S., Krasnodębska, K., Uhl, J. H., Carioli, A., Corbane, C., Dijkstra, L., Florio, P., Friedrich, H. K., Gao, J., Leyk, S., Lu, L., Maffenini, L., Mari-Rivero, I., Melchiorri, M., Syrris, V., Van Den Hoek, J., & Kemper, T. (2024). **Advances on the Global Human Settlement Layer by joint assessment of Earth Observation and population survey data.** *International Journal of Digital Earth*, 17(1).
>
> **DOI:** [`10.1080/17538947.2024.2390454`](https://doi.org/10.1080/17538947.2024.2390454)

---

### 🔬 What GHS-BUILT-S Measures

The `GHS-BUILT-S` layer quantifies the **total built-up surface area** per 100 m pixel, expressed in square meters. It is produced by running supervised machine learning models over:

- **Landsat** satellite image archives (1975–2014 epochs)
- **Sentinel-2** composite imagery (2015–2020 epochs)

The model classifies each pixel based on spectral signatures, texture patterns, and temporal consistency to determine whether it contains human-built structures (rooftops, impervious surfaces, etc.). The result is a continuous-value raster — not a simple binary mask — giving a nuanced measurement of urbanization density per cell.

For this project, a pixel threshold of `> 0` is used to define the urban footprint boundary, capturing the full extent of any detected built-up surface within the Rajshahi study area.

---

## ⚙️ Data Processing Pipeline

The raw satellite data goes through a 4-step reproducible pipeline before it reaches the browser:

```
JRC Remote Servers (GeoTIFF ZIP)
        │
        ▼
[Step 1] 01_download_direct.py
  - Streams remote ZIP via Rasterio Virtual File System (/vsicurl/)
  - Clips to Rajshahi bounding box [88.45, 24.28, 88.75, 24.52]
  - Saves: ghsl_{year}_raj.tif  (raw clipped GeoTIFF, EPSG:4326)
        │
        ▼
[Step 2] 02_process_cog.py
  - Validates and re-projects to EPSG:4326 if needed
  - Converts to Cloud Optimized GeoTIFF (COG) with DEFLATE compression
  - Adds internal overviews for efficient tiling
  - Saves: ghsl_{year}_raj.cog.tif
        │
        ▼
[Step 3] 03_compute_stats.py
  - Reads COG rasters, counts urban cells (value > 500 threshold)
  - Computes: urban_cells, area_km², weighted built surface (km²)
  - Outputs a JS-compatible stats object for embedding
        │
        ▼
[Step 4] 04_vectorize_ghsl.py
  - Reads raw TIF, masks all pixels > 0
  - Extracts polygon shapes (rasterio.features.shapes)
  - Applies unary_union + 50 m buffer + 20 m simplification (Shapely)
  - Saves: ghsl_{year}_raj.geojson  (single MultiPolygon per epoch)
        │
        ▼
Browser — Leaflet.js + Turf.js render the final GeoJSON layers
```

### Processing Environment
| Tool | Version | Role |
|---|---|---|
| Python 3 | ≥ 3.9 | Pipeline runtime |
| Rasterio | ≥ 1.3 | Raster I/O and clipping |
| Shapely | ≥ 2.0 | Polygon union and smoothing |
| rio-cogeo | ≥ 3.0 | Cloud Optimized GeoTIFF export |
| NumPy | ≥ 1.24 | Raster statistics |

---

## 📊 Area Data by Epoch

Computed urban footprint area for Rajshahi using spherical polygon area calculation (equivalent to Turf.js output):

| Year | Urban Footprint (sq km) | Growth vs 1990 | YoY Delta |
|------|------------------------|-----------------|-----------|
| 1990 | 423.2 | — (baseline) | — |
| 1995 | 427.2 | +4.0 | +4.0 |
| 2000 | 430.5 | +7.3 | +3.3 |
| 2005 | 442.9 | +19.7 | +12.4 |
| 2010 | 451.4 | +28.2 | +8.5 |
| 2015 | 459.9 | +36.7 | +8.5 |
| 2020 | 464.6 | +41.4 | +4.7 |

> **Note:** These figures represent the total **built-up surface extent** (binary threshold > 0) within the clipped Rajshahi study window. They are not official administrative boundary statistics.

---

## 🚀 How to Use the Observatory

1. **Timeline Slider** — Bottom-right panel. Drag to scrub through 1990–2020.
2. **Auto-Play** — Click the ▶ button to watch the city grow autonomously at 1.5 s/epoch.
3. **Diagnostic Data** — Left panel shows the current urban extent in sq km, growth delta vs 1990, and a live Growth Trend chart.
4. **Map Controls** — Pan, zoom, and explore specific neighborhoods across the decades.
5. **Toggle Panels** — Click the small arrow buttons on any panel to collapse it for a full-screen map view.

---

## 🛠️ Technical Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, Tailwind CSS, Inter & Playfair fonts, Mobile-Responsive UI |
| Mapping Engine | [Leaflet.js](https://leafletjs.com/) v1.9.4 |
| Base Imagery | OpenStreetMap (Standard bright tiles) |
| Area Calculation | [Turf.js](https://turfjs.org/) v6 (real-time, in-browser) |
| Statistical Chart | [Chart.js](https://www.chartjs.org/) v4.4.4 |
| Data Format | GeoJSON (MultiPolygon, one feature per epoch) |

---

## 📁 Repository Structure

```
rajshahi-urban-growth/
├── index.html              # Main application (self-contained)
├── serve.py                # Simple local dev server
├── data/
│   ├── ghsl_{year}_raj.tif       # Raw clipped rasters (EPSG:4326)
│   ├── ghsl_{year}_raj.cog.tif   # Cloud Optimized GeoTIFFs
│   └── ghsl_{year}_raj.geojson   # Vectorized urban footprint (browser-ready)
├── scripts/
│   ├── 01_download_direct.py     # Download + clip from JRC servers
│   ├── 01_clip_direct.py         # Manual clip fallback
│   ├── 02_process_cog.py         # COG conversion + validation
│   ├── 03_compute_stats.py       # Area statistics from COG rasters
│   └── 04_vectorize_ghsl.py      # Raster → GeoJSON vectorization
└── README.md
```

---

## 🏛️ Institutional Acknowledgement

This project uses data produced and maintained by the **Global Human Settlement (GHS) team** at the **European Commission's Joint Research Centre (JRC)**, Ispra, Italy.

The GHSL initiative provides open, free, and scientifically validated global data on human presence on Earth. It is used by the United Nations, World Bank, and academic institutions worldwide for urban studies, disaster risk management, and sustainable development goal monitoring.

More information: [https://ghsl.jrc.ec.europa.eu](https://ghsl.jrc.ec.europa.eu)
