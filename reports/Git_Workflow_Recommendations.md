# Recommandations de Workflow Git

## Stratégie de Branches

- `main`: branche stable pour la soumission finale.
- `feature/business-docs`: charte projet, CRISP-DM, Jira et README.
- `feature/eda`: notebook EDA et rapport d’analyse exploratoire.
- `feature/preprocessing`: nettoyage et pipeline de préparation.
- `feature/modeling`: entraînement, tuning et métriques.
- `feature/explainability`: importance des variables et SHAP.
- `feature/powerbi`: spécification dashboard, DAX et guide utilisateur.

## Workflow Recommandé

1. Créer une branche `feature/*` depuis `main`.
2. Réaliser une modification cohérente et limitée.
3. Exécuter les scripts ou notebooks concernés.
4. Créer un commit descriptif.
5. Fusionner via pull request.
6. Taguer la version finale de soumission.

## 20 Messages de Commit Réalistes

1. Initialiser la structure du projet de churn streaming
2. Ajouter le dataset IBM Telco dans le dossier raw
3. Adapter les variables télécom au contexte streaming
4. Ajouter des variables comportementales simulées
5. Implémenter le pipeline de preprocessing réutilisable
6. Ajouter le split stratifié et SMOTE sur l’entraînement
7. Ajouter le modèle baseline de régression logistique
8. Ajouter Random Forest avec GridSearchCV
9. Ajouter XGBoost avec validation croisée
10. Exporter les métriques de comparaison des modèles
11. Ajouter les courbes ROC et précision-rappel
12. Ajouter l’analyse d’optimisation du seuil
13. Exporter le fichier des clients à risque
14. Ajouter l’importance des variables
15. Ajouter l’analyse SHAP pour XGBoost
16. Rédiger le rapport CRISP-DM
17. Ajouter la spécification Power BI et les mesures DAX
18. Ajouter le backlog produit et la planification des sprints
19. Ajouter le script de présentation Marketing
20. Finaliser le README et la documentation de soumission
