"""Evaluation helpers for threshold and business error analysis."""

from __future__ import annotations

import pandas as pd
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score


def threshold_optimization(y_true, probabilities) -> pd.DataFrame:
    rows = []
    for threshold in [x / 100 for x in range(20, 81, 5)]:
        y_pred = (probabilities >= threshold).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        rows.append(
            {
                "threshold": threshold,
                "f1": f1_score(y_true, y_pred),
                "precision": precision_score(y_true, y_pred, zero_division=0),
                "recall": recall_score(y_true, y_pred),
                "false_negatives": fn,
                "false_positives": fp,
                "missed_churners": fn,
                "captured_churners": tp,
            }
        )
    return pd.DataFrame(rows)


def missed_churner_analysis(customers: pd.DataFrame, y_true, probabilities, threshold: float) -> pd.DataFrame:
    analysis = customers.copy()
    analysis["actual_churn"] = y_true
    analysis["churn_probability"] = probabilities
    analysis["predicted_churn"] = (probabilities >= threshold).astype(int)
    return analysis[(analysis["actual_churn"] == 1) & (analysis["predicted_churn"] == 0)]
