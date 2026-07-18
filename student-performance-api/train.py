"""
Trains the student pass/fail classifier end to end:

    load -> clean -> split -> train -> evaluate -> save

Run with:
    python train.py
"""

import json

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = [
    "hours_studied",
    "attendance_percentage",
    "previous_grade",
    "sleep_hours",
    "assignments_completed",
]
TARGET = "passed"


def load_data(path="data/students.csv"):
    df = pd.read_csv(path)
    return df


def clean_data(df):
    df = df.copy()
    # Median imputation for numeric gaps introduced by messy real-world data
    for col in FEATURES:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())
    df = df.drop_duplicates()
    return df


def train():
    df = load_data()
    print(f"Loaded {len(df)} rows")
    print("Missing values before cleaning:\n", df.isnull().sum())

    df = clean_data(df)
    print("Missing values after cleaning:\n", df.isnull().sum())

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Pipeline bundles scaling + model so the same object handles raw
    # feature values at inference time -- no separate scaler to manage.
    pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall": round(recall_score(y_test, y_pred), 4),
        "f1_score": round(f1_score(y_test, y_pred), 4),
    }

    print("\n=== Evaluation ===")
    for k, v in metrics.items():
        print(f"{k}: {v}")
    print("\nConfusion matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification report:\n", classification_report(y_test, y_pred))

    joblib.dump(pipeline, "model/model.pkl")
    with open("model/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print("\nSaved model to model/model.pkl")
    return metrics


if __name__ == "__main__":
    train()
