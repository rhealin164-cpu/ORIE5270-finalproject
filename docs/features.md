# Features for modeling

Reference for **`feature_engineering/features.py`**: engineered columns, rows removed, and columns **dropped** before `X` / `y`. Authoritative implementation: source code and docstrings in `features.py`.

---

## Pipeline (`build_features`)

1. Sort by **`date`**.  
2. **Lag AQI:** `aqi_lag_1`, `aqi_lag_2`, `aqi_lag_3`, `aqi_lag_7`.  
3. **Rolling AQI** (past-only via `shift(1)` before rolling): `aqi_roll_mean_3`, `aqi_roll_mean_7`, `aqi_roll_std_7`.  
4. **Trend:** `aqi_diff_1` (= lag₁ − lag₂), `aqi_diff_7` (= lag₁ − lag₇).  
5. **Calendar:** `month`, `weekday`, `season`; cyclic `month_sin`, `month_cos`, `weekday_sin`, `weekday_cos`.  
6. **Weather-derived:** `temp_range` (= max − min), `wind_dir_sin`, `wind_dir_cos` from **`winddirection_10m_dominant`** (degrees → radians → sin/cos).  
7. **Row drop:** drop rows with NaN in **`aqi_lag_1`…`aqi_lag_7`, `aqi_roll_mean_3`, `aqi_roll_mean_7`, `aqi_roll_std_7`** (warm-up period).

---

## Engineered columns (19)

| Group | Columns |
|-------|---------|
| Lag | `aqi_lag_1`, `aqi_lag_2`, `aqi_lag_3`, `aqi_lag_7` |
| Rolling | `aqi_roll_mean_3`, `aqi_roll_mean_7`, `aqi_roll_std_7` |
| Trend | `aqi_diff_1`, `aqi_diff_7` |
| Time | `month`, `weekday`, `season`, `month_sin`, `month_cos`, `weekday_sin`, `weekday_cos` |
| Weather-derived | `temp_range`, `wind_dir_sin`, `wind_dir_cos` |

---

## Base numeric columns kept in `features_table.csv` (16)

These come from **`modeling_table`** and remain in the modeling matrix (still numeric after pipeline):

`grid_latitude`, `grid_longitude`, `weathercode`, `temperature_2m_mean`, `temperature_2m_max`, `temperature_2m_min`, `daylight_duration`, `sunshine_duration`, `precipitation_sum`, `rain_sum`, `snowfall_sum`, `precipitation_hours`, `windspeed_10m_max`, `windgusts_10m_max`, `shortwave_radiation_sum`, `Number of Sites Reporting`

Together with the **19 engineered** columns → **35 features** + **`AQI`** target → **36 columns** in `features_table.csv` (see `save_features_table` in `features.py`).

---

## Columns removed in `get_X_y` (not in `X`)

Dropped if present (non-predictive, leakage risk, or replaced):

| Column(s) | Reason |
|-----------|--------|
| `AQI` | Target |
| `Category` | Derived from AQI |
| `date` | Encoded via time features |
| `Defining Parameter`, `Defining Site`, `State Name`, `county Name`, `location_label`, `forecasting` | Metadata / IDs |
| `sunrise`, `sunset` | Strings / not used as numeric features |
| `winddirection_10m_dominant` | Replaced by `wind_dir_sin`, `wind_dir_cos` |

Only columns **present** in the DataFrame are dropped (`get_X_y` filters the list).

---

## Output file

- **`feature_engineering/features_table.csv`**: rows after lag/rolling warmup; core engineered columns **non-null**; **`AQI`** typically last column for convenience.  
- Regenerate: `python feature_engineering/features.py` or `save_features_table(...)`.

---

## Related

- [Data dictionary](data_dictionary.md) — `modeling_table.csv` and raw inputs.
