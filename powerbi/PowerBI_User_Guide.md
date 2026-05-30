# Guide Utilisateur Power BI - 1 Page

## Objectif du Dashboard

Ce dashboard aide les équipes Marketing, CRM et Rétention à suivre le churn, identifier les abonnés à haut risque et prioriser les actions de rétention.

## Page 1: Vue Exécutive

Cette page sert au pilotage global. Les KPIs principaux sont:

- Taux de churn réel: pourcentage historique des clients ayant résilié.
- Taux de churn prédit: pourcentage des clients prédits comme churners.
- Clients à haut risque: nombre de clients avec une probabilité de churn supérieure ou égale à 70%.
- Revenu à risque: revenu mensuel associé aux clients à haut risque.

Utiliser les filtres `subscription_plan` et `risk_level` pour comparer les segments.

## Page 2: Clients à Haut Risque

Cette page sert aux campagnes CRM. Trier la table par `churn_probability` du plus élevé au plus faible. Prioriser les clients High, puis les clients Medium si la capacité de campagne le permet.

Workflow recommandé:

1. Filtrer sur le niveau High.
2. Examiner le prix mensuel et l’ancienneté.
3. Sélectionner les clients à fort impact revenu.
4. Exporter la liste filtrée pour l’équipe CRM.

## Page 3: Profil Client

Cette page sert avant le contact individuel. Sélectionner un `customer_id` pour analyser la probabilité de churn, le plan, la qualité de streaming, l’engagement, les appareils, le genre préféré et les facteurs de risque.

Exemples d’actions:

- Plan mensuel et faible ancienneté: proposer une offre d’onboarding ou une réduction sur le plan annuel.
- Faible engagement: envoyer des recommandations de contenu personnalisées.
- Prix mensuel élevé: proposer un bundle de valeur ou une remise fidélité.
- Absence d’option offline: promouvoir les téléchargements hors ligne.

## Interprétation

Une probabilité de churn élevée ne signifie pas que le client va forcément résilier. Elle indique que son profil ressemble à celui de clients ayant déjà churné. Le dashboard doit aider la décision humaine, pas la remplacer.
