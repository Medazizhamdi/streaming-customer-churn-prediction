# Script de Présentation Finale: Démonstration à l’Équipe Marketing

## Durée: 5 à 10 Minutes

### 1. Introduction

Bonjour à tous. Aujourd’hui, je vais présenter notre projet de prédiction du churn client pour une plateforme de streaming vidéo. Le problème métier est clair: environ 26% des abonnés annulent leur abonnement après le premier trimestre. Notre objectif est d’identifier les clients susceptibles de churner avant leur départ afin de permettre aux équipes Marketing et CRM d’agir plus tôt.

### 2. Contexte Métier

Dans une plateforme de streaming, un client peut résilier parce qu’il ne regarde pas assez de contenu, trouve le prix trop élevé, reste sur un plan mensuel flexible ou ne perçoit pas assez de valeur. Au lieu d’attendre l’annulation, nous proposons un modèle prédictif qui attribue à chaque client une probabilité de churn et un niveau de risque: Low, Medium ou High.

### 3. Données et Adaptation

La source est le dataset IBM Telco Customer Churn. Pour l’adapter à notre cas streaming, nous avons renommé les variables télécom. Par exemple, `tenure` devient `subscription_months`, `MonthlyCharges` devient `monthly_subscription_fee`, `Contract` devient `subscription_plan` et `InternetService` devient `streaming_quality`.

Nous avons aussi simulé des variables comportementales comme le nombre de vues par semaine, le genre préféré, le temps moyen de visionnage et le nombre d’appareils. Ces variables rendent le projet plus réaliste pour une plateforme de streaming.

### 4. Méthodologie

Le projet suit CRISP-DM: compréhension métier, compréhension des données, préparation des données, modélisation, évaluation et déploiement. Cette structure garantit une démarche complète, à la fois académique et proche d’un projet industriel.

### 5. Analyse Exploratoire

L’EDA couvre les types de données, les valeurs manquantes, les doublons, les statistiques descriptives, la distribution du churn, les corrélations, les heatmaps, les histogrammes, les boxplots et l’analyse du churn par catégorie.

Le dataset contient 7 043 clients, dont 1 869 churners, soit un taux de churn de 26.54%. Nous avons aussi identifié 11 valeurs manquantes dans `TotalCharges`.

### 6. Modélisation

Nous avons comparé trois modèles: Régression Logistique, Random Forest et XGBoost. Chaque modèle a été optimisé avec GridSearchCV et validation croisée à 5 plis. Le pipeline applique l’imputation, le One-Hot Encoding, la standardisation et SMOTE uniquement sur les données d’entraînement.

Le meilleur modèle est Random Forest avec un AUC-ROC de test de 0.8413, ce qui dépasse le critère de succès fixé à 0.80.

### 7. Explicabilité

Pour que les résultats soient compréhensibles par les équipes métier, nous avons généré l’importance des variables et une analyse SHAP pour XGBoost. Les facteurs importants incluent le plan mensuel, l’ancienneté, la méthode de paiement, la qualité de streaming, le prix mensuel et le support premium.

### 8. Dashboard Power BI

Le dashboard comporte trois pages.

La première page, Vue Exécutive, présente le taux de churn réel, le taux de churn prédit, le nombre de clients à haut risque, le revenu à risque et le churn par plan d’abonnement.

La deuxième page, Clients à Haut Risque, permet aux équipes CRM de trier les clients par probabilité de churn et de filtrer par niveau de risque, plan, qualité de streaming ou genre préféré.

La troisième page, Profil Client, affiche les détails d’un client, sa probabilité de churn, ses facteurs de risque et une recommandation de rétention.

### 9. Recommandations

Nous recommandons de prioriser les abonnés à haut risque, surtout ceux qui sont en plan mensuel et dans leurs premiers mois d’abonnement. Pour les clients sensibles au prix, une remise ou une migration vers un plan annuel peut être proposée. Pour les clients peu engagés, des recommandations de contenu personnalisées peuvent être utilisées.

### 10. Conclusion

Ce projet fournit un système complet: documentation CRISP-DM, notebooks annotés, code reproductible, modèles entraînés, fichier de prédictions, spécification Power BI, livrables Jira et recommandations métier. La prochaine étape serait d’intégrer de vraies données de visionnage et de tester les campagnes de rétention avec des expériences contrôlées.
