# Rapport CRISP-DM: Prédiction du Churn pour une Plateforme de Streaming Vidéo

## Résumé Exécutif

Ce projet applique la méthodologie CRISP-DM pour construire une solution complète de prédiction du churn client pour une plateforme de streaming vidéo. Le contexte métier est adapté à partir du dataset IBM Telco Customer Churn et reformulé autour des abonnements, de la qualité de streaming, des options de contenu, de la facturation et de l’engagement.

L’entreprise observe qu’environ 26% des abonnés annulent leur abonnement après le premier trimestre. L’objectif est d’identifier les clients à haut risque avant leur départ afin que les équipes Marketing, CRM et Rétention puissent lancer des actions ciblées.

Le projet livre une documentation métier, une analyse exploratoire, un pipeline de preprocessing, trois modèles supervisés, une analyse d’explicabilité, une optimisation du seuil, des fichiers de déploiement, une spécification Power BI, des livrables Jira et un script de présentation.

## 1. Compréhension Métier

### 1.1 Problème Métier

Le churn réduit directement le revenu récurrent et augmente la pression sur l’acquisition de nouveaux clients. Pour une plateforme de streaming, le churn peut être causé par une faible consommation de contenu, une sensibilité au prix, un plan mensuel flexible, une mauvaise expérience de paiement ou un manque de support.

### 1.2 Objectif Métier

L’objectif principal est de réduire le taux de churn de 10% en 6 mois. Le projet soutient cet objectif en produisant une liste priorisée de clients à risque et en expliquant les facteurs qui influencent leur probabilité de churn.

### 1.3 Objectif Data Mining

Construire un modèle de classification binaire prédisant si un client va churner. La variable cible est `churn`, où 1 signifie que le client a résilié et 0 signifie qu’il est resté.

### 1.4 Critères de Succès

- AUC-ROC supérieur à 0.80 sur le jeu de test.
- Split train/test stratifié 80/20.
- SMOTE appliqué uniquement sur les données d’entraînement.
- Comparaison de Régression Logistique, Random Forest et XGBoost.
- Explicabilité avec importance des variables et SHAP.
- Export Power BI et fichier de prédictions.

### 1.5 Parties Prenantes

Le Directeur Marketing a besoin des facteurs de churn et des tendances par segment. L’équipe CRM a besoin d’une liste priorisée de clients à contacter. L’équipe Rétention a besoin de facteurs de risque et de recommandations personnalisées. La Direction Générale a besoin de métriques fiables et d’une lecture business des résultats.

### 1.6 Contraintes

Le projet est soumis à des ressources limitées, un délai de 7 semaines et l’utilisation de données clients existantes uniquement. Comme le dataset source est télécom, certaines variables comportementales streaming sont simulées pour rendre le cas plus réaliste.

## 2. Compréhension des Données

### 2.1 Source des Données

La source est le dataset IBM Telco Customer Churn. Il contient des informations client, des caractéristiques de compte, des services souscrits, des informations de facturation et le statut de churn.

### 2.2 Adaptation au Contexte Streaming

Les variables télécom sont renommées dans un langage streaming. Par exemple, `tenure` devient `subscription_months`, `MonthlyCharges` devient `monthly_subscription_fee`, `InternetService` devient `streaming_quality`, `MultipleLines` devient `shared_profiles` et `Contract` devient `subscription_plan`.

### 2.3 Variables Comportementales Simulées

Les plateformes de streaming utilisent généralement des signaux d’engagement. Des variables déterministes ont donc été ajoutées: `views_per_week`, `favorite_genre`, `average_watch_time` et `number_of_devices`. Elles sont générées à partir de `customer_id`, ce qui garantit la reproductibilité.

### 2.4 Valeurs Manquantes

Le problème principal concerne `TotalCharges`, renommé `total_spent`. Le dataset contient 11 valeurs vides, converties en valeurs numériques manquantes et traitées par imputation médiane dans le pipeline.

### 2.5 Distribution de la Cible

Le dataset contient 7 043 clients, dont 1 869 churners et 5 174 non-churners. Le taux de churn est de 26.54%, proche du contexte métier. Le churn est donc une classe minoritaire; l’évaluation ne peut pas se limiter à l’accuracy.

### 2.6 Analyse Exploratoire

L’EDA couvre la structure du dataset, les types de données, les valeurs manquantes, les doublons, les statistiques descriptives, la distribution du churn, les corrélations, les heatmaps, les histogrammes, les boxplots et le churn par catégorie.

### 2.7 Premiers Enseignements

Les facteurs attendus incluent une faible ancienneté, un plan mensuel, une méthode de paiement moins stable, un prix mensuel élevé, un faible engagement et l’absence de services de support ou d’options de valeur.

## 3. Préparation des Données

### 3.1 Nettoyage

Le fichier brut est chargé depuis `data/raw/IBM_Telco_Customer_Churn.csv`. Les valeurs vides de `TotalCharges` sont converties en `NaN`. Les modalités télécom sont standardisées dans un contexte streaming.

### 3.2 Feature Engineering

Le projet ajoute des variables d’engagement et des ratios dérivés. `engagement_score` combine les vues, le temps de visionnage et le nombre d’appareils. `subscription_value_ratio` estime la valeur cumulée du client par rapport à son prix mensuel.

### 3.3 Encodage et Standardisation

