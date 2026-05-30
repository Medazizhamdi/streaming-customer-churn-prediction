"""Batch prediction entry point for new streaming churn data."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd

from feature_engineering import add_behavioral_features, adapt_telco_to_streaming


def risk_level(probability: float) -> str:
    if probability >= 0.70:
        return "High"
    if probability >= 0.40:
        return "Medium"
    return "Low"


def prepare_input(path: str) -> pd.DataFrame:
    raw = pd.read_csv(path)
    if "customerID" in raw.columns:
        return add_behavioral_features(adapt_telco_to_streaming(raw))
    return raw.copy()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="CSV file containing customers.")
    parser.add_argument("--model", default="models/best_model.pkl", help="Trained model path.")
    parser.add_argument("--output", default="outputs/predictions_churn.csv", help="Prediction output CSV.")
    parser.add_argument("--threshold", type=float, default=0.5, help="Decision threshold.")
    args = parser.parse_args()

    data = prepare_input(args.input)
    customer_ids = data["customer_id"]
    X = data.drop(columns=["customer_id", "churn"], errors="ignore")
    model = joblib.load(args.model)
    probabilities = model.predict_proba(X)[:, 1]

    predictions = pd.DataFrame(
        {
            "customer_id": customer_ids,
            "churn_probability": probabilities.round(4),
            "predicted_class": (probabilities >= args.threshold).astype(int),
            "risk_level": [risk_level(p) for p in probabilities],
        }
    )
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
