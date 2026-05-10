from pathlib import Path

import joblib
import onnx
from onnxmltools import convert_xgboost
from onnxmltools.convert.common.data_types import FloatTensorType


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "ml" / "password-model.xgb"
OUTPUT_PATH = ROOT.parent / "frontend" / "public" / "model" / "password-model.onnx"


def main() -> None:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Trained model not found: {MODEL_PATH}")

    model = joblib.load(MODEL_PATH)
    initial_types = [("float_input", FloatTensorType([None, 16]))]
    onnx_model = convert_xgboost(model, initial_types=initial_types)
    onnx.save_model(onnx_model, OUTPUT_PATH.as_posix())
    print(f"Saved ONNX model to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
