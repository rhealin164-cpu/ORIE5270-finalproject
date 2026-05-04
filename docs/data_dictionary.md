# Data dictionary

Column-level reference for the **data processing** outputs and related files.  
Units below match **`fetch_weather_forecasting_data.py`** defaults (°C, mm, m/s for wind) unless noted. For API field semantics see [Open-Meteo Historical Forecast API](https://open-meteo.com/en/docs/historical-forecast-api).

---

## `data/processed/modeling_table.csv`

One row per **calendar day** after cleaning: **Tompkins County, NY**, weather + county AQI aligned on **`date`**. Redundant merge keys may be dropped in `merge_datasets.py` (e.g. raw `Date`, FIPS-only keys, `date_et`).

| Column | Type | Description |
|--------|------|-------------|
| `location_label` | string | AOI tag from fetch (e.g. `tompkins_county_ny`). |
| `forecasting` | string | Series id (`open_meteo_historical_forecasting`). |
| `grid_latitude` | float | Nearest forecast grid latitude (°N). |
| `grid_longitude` | float | Nearest forecast grid longitude (°E, negative = W). |
| `weathercode` | int | WMO-style daily weather code (see Open-Meteo docs). |
| `temperature_2m_mean` | float | Daily mean air temperature at 2 m (°C). |
| `temperature_2m_max` | float | Daily max 2 m temperature (°C). |
| `temperature_2m_min` | float | Daily min 2 m temperature (°C). |
| `sunrise` | string/datetime | Local sunrise (parsed in cleaning). |
| `sunset` | string/datetime | Local sunset. |
| `daylight_duration` | float | Day length (seconds). |
| `sunshine_duration` | float | Bright sunshine duration (seconds). |
| `precipitation_sum` | float | Total precipitation including snow melt (mm). |
| `rain_sum` | float | Rain (mm). |
| `snowfall_sum` | float | Snowfall (cm, Open-Meteo convention). |
| `precipitation_hours` | float | Hours with measurable precipitation. |
| `windspeed_10m_max` | float | Max 10 m wind speed (m/s). |
| `windgusts_10m_max` | float | Max wind gust (m/s). |
| `winddirection_10m_dominant` | int | Dominant wind direction (°, meteorological). |
| `shortwave_radiation_sum` | float | Daily sum of shortwave radiation (MJ/m²). |
| `date` | date | **Merge key**: calendar date (America/New_York). |
| `State Name` | string | EPA: state (e.g. `New York`). |
| `county Name` | string | EPA: county (`Tompkins`). |
| `AQI` | float/int | US AQI (0–500; invalid/out-of-range may be set missing before row drop). |
| `Category` | string | EPA AQI category (e.g. Good, Moderate). |
| `Defining Parameter` | string | Pollutant driving the reported AQI (e.g. Ozone, PM2.5). |
| `Defining Site` | string | Site / monitor id for the defining parameter. |
| `Number of Sites Reporting` | float/int | Sites contributing to the county rollup. |

### EPA AQI categories (interpretation)

Standard **AQI** category cutoffs (same scale regardless of pollutant):

| AQI range | Category |
|-----------|----------|
| 0–50 | Good |
| 51–100 | Moderate |
| 101–150 | Unhealthy for Sensitive Groups |
| 151–200 | Unhealthy |
| 201–300 | Very Unhealthy |
| 301–500 | Hazardous |

Concentration breakpoints by pollutant: [EPA AQI breakpoints](https://aqs.epa.gov/aqsweb/documents/codetables/aqi_breakpoints.html). This pipeline may treat AQI &gt; 500 as invalid in `clean_data.py`.

---

## `data/raw/daily_weather_forecasting.csv`

Daily Open-Meteo historical-forecast export. Includes the **same weather columns** as in `modeling_table` plus typically:

| Column | Description |
|--------|-------------|
| `forecasting` | `open_meteo_historical_forecasting` for this pipeline. |
| `date_local` | Local calendar day string from the API. |
| `date_et` | Timestamp with NY offset; used before merge, usually not in `modeling_table`. |

---

## `data/raw/daily_aqi_by_county_*.csv`

County-level daily AQI from **[EPA AQS — Daily AQI by County](https://aqs.epa.gov/aqsweb/airdata/download_files.html#AQI)**. National file; code filters **NY + Tompkins**. Typical columns include:

`State Name`, `county Name`, `State Code`, `County Code`, `Date`, `AQI`, `Category`, `Defining Parameter`, `Defining Site`, `Number of Sites Reporting` (headers match EPA export; note possible leading space in `county Name` as in source).

---

## `data/processed/daily_air_quality.csv`

Tompkins-only rows cut from raw EPA file(s); **EPA-like columns**, **no** weather columns.

---

## `data/sample/sample_modeling_table.csv`

First ~50 rows of `modeling_table.csv` for quick inspection; **same schema** as `modeling_table.csv`.

---

## Attribution

- **Weather:** [Open-Meteo](https://open-meteo.com/) terms and model attribution.  
- **AQI:** [EPA AQS Air Data](https://aqs.epa.gov/aqsweb/airdata/download_files.html#AQI) terms of use and citation.  
- **Merged products:** cite **Open-Meteo + EPA** (or your actual sources) for underlying measurements.
