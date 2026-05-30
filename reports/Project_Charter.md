# Charte Projet: Prédiction du Churn Client pour une Plateforme de Streaming Vidéo

## Vue d’Ensemble

Ce projet transforme le dataset IBM Telco Customer Churn en un contexte de plateforme de streaming vidéo similaire à Netflix, Shahid, Disney+ ou Prime Video. L’entreprise observe qu’environ 26% des abonnés annulent leur abonnement après le premier trimestre. Le projet vise à prédire les clients à fort risque de churn avant leur départ afin de permettre aux équipes Marketing, CRM et Rétention de lancer des campagnes ciblées.

## Objectif Métier

Réduire le taux de churn de 10% dans les 6 prochains mois grâce à l’identification proactive des abonnés à risque.

## Critères de Succès

- AUC-ROC supérieur à 0.80 sur le jeu de test.
- Méthodologie CRISP-DM complète.
- Code réutilisable pour la préparation, l’entraînement, l’évaluation et la prédiction.
- Spécification Power BI destinée aux utilisateurs métier.
- Fichier `predictions_churn.csv` contenant les scores et niveaux de risque.
- Documentation prête pour une soumission universitaire.

## Périmètre

Inclus:

- Adaptation du contexte télécom vers un contexte streaming.
- Analyse exploratoire des données.
- Préparation des données et feature engineering.
- Comparaison de trois modèles: Régression Logistique, Random Forest et XGBoost.
- Interprétabilité avec importance des variables et SHAP.
- Export des prédictions et documentation Power BI.

Exclu:

- Intégration réelle avec un CRM.
- Données comportementales réelles de visionnage.
- Automatisation des campagnes marketing.
- Revue juridique des messages de rétention.

## Analyse des Parties Prenantes

| Partie prenante | Intérêt | Besoin de décision | Livrable associé |
|---|---|---|---|
| Directeur Marketing | Réduire le churn et protéger le revenu | Quels segments cibler? | Dashboard exécutif et recommandations |
| Équipe CRM | Prioriser les actions opérationnelles | Quels clients contacter en premier? | Liste des clients à haut risque |
| Équipe Rétention | Améliorer le taux de sauvegarde | Quelle action proposer? | Profil client et facteurs de risque |
| Direction Générale | Suivre la performance et le ROI | Le projet est-il fiable et utile? | KPIs, métriques modèle, synthèse business |

## Contraintes

- Ressources limitées.
- Délai de 7 semaines.
- Données clients existantes uniquement.
- Dataset d’origine télécom adapté à un scénario streaming.

## Risques

- Les variables comportementales simulées ne remplacent pas de vraies données de visionnage.
- Le dataset ne contient pas les promotions concurrentes, la satisfaction client ou l’historique des campagnes.
- Une forte précision peut masquer des churners non détectés; l’analyse des faux négatifs est donc essentielle.

## Planning Synthétique

| Semaine | Focus |
|---|---|
| 1-2 | Compréhension métier et EDA |
| 3-4 | Préparation des données et modélisation |
| 5 | Évaluation, seuil optimal et explicabilité |
| 6 | Spécification Power BI et exports |
| 7 | Documentation finale et présentation |
