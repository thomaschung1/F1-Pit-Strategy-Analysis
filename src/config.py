from pathlib import Path

# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "data" / "processed" / "f1_pit_strategy_model_data.csv"
MODEL_PATH = BASE_DIR / "models" / "random_forest_model.pkl"
MODEL_COLUMNS_PATH = BASE_DIR / "models" / "model_columns.pkl"
FIGURES_DIR = BASE_DIR / "figures"

METRICS_PATH = BASE_DIR / "data" / "processed" / "model_metrics.csv"
FEATURE_IMPORTANCE_PATH = BASE_DIR / "data" / "processed" / "feature_importance.csv"