# Livrables Jira - Version Prête pour PDF

## Vision Produit

Permettre aux équipes Marketing et CRM de réduire le churn des abonnés streaming grâce à l’identification précoce des clients à haut risque et à la priorisation des campagnes de rétention.

## Product Backlog

| ID | Récit utilisateur | MoSCoW | Points d’effort |
|---|---|---|---|
| US01 | En tant que Directeur Marketing, je veux voir le taux de churn global afin de suivre la santé business. | Must | 3 |
| US02 | En tant que spécialiste rétention, je veux visualiser les clients à haut risque afin de lancer des campagnes ciblées. | Must | 5 |
| US03 | En tant qu’analyste CRM, je veux une probabilité de churn par client afin de prioriser les actions. | Must | 5 |
| US04 | En tant que dirigeant, je veux un AUC-ROC supérieur à 0.80 afin de faire confiance au modèle. | Must | 8 |
| US05 | En tant que data scientist, je veux un pipeline de preprocessing réutilisable afin de rendre le projet reproductible. | Must | 5 |
| US06 | En tant que data scientist, je veux appliquer SMOTE uniquement sur le train afin d’éviter la fuite de données. | Must | 3 |
| US07 | En tant que Directeur Marketing, je veux analyser le churn par plan d’abonnement afin de concevoir des offres adaptées. | Must | 3 |
| US08 | En tant que manager CRM, je veux des niveaux de risque afin de faciliter la priorisation. | Must | 3 |
| US09 | En tant qu’agent de rétention, je veux consulter le profil client afin de personnaliser le contact. | Should | 5 |
| US10 | En tant que data scientist, je veux une analyse SHAP afin d’expliquer les prédictions XGBoost. | Should | 5 |
| US11 | En tant qu’analyste business, je veux des graphiques EDA afin de comprendre les tendances de churn. | Should | 3 |
| US12 | En tant qu’évaluateur académique, je veux une documentation CRISP-DM complète afin de noter la méthodologie. | Must | 5 |
| US13 | En tant que Product Owner, je veux des données de burndown afin de suivre l’avancement. | Could | 2 |
| US14 | En tant que développeur BI, je veux des mesures DAX afin de construire le dashboard plus rapidement. | Should | 3 |
| US15 | En tant qu’enseignant évaluateur, je veux des notebooks annotés afin de suivre l’analyse. | Must | 5 |

## Planification des Sprints

Sprint 1: compréhension métier et EDA.

Sprint 2: préparation des données et modélisation.

Sprint 3: évaluation, dashboard et documentation.

## Données de Burndown

Les données du burndown chart sont disponibles dans `jira/Burndown_Data.csv` et peuvent être importées dans Excel, Power BI ou Jira.

## Définition de Prêt

Une user story est prête lorsque le rôle utilisateur, l’objectif, la sortie attendue et les critères d’acceptation sont clairs.

## Définition de Terminé

Une user story est terminée lorsque le code ou la documentation est produit, les sorties sont générées et les critères d’acceptation sont satisfaits.
