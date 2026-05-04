# Feature engineering (Tompkins County, NY)

Turn **`data_processing/data/processed/modeling_table.csv`** into a numeric feature matrix + **`AQI`** target. Main code: **`features.py`**; typical output: **`features_table.csv`** (features + `AQI`, metadata columns dropped).

## Layout

```
feature_engineering/
├── features.py
├── features_table.csv   # generated / versioned snapshot
└── README.md
```

## Requirements

Python **3.10+**, `pandas`, `numpy` (project root `requirements.txt` installs everything).

## Quick start

From **repo root**:

```bash
python feature_engineering/features.py
```

Writes/updates `feature_engineering/features_table.csv` (paths inside script assume repo layout).

## Use from Python

```python
import pandas as pd
from feature_engineering.features import build_features, get_X_y

raw = pd.read_csv("data_processing/data/processed/modeling_table.csv")
X, y = get_X_y(build_features(raw))
# or load pre-built table: pd.read_csv("feature_engineering/features_table.csv")
```

## What gets engineered

- **AQI history:** lags (1,2,3,7 d), rolling mean/std (causal / shifted), short/long diffs  
- **Calendar:** month, weekday, season; sin/cos encoding for month & weekday  
- **Weather:** e.g. `temp_range`, cyclic `wind_dir_sin` / `wind_dir_cos` (raw wind ° dropped in `get_X_y`)  
- Base weather columns from the modeling table are kept where numeric

See **`features.py`** docstrings for exact column lists and drop rules.

**Engineered columns & screening:** [docs/features.md](../docs/features.md).

## Output table

`features_table.csv`: one row per day after lag/rolling warmup rows are dropped; **no NaNs** in core engineered columns; **`AQI`** last column for convenience.
