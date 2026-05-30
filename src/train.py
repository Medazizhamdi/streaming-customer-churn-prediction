"""Train, tune, evaluate, and export streaming churn models."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import shap
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    PrecisionRecallDisplay,
    RocCurveDisplay,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import GridSearchCV, train_test_split
from xgboost import XGBClassifier

from feature_engineering import load_streaming_dataset
from preprocessing import build_preprocessor, get_feature_names, split_features_target


ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = ROOT / "data" / "raw" / "IBM_Telco_Customer_Churn.csv"
PROCESSED_DATA = ROOT / "data" / "processed" / "streaming_churn_processed.csv"
OUTPUTS = ROOT / "outputs"
MODELS = ROOT / "models"
REPORTS = ROOT / "reports"


def ensure_directories() -> None:
    for path in [OUTPUTS, MODELS, REPORTS / "figures"]:
        path.mkdir(parents=True, exist_ok=True)


def risk_level(probability: float) -> str:
    if probability >= 0.70:
        return "High"
    if probability >= 0.40:
        return "Medium"
    return "Low"


def build_model_grid(X_train: pd.DataFrame) -> dict:
    preprocessor = build_preprocessor(X_train)
    return {
        "Logistic Regression": {
            "pipeline": ImbPipeline(
                steps=[
                    ("preprocessor", preprocessor),
                    ("smote", SMOTE(random_state=42)),
                    ("model", LogisticRegression(max_iter=3000, solver="liblinear", random_state=42)),
                ]
            ),
            "params": {
                "model__C": [0.5, 1.0, 2.0],
                "model__class_weight": [None, "balanced"],
            },
        },
        "Random Forest": {
            "pipeline": ImbPipeline(
                steps=[
                    ("preprocessor", build_preprocessor(X_train)),
                    ("smote", SMOTE(random_state=42)),
                    ("model", RandomForestClassifier(random_state=42, n_jobs=-1)),
                ]
            ),
            "params": {
                "model__n_estimators": [250],
                "model__max_depth": [6, 10, None],
                "model__min_samples_leaf": [2, 5],
            },
        },
        "XGBoost": {
            "pipeline": ImbPipeline(
                steps=[
                    ("preprocessor", build_preprocessor(X_train)),
                    ("smote", SMOTE(random_state=42)),
                    (
                        "model",
                        XGBClassifier(
                            objective="binary:logistic",
                            eval_metric="logloss",
                            random_state=42,
                            n_jobs=-1,
                        ),
                    ),
                ]
            ),
            "params": {
                "model__n_estimators": [150, 250],
                "model__max_depth": [2, 3],
                "model__learning_rate": [0.03, 0.08],
                "model__subsample": [0.85],
                "model__colsample_bytree": [0.85],
            },
        },
    }


def evaluate_model(name: str, estimator, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    probabilities = estimator.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    return {
        "model": name,
        "auc_roc": roc_auc_score(y_test, probabilities),
        "f1": f1_score(y_test, predictions),
        "precision": precision_score(y_test, predictions),
        "recall": recall_score(y_test, predictions),
        "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
        "classification_report": classification_report(y_test, predictions, output_dict=True),
    }


def save_curves(name: str, estimator, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    safe_name = name.lower().replace(" ", "_")
    fig, ax = plt.subplots(figsize=(7, 5))
    RocCurveDisplay.from_estimator(estimator, X_test, y_test, ax=ax)
    ax.set_title(f"{name} ROC Curve")
    fig.tight_layout()
    fig.savefig(REPORTS / "figures" / f"{safe_name}_roc_curve.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    PrecisionRecallDisplay.from_estimator(estimator, X_test, y_test, ax=ax)
    ax.set_title(f"{name} Precision-Recall Curve")
    fig.tight_layout()
    fig.savefig(REPORTS / "figures" / f"{safe_name}_precision_recall_curve.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(5, 4))
    ConfusionMatrixDisplay.from_estimator(estimator, X_test, y_test, ax=ax, cmap="Blues")
    ax.set_title(f"{name} Confusion Matrix")
    fig.tight_layout()
    fig.savefig(REPORTS / "figures" / f"{safe_name}_confusion_matrix.png", dpi=160)
    plt.close(fig)


def threshold_table(y_test: pd.Series, probabilities) -> pd.DataFrame:
    rows = []
    for threshold in [round(x, 2) for x in list(pd.Series(range(20, 81, 5)) / 100)]:
        preds = (probabilities >= threshold).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()
        rows.append(
            {
                "threshold": threshold,
                "f1": f1_score(y_test, preds),
                "precision": precision_score(y_test, preds, zero_division=0),
                "recall": recall_score(y_test, preds),
                "false_negatives": fn,
                "false_positives": fp,
                "true_positives": tp,
                "true_negatives": tn,
            }
        )
    return pd.DataFrame(rows).sort_values("f1", ascending=False)


def save_feature_importance(model_name: str, estimator, filename: str = "feature_importance.csv") -> None:
    preprocessor = estimator.named_steps["preprocessor"]
    model = estimator.named_steps["model"]
    feature_names = get_feature_names(preprocessor)

    if hasattr(model, "feature_importances_"):
        importance = pd.DataFrame(
            {"feature": feature_names, "importance": model.feature_importances_}
        ).sort_values("importance", ascending=False)
    elif hasattr(model, "coef_"):
        importance = pd.DataFrame(
            {"feature": feature_names, "importance": abs(model.coef_[0])}
        ).sort_values("importance", ascending=False)
    else:
        return

    importance.to_csv(OUTPUTS / filename, index=False)
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.barplot(data=importance.head(15), y="feature", x="importance", ax=ax, color="#2f6f9f")
    ax.set_title(f"{model_name} Top Feature Importance")
    fig.tight_layout()
    figure_name = filename.replace(".csv", ".png")
    fig.savefig(REPORTS / "figures" / figure_name, dpi=160)
    plt.close(fig)


def save_shap(best_estimator, X_test: pd.DataFrame) -> None:
    preprocessor = best_estimator.named_steps["preprocessor"]
    model = best_estimator.named_steps["model"]
    X_sample = X_test.sample(min(500, len(X_test)), random_state=42)
    X_transformed = preprocessor.transform(X_sample)
    feature_names = get_feature_names(preprocessor)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_transformed)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    shap.summary_plot(shap_values, X_transformed, feature_names=feature_names, show=False, max_display=20)
    plt.tight_layout()
    plt.savefig(REPORTS / "figures" / "shap_summary_plot.png", dpi=160, bbox_inches="tight")
    plt.close()

    impact = pd.DataFrame(
        {"feature": feature_names, "mean_abs_shap": abs(shap_values).mean(axis=0)}
    ).sort_values("mean_abs_shap", ascending=False)
    impact.to_csv(OUTPUTS / "shap_feature_impact.csv", index=False)


def main() -> None:
    ensure_directories()
    df = load_streaming_dataset(str(RAW_DATA))
    df.to_csv(PROCESSED_DATA, index=False)

    X, y = split_features_target(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    results = []
    estimators = {}
    for name, config in build_model_grid(X_train).items():
        search = GridSearchCV(
            config["pipeline"],
            config["params"],
            scoring="roc_auc",
            cv=5,
            n_jobs=-1,
            refit=True,
        )
        search.fit(X_train, y_train)
        estimator = search.best_estimator_
        estimators[name] = estimator
        metrics = evaluate_model(name, estimator, X_test, y_test)
        metrics["best_params"] = search.best_params_
        metrics["cv_auc_roc"] = search.best_score_
        results.append(metrics)
        save_curves(name, estimator, X_test, y_test)

    metrics_df = pd.DataFrame(
        [
            {
                "model": r["model"],
                "cv_auc_roc": r["cv_auc_roc"],
                "test_auc_roc": r["auc_roc"],
                "f1": r["f1"],
                "precision": r["precision"],
                "recall": r["recall"],
                "best_params": json.dumps(r["best_params"]),
            }
            for r in results
        ]
    ).sort_values("test_auc_roc", ascending=False)
    metrics_df.to_csv(OUTPUTS / "model_metrics.csv", index=False)

    best_name = metrics_df.iloc[0]["model"]
    best_estimator = estimators[best_name]
    joblib.dump(best_estimator, MODELS / "best_model.pkl")

    best_probabilities = best_estimator.predict_proba(X_test)[:, 1]
    thresholds = threshold_table(y_test, best_probabilities)
    thresholds.to_csv(OUTPUTS / "threshold_optimization.csv", index=False)
    best_threshold = float(thresholds.iloc[0]["threshold"])

    predictions = pd.DataFrame(
        {
            "customer_id": df.loc[X_test.index, "customer_id"],
            "churn_probability": best_probabilities.round(4),
            "predicted_class": (best_probabilities >= best_threshold).astype(int),
            "risk_level": [risk_level(p) for p in best_probabilities],
        }
    ).sort_values("churn_probability", ascending=False)
    predictions.to_csv(OUTPUTS / "predictions_churn.csv", index=False)

    full_probabilities = best_estimator.predict_proba(X)[:, 1]
    powerbi_export = df.copy()
    powerbi_export["churn_probability"] = full_probabilities.round(4)
    powerbi_export["predicted_class"] = (full_probabilities >= best_threshold).astype(int)
    powerbi_export["risk_level"] = [risk_level(p) for p in full_probabilities]
    powerbi_export.to_csv(OUTPUTS / "powerbi_streaming_churn_dataset.csv", index=False)

    save_feature_importance(best_name, best_estimator)
    if "Random Forest" in estimators:
        save_feature_importance("Random Forest", estimators["Random Forest"], "random_forest_feature_importance.csv")
    if "XGBoost" in estimators:
        save_feature_importance("XGBoost", estimators["XGBoost"], "xgboost_feature_importance.csv")
        save_shap(estimators["XGBoost"], X_test)

    with open(OUTPUTS / "classification_reports.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(metrics_df.to_string(index=False))
    print(f"Best model: {best_name}; optimized threshold: {best_threshold}")


if __name__ == "__main__":
    main()
