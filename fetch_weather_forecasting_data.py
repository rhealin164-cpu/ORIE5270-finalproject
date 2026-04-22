#!/usr/bin/env python3
"""Run the weather forecasting fetcher from repo root: delegates to data_processing/fetch_weather_forecasting_data.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_REAL = _ROOT / "data_processing" / "fetch_weather_forecasting_data.py"

if not _REAL.is_file():
    print(f"ERROR: expected script at {_REAL}", file=sys.stderr)
    raise SystemExit(1)

raise SystemExit(subprocess.call([sys.executable, str(_REAL), *sys.argv[1:]]))
