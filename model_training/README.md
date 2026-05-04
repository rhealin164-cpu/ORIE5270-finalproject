# Model training (Tompkins County, NY)

Train **regressors** on **`feature_engineering/features_table.csv`**: **Random Forest** always; **XGBoost** when the native library loads (see below). Metrics: **MSE**, **MAE**, **R²**; optional **matplotlib** diagnostic plots.

## Layout

```
model_training/
├── model.py
└── README.md
```

## Requirements

Project root **`requirements.txt`** (`scikit-learn`, `pandas`, `matplotlib`, `xgboost`, …). Python **3.10+**.

## Input

Default CSV (relative to **repo root**):

`feature_engineering/features_table.csv`

Override by passing a path into `load_data(...)` or `run_model_pipeline(data_path=...)`.

`prepare_features` keeps **numeric columns only**, uses **`AQI`** as target, drops it from `X`. Feature definitions: **[docs/features.md](../docs/features.md)**.

## Quick start

From **repo root**:

```bash
python model_training/model.py
```

Prints the metrics table; opens figures if your backend supports `matplotlib` `show()`.

## Models & split

| Piece | Setting |
|-------|---------|
| Split | 80% train / 20% test, `random_state=42` |
| Random Forest | `RandomForestRegressor(n_estimators=200, random_state=42)` |
| XGBoost | `XGBRegressor(n_estimators=200, learning_rate=0.05, max_depth=4, random_state=42)` |

If **`xgboost_available()`** is false (common on macOS without OpenMP), the pipeline still fits **Random Forest** only. Install OpenMP: `brew install libomp`.

## Use from Python

```python
from model_training.model import run_model_pipeline, xgboost_available

results, rf_imp, xgb_imp = run_model_pipeline(show_plots=False)
print(results)
print("XGBoost usable:", xgboost_available())
```

Lower-level helpers: `load_data`, `prepare_features`, `split_data`, `train_random_forest`, `train_xgboost`, `evaluate_model`, plotting helpers — see **`model.py`**.
