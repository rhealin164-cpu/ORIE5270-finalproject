import numpy as np
import pandas as pd
import matplotlib
import pytest

matplotlib.use("Agg")

from model_training.model import (
    prepare_features,
    split_data,
    evaluate_model,
    train_random_forest,
    train_xgboost,
    plot_feature_importance,
    plot_actual_vs_predicted,
    run_model_pipeline,
    xgboost_available,
)


def sample_model_df():
    return pd.DataFrame({
        "temperature_2m_mean": [10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
        "precipitation_sum": [0, 1, 0, 2, 0, 1, 0, 0, 1, 0],
        "windspeed_10m_max": [3, 4, 5, 4, 3, 5, 6, 4, 3, 2],
        "AQI": [30, 35, 38, 45, 48, 55, 60, 65, 70, 75],
        "non_numeric_col": ["a"] * 10,
    })


def test_prepare_features():
    df = sample_model_df()
    X, y = prepare_features(df)

    assert "AQI" not in X.columns
    assert "non_numeric_col" not in X.columns
    assert len(X) == len(y)


def test_split_data():
    df = sample_model_df()
    X, y = prepare_features(df)

    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.3)

    assert len(X_train) == 7
    assert len(X_test) == 3
    assert len(y_train) == 7
    assert len(y_test) == 3


def test_train_random_forest():
    df = sample_model_df()
    X, y = prepare_features(df)
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.3)

    model = train_random_forest(X_train, y_train)

    assert model is not None
    assert hasattr(model, "predict")


@pytest.mark.skipif(
    not xgboost_available(),
    reason="XGBoost native library unavailable (e.g. missing libomp on macOS)",
)
def test_train_xgboost():
    df = sample_model_df()
    X, y = prepare_features(df)
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.3)

    model = train_xgboost(X_train, y_train)

    assert model is not None
    assert hasattr(model, "predict")


def test_evaluate_model():
    y_true = np.array([10, 20, 30])
    y_pred = np.array([12, 18, 33])

    metrics = evaluate_model(y_true, y_pred)

    assert "MSE" in metrics
    assert "MAE" in metrics
    assert "R2" in metrics


def test_plot_feature_importance(monkeypatch):
    import matplotlib.pyplot as plt

    monkeypatch.setattr(plt, "show", lambda: None)

    df = sample_model_df()
    X, y = prepare_features(df)
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.3)

    model = train_random_forest(X_train, y_train)
    importance = plot_feature_importance(model, X.columns, "Test Feature Importance")

    assert isinstance(importance, pd.DataFrame)
    assert "Feature" in importance.columns
    assert "Importance" in importance.columns


def test_plot_actual_vs_predicted(monkeypatch):
    import matplotlib.pyplot as plt

    monkeypatch.setattr(plt, "show", lambda: None)

    y_test = pd.Series([10, 20, 30])
    y_pred = np.array([11, 19, 31])

    plot_actual_vs_predicted(y_test, y_pred, "Test Plot")


def test_run_model_pipeline_without_plots(tmp_path):
    df = sample_model_df()
    csv_path = tmp_path / "features_table.csv"
    df.to_csv(csv_path, index=False)

    results, rf_importance, xgb_importance = run_model_pipeline(
        data_path=str(csv_path),
        show_plots=False
    )

    assert isinstance(results, pd.DataFrame)
    assert "Random Forest" in set(results["Model"])
    if xgboost_available():
        assert "XGBoost" in set(results["Model"])
        assert len(results) == 2
    else:
        assert len(results) == 1
    assert rf_importance is None
    assert xgb_importance is None