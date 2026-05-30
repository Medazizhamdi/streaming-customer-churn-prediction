"""Génère les notebooks académiques annotés en français."""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"


def write_notebook(filename: str, cells: list) -> None:
    nb = nbf.v4.new_notebook()
    nb["cells"] = cells
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
    }
    nbf.write(nb, NOTEBOOKS / filename)


def md(text: str):
    return nbf.v4.new_markdown_cell(text)


def code(text: str):
    return nbf.v4.new_code_cell(text)


def main() -> None:
    NOTEBOOKS.mkdir(parents=True, exist_ok=True)

    write_notebook(
        "01_EDA.ipynb",
        [
            md("# 01 - Analyse Exploratoire des Données\n\nCe notebook couvre la phase **Compréhension des données** de CRISP-DM. Il est volontairement très annoté afin de montrer clairement les étapes attendues pour l’évaluation académique."),
            code("import sys\nfrom pathlib import Path\n\nROOT = Path.cwd().parents[0] if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.append(str(ROOT / 'src'))\n\nimport pandas as pd\nimport seaborn as sns\nimport matplotlib.pyplot as plt\n\nfrom feature_engineering import load_streaming_dataset"),
            md("## Chargement et Adaptation du Dataset\n\nLe dataset IBM Telco est chargé depuis `data/raw`, puis adapté au contexte d’une plateforme de streaming vidéo. Les variables télécom sont renommées en variables métier streaming."),
            code("df = load_streaming_dataset(ROOT / 'data' / 'raw' / 'IBM_Telco_Customer_Churn.csv')\ndf.head()"),
            md("## Vue d’Ensemble du Dataset\n\nCette section vérifie le nombre de lignes, le nombre de colonnes, les types de données et les premières observations."),
            code("print(f'Lignes: {df.shape[0]:,}')\nprint(f'Colonnes: {df.shape[1]:,}')\ndf.info()"),
            md("## Analyse des Valeurs Manquantes\n\nLa variable `TotalCharges`, renommée `total_spent`, contient des valeurs vides dans le dataset original. Elles sont converties en valeurs manquantes numériques."),
            code("missing = df.isna().sum().sort_values(ascending=False)\nmissing[missing > 0]"),
            md("## Vérification des Doublons\n\n`customer_id` doit être unique. Des doublons pourraient fausser les indicateurs et l’apprentissage."),
            code("df['customer_id'].duplicated().sum()"),
            md("## Statistiques Descriptives\n\nLes statistiques descriptives permettent d’analyser les distributions, les valeurs extrêmes et la dispersion des variables numériques."),
            code("df.describe().T"),
            md("## Distribution de la Variable Cible\n\nLe churn est une classe minoritaire. Cette observation justifie le split stratifié et l’utilisation de SMOTE uniquement sur l’entraînement."),
            code("target_dist = df['churn'].value_counts(normalize=True).rename('pourcentage') * 100\nprint(target_dist)\nsns.countplot(data=df, x='churn')\nplt.title('Distribution du churn')\nplt.show()"),
            md("## Heatmap de Corrélation\n\nLa heatmap permet d’observer les relations entre les variables numériques, notamment l’ancienneté, le prix, les dépenses et l’engagement."),
            code("numeric_cols = df.select_dtypes(include='number').columns\nplt.figure(figsize=(10, 7))\nsns.heatmap(df[numeric_cols].corr(), cmap='coolwarm', center=0)\nplt.title('Heatmap de corrélation')\nplt.show()"),
            md("## Histogrammes\n\nLes histogrammes montrent la forme des distributions pour l’ancienneté, le prix, les dépenses et les variables de comportement."),
            code("df[['subscription_months', 'monthly_subscription_fee', 'total_spent', 'views_per_week', 'average_watch_time']].hist(figsize=(12, 8), bins=30)\nplt.tight_layout()\nplt.show()"),
            md("## Boxplots par Churn\n\nLes boxplots comparent les churners et non-churners sur les variables numériques importantes."),
            code("for col in ['subscription_months', 'monthly_subscription_fee', 'total_spent', 'engagement_score']:\n    plt.figure(figsize=(7, 4))\n    sns.boxplot(data=df, x='churn', y=col)\n    plt.title(f'{col} selon le churn')\n    plt.show()"),
            md("## Analyse du Churn par Catégorie\n\nCes graphiques relient le churn à des dimensions exploitables par les équipes Marketing et CRM."),
            code("for col in ['subscription_plan', 'streaming_quality', 'payment_method', 'offline_downloads', 'premium_support', 'favorite_genre']:\n    rates = df.groupby(col)['churn'].mean().sort_values(ascending=False).reset_index()\n    plt.figure(figsize=(9, 4))\n    sns.barplot(data=rates, x='churn', y=col, color='#2f6f9f')\n    plt.title(f'Taux de churn par {col}')\n    plt.xlabel('Taux de churn')\n    plt.ylabel(col)\n    plt.show()"),
            md("## Conclusion EDA\n\nLes signaux attendus sont l’ancienneté faible, le plan mensuel, la méthode de paiement, le prix mensuel et l’engagement. Ces résultats orientent la préparation des données et la modélisation."),
        ],
    )

    write_notebook(
        "02_Data_Preparation.ipynb",
        [
            md("# 02 - Préparation des Données\n\nCe notebook couvre la phase **Préparation des données** de CRISP-DM: imputation, encodage, standardisation, traitement du déséquilibre et split stratifié."),
            code("import sys\nfrom pathlib import Path\n\nROOT = Path.cwd().parents[0] if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.append(str(ROOT / 'src'))\n\nimport pandas as pd\nfrom sklearn.model_selection import train_test_split\nfrom imblearn.over_sampling import SMOTE\n\nfrom feature_engineering import load_streaming_dataset\nfrom preprocessing import build_preprocessor, split_features_target, get_feature_types"),
            md("## Chargement du Dataset Streaming\n\nLe module de feature engineering applique le renommage métier et ajoute des variables comportementales simulées."),
            code("df = load_streaming_dataset(ROOT / 'data' / 'raw' / 'IBM_Telco_Customer_Churn.csv')\nX, y = split_features_target(df)\nX.head()"),
            md("## Identification des Types de Variables\n\nLes variables numériques reçoivent imputation médiane et standardisation. Les variables catégorielles reçoivent imputation par modalité la plus fréquente et One-Hot Encoding."),
            code("numeric_features, categorical_features = get_feature_types(X)\nprint('Numériques:', numeric_features)\nprint('Catégorielles:', categorical_features)"),
            md("## Split Train/Test Stratifié 80/20\n\nLa stratification conserve la proportion de churners dans le train et le test."),
            code("X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)\nprint(y_train.mean(), y_test.mean())"),
            md("## Pipeline de Preprocessing Réutilisable\n\nLe pipeline évite la fuite de données: il apprend les transformations sur le train puis les applique au test."),
            code("preprocessor = build_preprocessor(X_train)\nX_train_prepared = preprocessor.fit_transform(X_train)\nX_test_prepared = preprocessor.transform(X_test)\nprint(X_train_prepared.shape, X_test_prepared.shape)"),
            md("## SMOTE sur les Données d’Entraînement Uniquement\n\nSMOTE est appliqué après le split et uniquement au train. Le test reste inchangé afin de simuler de vrais nouveaux clients."),
            code("smote = SMOTE(random_state=42)\nX_train_balanced, y_train_balanced = smote.fit_resample(X_train_prepared, y_train)\nprint('Avant SMOTE:', y_train.value_counts().to_dict())\nprint('Après SMOTE:', pd.Series(y_train_balanced).value_counts().to_dict())"),
            md("## Export du Dataset Préparé\n\nLe script d’entraînement exporte également le dataset adapté dans `data/processed/streaming_churn_processed.csv` pour audit et reproductibilité."),
            code("processed_path = ROOT / 'data' / 'processed' / 'streaming_churn_processed.csv'\ndf.to_csv(processed_path, index=False)\nprocessed_path"),
            md("## Conclusion\n\nCette phase produit un pipeline réutilisable et compatible avec la validation croisée, l’entraînement et le scoring batch."),
        ],
    )

    write_notebook(
        "03_Modeling.ipynb",
        [
            md("# 03 - Modélisation, Évaluation et Explicabilité\n\nCe notebook couvre les phases **Modélisation** et **Évaluation** de CRISP-DM. Le script exécutable principal est `src/train.py`; le notebook explique comment inspecter les sorties."),
            code("import sys\nfrom pathlib import Path\n\nROOT = Path.cwd().parents[0] if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.append(str(ROOT / 'src'))\n\nimport json\nimport pandas as pd\nfrom IPython.display import display, Image"),
            md("## Entraînement des Modèles\n\nLe script entraîne Régression Logistique, Random Forest et XGBoost avec GridSearchCV et validation croisée à 5 plis.\n\n```powershell\npython src/train.py\n```"),
            code("# Dans un environnement notebook local, décommenter pour entraîner depuis le notebook.\n# import subprocess\n# subprocess.run([sys.executable, str(ROOT / 'src' / 'train.py')], check=True)"),
            md("## Tableau de Comparaison\n\nLe fichier `outputs/model_metrics.csv` contient AUC-ROC, F1-score, précision, rappel et meilleurs hyperparamètres."),
            code("metrics_path = ROOT / 'outputs' / 'model_metrics.csv'\nif metrics_path.exists():\n    metrics = pd.read_csv(metrics_path)\n    display(metrics)\nelse:\n    print('Exécuter src/train.py pour générer model_metrics.csv')"),
            md("## Rapports de Classification\n\nLes rapports détaillent précision, rappel, F1-score et support. Le rappel est particulièrement important car les faux négatifs sont des churners manqués."),
            code("reports_path = ROOT / 'outputs' / 'classification_reports.json'\nif reports_path.exists():\n    reports = json.loads(reports_path.read_text())\n    print(json.dumps(reports[0]['classification_report'], indent=2)[:3000])\nelse:\n    print('Exécuter src/train.py pour générer les rapports')"),
            md("## Courbes et Matrices de Confusion\n\nLes courbes ROC, précision-rappel et matrices de confusion sont générées dans `reports/figures`."),
            code("fig_dir = ROOT / 'reports' / 'figures'\nif fig_dir.exists():\n    for path in sorted(fig_dir.glob('*roc_curve.png')):\n        display(Image(filename=str(path)))\nelse:\n    print('Exécuter src/train.py pour générer les figures')"),
            md("## Optimisation du Seuil\n\nLe seuil 0.50 n’est pas forcément optimal. Le fichier `threshold_optimization.csv` compare plusieurs seuils et permet d’équilibrer rappel, précision et faux négatifs."),
            code("threshold_path = ROOT / 'outputs' / 'threshold_optimization.csv'\nif threshold_path.exists():\n    display(pd.read_csv(threshold_path).head(10))\nelse:\n    print('Exécuter src/train.py pour générer threshold_optimization.csv')"),
            md("## Importance des Variables et SHAP\n\nL’importance des variables identifie les drivers de churn. SHAP permet d’expliquer l’impact des variables pour XGBoost."),
            code("importance_path = ROOT / 'outputs' / 'feature_importance.csv'\nif importance_path.exists():\n    display(pd.read_csv(importance_path).head(20))\n\nshap_path = ROOT / 'outputs' / 'shap_feature_impact.csv'\nif shap_path.exists():\n    display(pd.read_csv(shap_path).head(20))"),
            md("## Sortie de Déploiement\n\nLe fichier `outputs/predictions_churn.csv` contient `customer_id`, `churn_probability`, `predicted_class` et `risk_level`. Il peut être utilisé par le CRM."),
            code("pred_path = ROOT / 'outputs' / 'predictions_churn.csv'\nif pred_path.exists():\n    display(pd.read_csv(pred_path).head(20))\nelse:\n    print('Exécuter src/train.py pour générer les prédictions')"),
            md("## Conclusion\n\nLe meilleur modèle est sélectionné selon l’AUC-ROC et la pertinence métier. L’analyse des faux négatifs et le choix du seuil doivent être alignés avec la capacité de campagne."),
        ],
    )


if __name__ == "__main__":
    main()
