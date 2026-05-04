# Data processing (Tompkins County, NY)

Pull **Open-Meteo historical-forecast** daily weather, merge with **EPA Daily AQI by County** (NY / Tompkins), clean, and write **`data/processed/modeling_table.csv`** for downstream feature engineering or modeling.

## Layout

```
data_processing/
├── fetch_weather_forecasting_data.py
├── merge_datasets.py
├── clean_data.py
└── data/
    ├── raw/       # weather + AQI CSVs you download or regenerate
    └── processed/ # modeling_table.csv, daily_air_quality.csv, etc.
```

## Requirements

Python **3.10+**, `pandas`, `requests` (see project root `requirements.txt` for full env).

## Quick start

From **`data_processing/`** (or prefix paths with `data_processing/` from repo root):

```bash
# 1) Weather → data/raw/daily_weather_forecasting.csv
python fetch_weather_forecasting_data.py --tompkins --start 2024-01-01 --end 2025-12-31 --sleep-sec 0

# 2) Merge AQI + weather → data/processed/modeling_table.csv
python merge_datasets.py

# 3) Re-clean only (optional)
python clean_data.py                    # default: drop incomplete rows
python clean_data.py --keep-incomplete
```

Single-year AQI example:

```bash
python merge_datasets.py --aqi data/raw/daily_aqi_by_county_2025.csv
```

## Scripts

| Script | Role |
|--------|------|
| `fetch_weather_forecasting_data.py` | Open-Meteo Historical Forecast API; `--tompkins`, date range, `--freq daily\|hourly`, output path. |
| `merge_datasets.py` | Filter Tompkins from EPA county files, join to weather on calendar **`date`** (America/New_York), clean. |
| `clean_data.py` | Dtypes, dedupe by `date`, AQI sanity checks; optional `--keep-incomplete`. |

## Data sources (citations)

| Raw file(s) under `data/raw/` | Source |
|-------------------------------|--------|
| `daily_weather_forecasting.csv` | [Open-Meteo Historical Forecast API](https://open-meteo.com/en/docs/historical-forecast-api) |
| `daily_aqi_by_county_*.csv` | [EPA AQS — Daily AQI by County](https://aqs.epa.gov/aqsweb/airdata/download_files.html#AQI) |

Place EPA exports in `data/raw/`; pipeline keeps **New York / Tompkins**. For writing or papers, cite **EPA + Open-Meteo**, not only this repo. Endpoints and flags: see comments in `fetch_weather_forecasting_data.py`.

**Full column definitions:** [docs/data_dictionary.md](../docs/data_dictionary.md).

## Merge / cleaning (short)

- Join uses **outer** merge; default cleaning **drops** rows missing solid AQI or core weather (unless `--keep-incomplete`).
- Weather times are normalized to one **`date`** per day for joining.

## Attribution

Follow **Open-Meteo** and **EPA Air Data** terms / citation for the underlying data; merged CSVs are derivatives—still cite the original sources.
