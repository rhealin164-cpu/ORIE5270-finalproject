# Ozone AQI Prediction in Tompkins County, NY

This repository contains the final project for ORIE5270 (Machine Learning), focusing on predicting ozone Air Quality Index (AQI) in Tompkins County, NY. 

---

## Project Overview

The project's objective is to predict next-day ozone AQI in Tompkins County, NY based on historical weather patterns and environmental AQI records. This can provide community stakeholders and public officials with timely predictions to support health and planning decisions.

We utilize Random Forest and XGBoost regression models, with a well-defined data processing and feature engineering pipeline.

---

## Repository Structure

```
data_processing/
├── README.md                 # this file
├── fetch_weather_forecasting_data.py  # download forecasting archive → CSV
├── merge_datasets.py         # merge AQI + weather → modeling table (+ extras)
├── clean_data.py             # optional: re-clean an existing modeling CSV
└── data/
    ├── raw/                  # inputs you keep or regenerate
    │   ├── daily_weather_forecasting.csv
    │   ├── daily_aqi_by_county_2024.csv
    │   └── daily_aqi_by_county_2025.csv
    ├── processed/            # outputs ready for modeling
    │   ├── modeling_table.csv
    │   └── daily_air_quality.csv   # Tompkins-only slice from raw AQI (for quick checks)
    └── sample/
        └── sample_modeling_table.csv   # first ~50 rows of modeling_table

feature_engineering/
  ├── features_table.csv
  ├── README.md
  └── features.py
model_training/
  └── model.py
test/
  ├── test_features.py
  ├── test_merge.py
  └── test_model.py
README.md
requirements.txt
```

- **data_processing/**: Scripts for downloading, cleaning, and merging weather and AQI data.
- **feature_engineering/**: Feature generation and transformation utilities.
- **model_training/**: Model training and evaluation code (Random Forest, XGBoost).
- **test/**: Unit tests for data processing, feature engineering, and model functionality.

---

## Data sources

What each input file is **supposed** to come from (cite these in papers / homework):

| File(s) in `data/raw/` | Source | Notes |
|------------------------|--------|--------|
| `daily_weather_forecasting.csv` | **[Open-Meteo Historical Forecast API](https://open-meteo.com/en/docs/historical-forecast-api)** | This repo calls `https://historical-forecast-api.open-meteo.com/v1/forecast` (archived high-resolution **forecast** model fields stitched over time; not ERA5 reanalysis). Typical availability from ~2022 onward. Point query uses the nearest grid cell (`grid_latitude` / `grid_longitude` in the CSV). Column `forecasting` identifies the series (`open_meteo_historical_forecasting`). Hourly default file: `hourly_weather_forecasting.csv`. |
| `daily_aqi_by_county_2024.csv`, `daily_aqi_by_county_2025.csv` | **[EPA AQS Air Data — Daily AQI by County](https://aqs.epa.gov/aqsweb/airdata/download_files.html#AQI)** | Download the **“Daily AQI by County”** files for the years you need from that page (this project’s raw AQI CSVs come from there). Column names match the EPA export (state/county, FIPS, `Defining Parameter`, etc.). Follow EPA’s **terms of use / citation** on the Air Data site for reports or publications. |

Processed files (`modeling_table.csv`, `daily_air_quality.csv`, `sample_…`) are **derived** from the above; cite the original weather + AQI sources, not “this repo” as the primary data origin.

(Please refer to code comments in `fetch_weather_forecasting_data.py` for exact endpoints and usage.)

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/rhealin164-cpu/ORIE5270-finalproject-ozone-aqi-prediction.git
   cd ORIE5270-finalproject
   ```
2. Create and activate a Python virtual environment (optional but recommended):
   **Mac/Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows**
   ```bash
   python3 -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## How to Run

1. **Fetch and prepare the data**:
    ```bash
    python data_processing/fetch_weather_forecasting_data.py
    python data_processing/clean_data.py
    python data_processing/merge_datasets.py
    ```

2. **Generate features**:
    ```bash
    python feature_engineering/features.py
    ```

3. **Train and evaluate models**:
    ```bash
    python model_training/model.py
    ```

Intermediate and output files will be written to a local `data/` folder (created if not present).

---

## Testing

Run unit tests using `pytest`:

```bash
pytest --cov=. --cov-report=term-missing
```

**Test Coverage**:  
- Total tests: 28
- Total code coverage: **84%**

Core modules coverage:
- data_processing.merge_datasets: 90%
- feature_engineering.features: 82%
- model_training.model: 94%


> **Note:** API fetching modules are not heavily unit tested due to their reliance on external APIs and variable network conditions.

---

## Contributors
- _Huizhi Deng_ (`hd424`)
- _Yunqi Cui_ (`yc2963`)
- _Sirui Lin_ (`sl3669`)
- _Ziyi Guan_ (`zg359`)



---

For any questions, please contact [yc2963@cornell.edu].
