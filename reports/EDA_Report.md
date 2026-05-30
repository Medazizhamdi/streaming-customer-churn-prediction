# Rapport d’Analyse Exploratoire des Données

## Vue d’Ensemble du Dataset

Le projet utilise le dataset IBM Telco Customer Churn et l’adapte à un contexte de plateforme de streaming vidéo. Le fichier brut local contient 7 043 clients et 21 colonnes d’origine. Chaque ligne représente un abonné.

Exemples de renommage:

| Variable d’origine | Variable streaming |
|---|---|
| `tenure` | `subscription_months` |
| `MonthlyCharges` | `monthly_subscription_fee` |
| `TotalCharges` | `total_spent` |
| `InternetService` | `streaming_quality` |
| `MultipleLines` | `shared_profiles` |
| `OnlineBackup` | `offline_downloads` |
| `Contract` | `subscription_plan` |
| `Churn` | `churn` |

Des variables comportementales simulées ont été ajoutées:

- `views_per_week`
- `favorite_genre`
- `average_watch_time`
- `number_of_devices`
- `engagement_score`
- `subscription_value_ratio`

Ces variables rendent le scénario plus proche d’une vraie plateforme de streaming tout en restant reproductibles.

## Types de Données

Le dataset contient des variables numériques, binaires et catégorielles. Les variables numériques incluent la durée d’abonnement, le prix mensuel, le total dépensé, les vues par semaine, le temps moyen de visionnage, le nombre d’appareils, le score d’engagement et le ratio de valeur.

## Valeurs Manquantes

Le principal problème concerne `TotalCharges`, renommé `total_spent`. Dans le fichier original, 11 valeurs sont vides. Elles sont converties en valeurs manquantes numériques puis traitées par imputation médiane dans le pipeline de preprocessing.

## Doublons

La variable `customer_id` doit être unique. Un contrôle des doublons est nécessaire avant la modélisation:

```python
df["customer_id"].duplicated().sum()
```

En production, si des doublons apparaissent, il faut conserver l’enregistrement le plus récent selon la date d’extraction.

## Statistiques Descriptives

Les variables clés à analyser sont:

- `subscription_months`
- `monthly_subscription_fee`
- `total_spent`
- `views_per_week`
- `average_watch_time`
- `engagement_score`

Ces statistiques permettent d’identifier les profils extrêmes, la dispersion des prix et les comportements d’engagement.

## Distribution de la Variable Cible

Le dataset contient 1 869 churners et 5 174 non-churners. Le taux de churn est donc de 26.54%, ce qui correspond au contexte métier annoncé. Le churn est une classe minoritaire; il faut donc utiliser une séparation stratifiée et traiter le déséquilibre uniquement sur les données d’entraînement.

## Corrélation et Heatmap

La heatmap de corrélation porte sur les variables numériques. Elle permet d’observer les liens entre ancienneté, prix, dépenses, engagement et churn. Les corrélations ne prouvent pas la causalité, mais elles orientent l’analyse métier et la modélisation.

## Histogrammes et Boxplots

Les visualisations recommandées sont:

- Histogramme de `subscription_months`.
- Histogramme de `monthly_subscription_fee`.
- Histogramme de `total_spent`.
- Boxplot du prix mensuel selon le churn.
- Boxplot de l’ancienneté selon le churn.
- Boxplot du score d’engagement selon le churn.

Interprétation attendue:

- Les churners sont souvent concentrés parmi les nouveaux abonnés.
- Les abonnements mensuels sont plus exposés au churn.
- Un prix élevé avec un faible engagement peut signaler une faible perception de valeur.

## Analyse du Churn par Catégorie

Dimensions recommandées:

- `subscription_plan`
- `streaming_quality`
- `payment_method`
- `offline_downloads`
- `premium_support`
- `favorite_genre`

Les équipes métier peuvent utiliser ces analyses pour créer des campagnes de rétention segmentées.

## Analyse du Plan d’Abonnement

Le plan d’abonnement est un levier majeur. Les clients sur un plan mensuel sont généralement plus mobiles et plus sensibles aux offres concurrentes. Une action possible consiste à proposer aux clients à risque une migration vers un plan annuel avec avantage promotionnel.

## Analyse du Prix Mensuel

Le prix mensuel peut refléter la sensibilité au prix ou la profondeur de l’offre. Un prix élevé n’est pas forcément négatif si l’engagement est fort. L’analyse doit donc combiner prix, engagement, ancienneté et type de plan.

## Analyse de l’Ancienneté

Le premier trimestre est une période critique. Les clients avec moins de 3 à 6 mois d’ancienneté doivent être suivis de près, surtout s’ils ont un plan mensuel et un faible engagement.
