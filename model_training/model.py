from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


DEFAULT_FEATURES_PATH = _repo_root() / "feature_engineering" / "features_table.csv"


def xgboost_available() -> bool:
    """False if xgboost is missing or fails to load native libs (e.g. macOS without libomp)."""
    try:
        import xgboost  # noqa: F401
        from xgboost import XGBRegressor  # noqa: F401
    except Exception:
        return False
    return True


def load_data(path=None):
    resolved = Path(path) if path is not None else DEFAULT_FEATURES_PATH
    return pd.read_csv(resolved)


def prepare_features(df, target="AQI"):
    numeric_df = df.select_dtypes(include=["number"])
    X = numeric_df.drop(columns=[target])
    y = numeric_df[target]
    return X, y


def split_data(X, y, test_size=0.2, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def evaluate_model(y_true, y_pred):
    return {
        "MSE": mean_squared_error(y_true, y_pred),
        "MAE": mean_absolute_error(y_true, y_pred),
        "R2": r2_score(y_true, y_pred),
    }


def train_random_forest(X_train, y_train):
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    return model


def train_xgboost(X_train, y_train):
    try:
        from xgboost import XGBRegressor
    except Exception as exc:
        raise ImportError(
            "XGBoost could not be loaded. On macOS install OpenMP: brew install libomp"
        ) from exc
    model = XGBRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=4,
        random_state=42,
    )
    model.fit(X_train, y_train)
    return model


def plot_actual_vs_predicted(y_test, y_pred, title):
    plt.figure(figsize=(6, 5))
    plt.scatter(y_test, y_pred)

    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())

    plt.plot([min_val, max_val], [min_val, max_val], "r-")
    plt.xlabel("Actual AQI")
    plt.ylabel("Predicted AQI")
    plt.title(title)
    plt.show()


def plot_feature_importance(model, feature_names, title):
    importance = pd.DataFrame({
        "Feature": feature_names,
        "Importance": model.feature_importances_,
    })

    importance = importance.sort_values(by="Importance", ascending=False).head(10)

    plt.figure(figsize=(8, 5))
    plt.barh(importance["Feature"], importance["Importance"])
    plt.xlabel("Feature Importance")
    plt.ylabel("Feature")
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.show()

    return importance


def run_model_pipeline(data_path=None, show_plots=True):
    df = load_data(data_path)
    X, y = prepare_features(df)

    X_train, X_test, y_train, y_test = split_data(X, y)

    rf = train_random_forest(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    rf_results = evaluate_model(y_test, y_pred_rf)

    xgb_model = None
    y_pred_xgb = None
    xgb_results = None
    if xgboost_available():
        try:
            xgb_model = train_xgboost(X_train, y_train)
            y_pred_xgb = xgb_model.predict(X_test)
            xgb_results = evaluate_model(y_test, y_pred_xgb)
        except ImportError:
            xgb_model = None
            y_pred_xgb = None
            xgb_results = None

    rows = [
        {
            "Model": "Random Forest",
            "MSE": rf_results["MSE"],
            "MAE": rf_results["MAE"],
            "R2": rf_results["R2"],
        }
    ]
    if xgb_results is not None:
        rows.append({
            "Model": "XGBoost",
            "MSE": xgb_results["MSE"],
            "MAE": xgb_results["MAE"],
            "R2": xgb_results["R2"],
        })
    results = pd.DataFrame(rows)

    rf_importance = None
    xgb_importance = None
    if show_plots:
        rf_importance = plot_feature_importance(
            rf, X.columns, "Top 10 Feature Importance - Random Forest"
        )
        if xgb_model is not None:
            xgb_importance = plot_feature_importance(
                xgb_model, X.columns, "Top 10 Feature Importance - XGBoost"
            )
        plot_actual_vs_predicted(
            y_test, y_pred_rf, "Random Forest: Actual vs Predicted AQI"
        )
        if y_pred_xgb is not None:
            plot_actual_vs_predicted(
                y_test, y_pred_xgb, "XGBoost: Actual vs Predicted AQI"
            )

    return results, rf_importance, xgb_importance


if __name__ == "__main__":
    results, rf_importance, xgb_importance = run_model_pipeline()
    print(results)
