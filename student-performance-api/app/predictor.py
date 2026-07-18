from pathlib import Path

import joblib
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "model.pkl"

FEATURES = [
    "hours_studied",
    "attendance_percentage",
    "previous_grade",
    "sleep_hours",
    "assignments_completed",
]


class Predictor:
    def __init__(self, model_path: Path = MODEL_PATH):
        self.model = joblib.load(model_path)

    def predict(self, features: dict) -> dict:
        X = pd.DataFrame([features], columns=FEATURES)
        pred = self.model.predict(X)[0]
        proba = self.model.predict_proba(X)[0][pred]
        return {
            "prediction": "Pass" if pred == 1 else "Fail",
            "probability": round(float(proba), 4),
        }
