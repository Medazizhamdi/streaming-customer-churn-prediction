# Prédiction du Churn Client pour une Plateforme de Streaming Vidéo

Ce dépôt contient un projet Data Science complet basé sur le jeu de données IBM Telco Customer Churn, adapté à un contexte de plateforme de streaming vidéo similaire à Netflix, Shahid, Disney+ ou Prime Video.

## Objectif Métier

L’entreprise observe qu’environ 26% des abonnés annulent leur abonnement après le premier trimestre. L’objectif est de prédire les clients à fort risque de churn avant leur départ afin que les équipes Marketing, CRM et Rétention puissent lancer des campagnes ciblées.

Objectif business: réduire le taux de churn de 10% en 6 mois.

## Méthodologie

Le projet suit exactement la méthodologie CRISP-DM:

1. Compréhension métier
2. Compréhension des données
3. Préparation des données
4. Modélisation
5. Évaluation
6. Déploiement

## Structure du Projet

```text
streaming-churn-prediction/
data/
  raw/
  processed/
notebooks/
  01_EDA.ipynb
  02_Data_Preparation.ipynb
  03_Modeling.ipynb
src/
  preprocessing.py
  feature_engineering.py
  train.py
  evaluate.py
  predict.py
outputs/
  predictions_churn.csv
  model_metrics.csv
reports/
  Project_Charter.md
  EDA_Report.md
  CRISP_DM_Report.md
  Presentation_Script.md
powerbi/
  Dashboard_Specification.md
  PowerBI_User_Guide.md
jira/
  Product_Backlog.md
  Sprint_1.md
  Sprint_2.md
  Sprint_3.md
  Burndown_Data.csv
models/
  best_model.pkl
```

## Adaptation du Dataset

| Champ IBM Telco | Champ Plateforme Streaming |
|---|---|
| `tenure` | `subscription_months` |
| `MonthlyCharges` | `monthly_subscription_fee` |
| `TotalCharges` | `total_spent` |
| `InternetService` | `streaming_quality` |
| `MultipleLines` | `shared_profiles` |
| `OnlineBackup` | `offline_downloads` |
| `Contract` | `subscription_plan` |
| `Churn` | `churn` |

Fonctionnalités comportementales simulées:

- `views_per_week`
- `favorite_genre`
- `average_watch_time`
- `number_of_devices`
- `engagement_score`

## Modélisation

Trois modèles sont entraînés et comparés:

- Régression Logistique
- Random Forest
- XGBoost

Chaque modèle utilise GridSearchCV avec validation croisée à 5 plis. Le pipeline de préparation inclut l’imputation par médiane, le One-Hot Encoding, la standardisation et SMOTE appliqué uniquement sur les données d’entraînement.

## Résultats

Le meilleur modèle généré est Random Forest avec un AUC-ROC de test de 0.8413, supérieur au critère de succès fixé à 0.80. Le seuil optimisé est 0.40 afin d’améliorer la détection des churners dans un contexte de rétention.

## Exécution

Installer les dépendances:

```powershell
pip install -r requirements.txt
```

Entraîner les modèles et générer les sorties:

```powershell
python src/train.py
```

Lancer une prédiction batch:

```powershell
python src/predict.py --input data/raw/IBM_Telco_Customer_Churn.csv --output outputs/predictions_churn.csv
```

## Sorties Principales

- `outputs/model_metrics.csv`: comparaison des modèles.
- `outputs/predictions_churn.csv`: liste des clients avec risque de churn.
- `outputs/powerbi_streaming_churn_dataset.csv`: dataset prêt pour Power BI.
- `outputs/feature_importance.csv`: principaux facteurs de churn.
- `outputs/shap_feature_impact.csv`: impact SHAP pour XGBoost.
- `models/best_model.pkl`: meilleur modèle entraîné.

## Power BI

Le tableau de bord contient trois pages:

- Vue Exécutive
- Clients à Haut Risque
- Profil Client

Les mesures DAX, la spécification du dashboard et le guide utilisateur d’une page sont disponibles dans le dossier `powerbi/`.

## Livrables Académiques

Le dépôt inclut la charte projet, le rapport EDA, le rapport CRISP-DM complet, le backlog Jira, la planification des sprints, les données de burndown, les recommandations Git et un script de présentation final pour l’équipe Marketing.
