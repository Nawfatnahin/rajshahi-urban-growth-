# Rajshahi Urban Growth Observatory 🏙️✨

> A quantitative, aesthetic visualization of Rajshahi's expanding urban footprint from 1990 to 2020.

**[Live Observatory]({GITHUB_PAGES_URL})** *(Note: Link will be active once GitHub Pages is deployed)*

## 📖 About the Project

This project was built to visually and mathematically track the rapid urban expansion of Rajshahi city over the last three decades. It transforms dense, complex geospatial satellite data into an elegant, interactive, and easy-to-understand web experience.

By utilizing high-contrast color palettes and luxury glassmorphism UI elements, the observatory allows users to scrub through time and watch the city's peri-urban sprawl and infrastructural density evolve, stacked layer upon layer.

## 🎯 Objective

The core objective is to provide an **honest, data-driven visualization** of urban sprawl. Instead of using abstract shapes or generalized boundaries, this observatory relies on authentic vector data extracted directly from satellite imagery. It aims to help researchers, urban planners, and local enthusiasts instantly grasp how quickly and vastly Rajshahi has expanded over 30 years.

## 🛠️ Why It Was Made

Urban growth is often discussed but rarely "felt." Reading that a city grew by 20 square kilometers doesn't hold the same weight as watching the infrastructure physically stretch out across the map. I wanted to bridge the gap between technical GIS data and human intuition, creating a tool that is as beautiful to look at as it is accurate to study. 

## 🚀 How to Use

1. **The Timeline:** At the bottom right of the screen, you will find a timeline slider ranging from 1990 to 2020. Drag it to scrub through the years.
2. **Auto-Play:** Click the play button next to the slider to watch the city grow autonomously.
3. **Diagnostic Data:** The left panel provides real-time geospatial statistics, calculating the exact square-kilometer footprint of the city for the selected year using Turf.js.
4. **Interactive Map:** You can drag, pan, and zoom around the map to explore specific neighborhoods and how they developed over the decades.
5. **Toggle Panels:** If you want an unobstructed view of the map, click the small arrow buttons attached to the corners of the floating panels to slide them off-screen.

## 📡 Data Collection & Methodology

The authentic geospatial data powering this observatory is derived from the **Global Human Settlement Layer (GHSL)**, an open-source initiative maintained by the **European Commission's Joint Research Centre (JRC)**. 

Specifically, this uses the `GHS_BUILT_S` (Built-up Surface) multitemporal dataset. This data is produced by running advanced machine learning algorithms over decades of massive satellite imagery archives (including Landsat and Sentinel). To adapt it for this lightweight web visualization, the dense raster pixel grids were mathematically vectorized into precise GeoJSON polygons.

## ⚙️ Technical Stack

- **Frontend:** HTML5, Tailwind CSS
- **Mapping:** Leaflet.js over ESRI World Imagery
- **Geospatial Analysis:** Turf.js (Real-time area calculation)