Les variables catégorielles sont encodées par One-Hot Encoding. Les variables numériques sont imputées par médiane puis standardisées avec `StandardScaler`. Ces étapes sont regroupées dans un `ColumnTransformer` réutilisable.

### 3.4 Traitement du Déséquilibre

SMOTE est utilisé pour traiter le déséquilibre de classe. Il est placé dans un pipeline imbalanced-learn après le preprocessing et avant le modèle. Comme le pipeline est utilisé dans la validation croisée, SMOTE est appliqué uniquement sur les plis d’entraînement.

### 3.5 Split Train/Test

Le dataset est divisé en 80% entraînement et 20% test avec stratification et `random_state=42`.

## 4. Modélisation

### 4.1 Modèles Candidats

Trois familles de modèles sont entraînées:

- Régression Logistique: baseline interprétable.
- Random Forest: modèle non linéaire robuste avec importance des variables.
- XGBoost: modèle de boosting performant sur données tabulaires.

### 4.2 Optimisation des Hyperparamètres

Chaque modèle est optimisé avec `GridSearchCV`, validation croisée à 5 plis et scoring AUC-ROC. Le pipeline contient preprocessing, SMOTE et estimateur.

### 4.3 Métriques

Les métriques exportées sont AUC-ROC, F1-score, précision, rappel, matrice de confusion, rapport de classification, courbe ROC et courbe précision-rappel.

### 4.4 Résultats des Modèles

| Modèle | CV AUC-ROC | Test AUC-ROC | F1 | Précision | Rappel |
|---|---:|---:|---:|---:|---:|
| Random Forest | 0.8457 | 0.8413 | 0.6114 | 0.5615 | 0.6711 |
| XGBoost | 0.8469 | 0.8378 | 0.6079 | 0.5984 | 0.6176 |
| Régression Logistique | 0.8432 | 0.8357 | 0.6229 | 0.5102 | 0.7995 |

Random Forest est retenu comme meilleur modèle car il obtient le meilleur AUC-ROC sur le test. La Régression Logistique présente un rappel plus élevé, intéressant pour une campagne large, mais avec une précision plus faible.

### 4.5 Explicabilité

Random Forest et XGBoost fournissent l’importance des variables. XGBoost est aussi analysé avec SHAP. Les facteurs importants incluent le plan mensuel, l’ancienneté, la méthode de paiement électronique, la qualité Ultra HD, le prix mensuel, le total dépensé et l’absence de support premium.

## 5. Évaluation

### 5.1 Sélection du Modèle

La sélection repose principalement sur l’AUC-ROC et la pertinence métier. Pour un cas de rétention, le rappel est important car un faux négatif représente un client qui churn mais qui n’est pas détecté.

### 5.2 Optimisation du Seuil

Le seuil par défaut de 0.50 n’est pas toujours optimal. Le projet teste des seuils de 0.20 à 0.80. Le meilleur seuil selon le F1-score est 0.40, avec F1 = 0.6347, précision = 0.5274 et rappel = 0.7968.

### 5.3 Analyse des Faux Négatifs

Les faux négatifs sont les churners manqués. Ils sont coûteux car l’entreprise ne déclenche aucune action de rétention. L’analyse doit examiner ces clients selon le plan d’abonnement, l’ancienneté, le prix mensuel et l’engagement.

### 5.4 Limites

Le dataset n’est pas un vrai dataset streaming. Les variables comportementales sont simulées. Le dataset ne contient pas les promotions concurrentes, la satisfaction client, la région, le canal d’acquisition, l’historique de campagne ou la profondeur réelle du catalogue.

### 5.5 Biais et Qualité des Données

Certaines variables démographiques doivent être utilisées avec prudence. Les offres de rétention doivent éviter tout traitement discriminatoire et être auditées avant un déploiement réel.

### 5.6 Recommandations Métier

Prioriser les clients à haut risque sur plan mensuel, surtout durant les 3 à 6 premiers mois. Proposer des incitations vers un plan annuel pour les clients sensibles au prix. Utiliser des recommandations de contenu pour les clients peu engagés. Combiner le risque de churn avec la valeur client pour optimiser l’usage des ressources CRM.

## 6. Déploiement

### 6.1 Fichier de Prédictions

Le fichier `outputs/predictions_churn.csv` contient:

- `customer_id`
- `churn_probability`
- `predicted_class`
- `risk_level`

Les niveaux de risque sont High pour une probabilité supérieure ou égale à 0.70, Medium entre 0.40 et 0.69, et Low sous 0.40.

### 6.2 Dataset Power BI

Le fichier `outputs/powerbi_streaming_churn_dataset.csv` est prêt pour la construction du dashboard Power BI.

### 6.3 Dashboard

Le dashboard comprend trois pages: Vue Exécutive, Clients à Haut Risque et Profil Client. Il permet le pilotage stratégique, la priorisation opérationnelle et l’aide à la décision individuelle.

### 6.4 Considérations Production

En production, le scoring devrait être planifié de façon hebdomadaire ou mensuelle. La performance du modèle doit être surveillée pour détecter le drift, surtout après des changements de prix, de catalogue ou de stratégie marketing.

## Conclusion

Ce projet fournit une solution complète et prête pour une soumission académique. Il suit CRISP-DM, adapte le dataset IBM à un contexte streaming, compare trois modèles, génère des sorties d’explicabilité, produit un fichier de prédictions et documente un dashboard Power BI destiné aux utilisateurs métier.
