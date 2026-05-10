import argparse
from pathlib import Path

# pyrefly: ignore [missing-import]
import joblib
# pyrefly: ignore [missing-import]
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import KFold
# pyrefly: ignore [missing-import]
from xgboost import XGBRegressor

from features import extract_features


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "passwords.csv"
MODEL_PATH = ROOT / "ml" / "password-model.xgb"


def scale_score(guesses_log10: float) -> float:
    return float(np.clip((guesses_log10 / 18.0) * 100.0, 0.0, 100.0))


def build_dataset(csv_path: Path, max_rows: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    df = pd.read_csv(csv_path)
    if "password" not in df.columns or "guesses_log10" not in df.columns:
        raise ValueError("CSV must contain 'password' and 'guesses_log10' columns")

    cleaned = df[["password", "guesses_log10"]].copy()
    cleaned["guesses_log10"] = pd.to_numeric(cleaned["guesses_log10"], errors="coerce")
    cleaned = cleaned.dropna(subset=["password", "guesses_log10"])
    cleaned["password"] = cleaned["password"].astype(str).str.strip()
    cleaned = cleaned[cleaned["password"] != ""]

    if cleaned.empty:
        raise ValueError("No valid rows after cleaning 'password' and 'guesses_log10'.")

    if max_rows is not None and max_rows > 0 and len(cleaned) > max_rows:
        cleaned = cleaned.sample(n=max_rows, random_state=42).reset_index(drop=True)
        print(f"Using sampled subset: {len(cleaned)} rows")

    feature_cache: dict[str, list[float]] = {}
    feature_rows: list[list[float]] = []
    total_rows = len(cleaned)
    for index, password in enumerate(cleaned["password"], start=1):
        if password not in feature_cache:
            feature_cache[password] = extract_features(password)
        feature_rows.append(feature_cache[password])
        if index % 10000 == 0 or index == total_rows:
            print(f"Extracted features for {index}/{total_rows} rows")

    features = np.array(feature_rows, dtype=np.float32)
    labels = np.array(
        [scale_score(value) for value in cleaned["guesses_log10"]],
        dtype=np.float32,
    )
    return features, labels


def train_model(x: np.ndarray, y: np.ndarray) -> XGBRegressor:
    model = XGBRegressor(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
    )

    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    for fold, (train_idx, test_idx) in enumerate(kf.split(x), start=1):
        x_train, x_test = x[train_idx], x[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        fold_model = XGBRegressor(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
        )
        fold_model.fit(x_train, y_train)
        preds = fold_model.predict(x_test)
        mae = mean_absolute_error(y_test, preds)
        print(f"Fold {fold} MAE: {mae:.4f}")

    model.fit(x, y)
    return model


def main() -> None:
    parser = argparse.ArgumentParser(description="Train password strength model")
    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        help="Optional sample size for faster training on very large datasets",
    )
    args = parser.parse_args()

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Training data not found: {DATA_PATH}")

    x, y = build_dataset(DATA_PATH, max_rows=args.max_rows)
    model = train_model(x, y)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
