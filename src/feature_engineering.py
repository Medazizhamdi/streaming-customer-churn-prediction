"""Feature engineering for the streaming-platform churn project."""

from __future__ import annotations

import hashlib
from typing import Iterable

import numpy as np
import pandas as pd


STREAMING_RENAME_MAP = {
    "customerID": "customer_id",
    "tenure": "subscription_months",
    "MonthlyCharges": "monthly_subscription_fee",
    "TotalCharges": "total_spent",
    "InternetService": "streaming_quality",
    "MultipleLines": "shared_profiles",
    "OnlineBackup": "offline_downloads",
    "OnlineSecurity": "account_security",
    "DeviceProtection": "device_protection",
    "TechSupport": "premium_support",
    "StreamingTV": "live_tv_package",
    "StreamingMovies": "movie_package",
    "Contract": "subscription_plan",
    "PaperlessBilling": "digital_billing",
    "PaymentMethod": "payment_method",
    "Churn": "churn",
    "PhoneService": "mobile_access",
    "SeniorCitizen": "senior_subscriber",
    "Partner": "family_account",
    "Dependents": "kids_profile",
}

QUALITY_MAP = {
    "DSL": "Standard HD",
    "Fiber optic": "Ultra HD",
    "No": "Mobile only",
}

PLAN_MAP = {
    "Month-to-month": "Monthly",
    "One year": "Annual",
    "Two year": "Two-Year",
}

PROFILE_MAP = {
    "Yes": "Multiple",
    "No": "Single",
    "No phone service": "Single",
}

GENRES = ["Drama", "Comedy", "Sports", "Kids", "Documentary", "Action", "Reality"]


def _stable_index(value: str, modulo: int) -> int:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % modulo


def _stable_uniform(value: str, low: float, high: float) -> float:
    idx = _stable_index(value, 10_000)
    return low + (high - low) * (idx / 9_999)


def adapt_telco_to_streaming(df: pd.DataFrame) -> pd.DataFrame:
    """Rename telecom columns and values into a streaming subscription context."""
    data = df.rename(columns=STREAMING_RENAME_MAP).copy()

    data["total_spent"] = pd.to_numeric(data["total_spent"], errors="coerce")
    data["streaming_quality"] = data["streaming_quality"].map(QUALITY_MAP).fillna(data["streaming_quality"])
    data["subscription_plan"] = data["subscription_plan"].map(PLAN_MAP).fillna(data["subscription_plan"])
    data["shared_profiles"] = data["shared_profiles"].map(PROFILE_MAP).fillna(data["shared_profiles"])
    data["churn"] = data["churn"].map({"Yes": 1, "No": 0}).astype(int)

    yes_no_cols: Iterable[str] = [
        "family_account",
        "kids_profile",
        "mobile_access",
        "offline_downloads",
        "account_security",
        "device_protection",
        "premium_support",
        "live_tv_package",
        "movie_package",
        "digital_billing",
    ]
    for col in yes_no_cols:
        if col in data.columns:
            data[col] = data[col].replace({"No internet service": "No", "No phone service": "No"})

    return data


def add_behavioral_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create deterministic simulated behavioral features for academic reproducibility."""
    data = df.copy()
    ids = data["customer_id"].astype(str)

    tenure_factor = np.log1p(data["subscription_months"].clip(lower=0))
    fee_factor = data["monthly_subscription_fee"].fillna(data["monthly_subscription_fee"].median()) / 100

    data["views_per_week"] = [
        round(max(1, _stable_uniform(customer_id, 2, 28) + tenure_factor.iloc[i] - fee_factor.iloc[i]), 1)
        for i, customer_id in enumerate(ids)
    ]
    data["average_watch_time"] = [
        round(max(0.3, _stable_uniform(customer_id + "watch", 0.5, 4.2) + 0.04 * data["views_per_week"].iloc[i]), 2)
        for i, customer_id in enumerate(ids)
    ]
    data["number_of_devices"] = [
        int(np.clip(1 + _stable_index(customer_id + "devices", 5), 1, 5))
        for customer_id in ids
    ]
    data["favorite_genre"] = [
        GENRES[_stable_index(customer_id + "genre", len(GENRES))]
        for customer_id in ids
    ]

    data["engagement_score"] = (
        data["views_per_week"] * data["average_watch_time"] / data["number_of_devices"]
    ).round(2)
    data["subscription_value_ratio"] = (
        data["total_spent"].fillna(data["total_spent"].median())
        / data["monthly_subscription_fee"].replace(0, np.nan)
    ).fillna(0).round(2)
    return data


def load_streaming_dataset(path: str) -> pd.DataFrame:
    """Load IBM Telco churn data and transform it into a streaming-platform dataset."""
    raw = pd.read_csv(path)
    return add_behavioral_features(adapt_telco_to_streaming(raw))
