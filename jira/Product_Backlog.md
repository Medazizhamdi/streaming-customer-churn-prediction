# Product Backlog

## Synthèse MoSCoW

| ID | Récit utilisateur | Priorité | Sprint |
|---|---|---|---|
| US01 | En tant que Directeur Marketing, je veux voir le taux de churn global afin de suivre la santé business. | Must | 1 |
| US02 | En tant que spécialiste rétention, je veux visualiser les clients à haut risque afin de lancer des campagnes ciblées. | Must | 3 |
| US03 | En tant qu’analyste CRM, je veux une probabilité de churn par client afin de prioriser les actions. | Must | 3 |
| US04 | En tant que dirigeant, je veux un AUC-ROC supérieur à 0.80 afin de faire confiance au modèle. | Must | 2 |
| US05 | En tant que data scientist, je veux un pipeline de preprocessing réutilisable afin de rendre le projet reproductible. | Must | 2 |
| US06 | En tant que data scientist, je veux appliquer SMOTE uniquement sur le train afin d’éviter la fuite de données. | Must | 2 |
| US07 | En tant que Directeur Marketing, je veux analyser le churn par plan d’abonnement afin de concevoir des offres adaptées. | Must | 1 |
| US08 | En tant que manager CRM, je veux des niveaux de risque afin de faciliter la priorisation. | Must | 3 |
| US09 | En tant qu’agent de rétention, je veux consulter le profil client afin de personnaliser le contact. | Should | 3 |
| US10 | En tant que data scientist, je veux une analyse SHAP afin d’expliquer les prédictions XGBoost. | Should | 2 |
| US11 | En tant qu’analyste business, je veux des graphiques EDA afin de comprendre les tendances de churn. | Should | 1 |
| US12 | En tant qu’évaluateur académique, je veux une documentation CRISP-DM complète afin de noter la méthodologie. | Must | 3 |
| US13 | En tant que Product Owner, je veux des données de burndown afin de suivre l’avancement. | Could | 3 |
| US14 | En tant que développeur BI, je veux des mesures DAX afin de construire le dashboard plus rapidement. | Should | 3 |
| US15 | En tant qu’enseignant évaluateur, je veux des notebooks annotés afin de suivre l’analyse. | Must | 3 |

## Définition de Terminé

- Le code exécute le flux complet depuis les données brutes jusqu’aux prédictions.
- Les sorties sont sauvegardées dans les dossiers demandés.
- La documentation suit CRISP-DM.
- La spécification Power BI inclut les pages, KPIs et mesures DAX.
- La comparaison des modèles inclut AUC-ROC, F1, précision, rappel, matrice de confusion et courbes.
