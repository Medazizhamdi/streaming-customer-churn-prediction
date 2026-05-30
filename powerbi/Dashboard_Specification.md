# Spécification du Dashboard Power BI

## Source de Données

Utiliser `outputs/powerbi_streaming_churn_dataset.csv`.

## Page 1: Vue Exécutive

Objectif: donner à la Direction et au Marketing une vision synthétique du churn et du risque business.

Visuels:

- Carte KPI: taux de churn réel.
- Carte KPI: taux de churn prédit.
- Carte KPI: nombre de clients à haut risque.
- Carte KPI: revenu mensuel à risque.
- Courbe: tendance par bucket d’ancienneté.
- Bar chart: churn par `subscription_plan`.
- Bar chart: clients à haut risque par `streaming_quality`.
- Slicer: plan d’abonnement.
- Slicer: niveau de risque.

## Page 2: Clients à Haut Risque

Objectif: aider les équipes CRM et Rétention à prioriser les actions.

Visuels:

- Table client avec `customer_id`, `churn_probability`, `risk_level`, `subscription_plan`, `monthly_subscription_fee`, `subscription_months`, `views_per_week` et `favorite_genre`.
- Bar chart Top N clients à risque.
- Scatter plot: prix mensuel vs score d’engagement, coloré par niveau de risque.
- Slicer: niveau de risque.
- Slicer: genre préféré.
- Slicer: qualité de streaming.

## Page 3: Profil Client

Objectif: faciliter une action de rétention personnalisée.

Visuels:

- Sélecteur de client.
- Carte KPI: probabilité de churn.
- Carte KPI: prix mensuel.
- Carte KPI: ancienneté.
- Carte KPI: score d’engagement.
- Table de détails: plan, qualité, méthode de paiement, téléchargements offline, support premium et nombre d’appareils.
- Zone de recommandation de rétention.

## Mesures DAX

```DAX
Total Customers = DISTINCTCOUNT(streaming_churn[customer_id])

Actual Churners =
CALCULATE(
    DISTINCTCOUNT(streaming_churn[customer_id]),
    streaming_churn[churn] = 1
)

Overall Churn Rate =
DIVIDE([Actual Churners], [Total Customers])

Predicted Churners =
CALCULATE(
    DISTINCTCOUNT(streaming_churn[customer_id]),
    streaming_churn[predicted_class] = 1
)

Predicted Churn Rate =
DIVIDE([Predicted Churners], [Total Customers])

Clients Haut Risque =
CALCULATE(
    DISTINCTCOUNT(streaming_churn[customer_id]),
    streaming_churn[risk_level] = "High"
)

Revenue At Risk =
CALCULATE(
    SUM(streaming_churn[monthly_subscription_fee]),
    streaming_churn[risk_level] = "High"
)

Average Churn Probability =
AVERAGE(streaming_churn[churn_probability])

Average Monthly Fee =
AVERAGE(streaming_churn[monthly_subscription_fee])
```

## Logique de Recommandation

| Profil Client | Action Recommandée |
|---|---|
| Haut risque, plan mensuel, faible ancienneté | Offre d’onboarding ou réduction sur plan annuel |
| Haut risque, faible engagement | Recommandations de contenu personnalisées |
| Haut risque, prix élevé | Bundle de valeur ou remise fidélité temporaire |
| Haut risque, pas de téléchargements offline | Éducation sur la fonctionnalité offline |
| Haut risque, absence de support premium | Contact prioritaire par l’équipe CRM |
