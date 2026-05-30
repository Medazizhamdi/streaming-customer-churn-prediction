"""Reusable preprocessing pipeline for streaming churn modeling."""

from __future__ import annotations

from typing import List, Tuple

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


TARGET = "churn"
ID_COLUMN = "customer_id"


def split_features_target(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Separate model features from target and customer identifier."""
    X = df.drop(columns=[TARGET, ID_COLUMN], errors="ignore")
    y = df[TARGET]
    return X, y


def get_feature_types(X: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """Return numeric and categorical feature lists."""
    numeric_features = X.select_dtypes(include=["int64", "float64", "int32", "float32"]).columns.tolist()
    categorical_features = [col for col in X.columns if col not in numeric_features]
    return numeric_features, categorical_features


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """Create a preprocessing transformer with imputation, scaling, and one-hot encoding."""
    numeric_features, categorical_features = get_feature_types(X)

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric_features),
            ("categorical", categorical_pipeline, categorical_features),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )


def get_feature_names(preprocessor: ColumnTransformer) -> list[str]:
    """Extract transformed feature names for explainability outputs."""
    return preprocessor.get_feature_names_out().tolist()
