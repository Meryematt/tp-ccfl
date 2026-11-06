# Auto-évaluation — ATTARI Meryem

## Étapes

| Étape | État (terminée / partielle / non abordée) | Points de vérification obtenus | Ce qui a bloqué | Temps réel passé par étape |
|---|---|---|---|---|
| 1 | terminée | Lecture des 4 CSV ; 5 sites, 367 matériels, 210 associations et 4618 réservations affichés ; POL-HAZ est le site ayant le plus de réservations avec 1869 ; 181 matériels à l’état bon ; plus de 6 catégories distinctes ; 72 réservations en cours. | Utilisation de `Counter.most_common()` pour afficher les résultats du plus grand au plus petit. | 45min |
| 2 | terminée | Chargement des 4 CSV avec pandas ; formes vérifiées : 367 matériels et 4618 réservations ; dates des réservations converties ; `valeur_achat` convertie en nombre ; 72 retours réels manquants identifiés comme prêts en cours ; 21 réservations sans matériel correspondant détectées ; fusion des tables réalisée ; top 10 des matériels les plus réservés exporté dans `sorties/top10_materiel.csv`. | - | 35 min |
| 3 | terminée | Audit de 14 catégories d'anomalies ; génération de trois fichiers nettoyés et d'un rapport qualité ; 360 matériels conservés avec 6 catégories homogènes ; prêts en cours conservés comme cas métier normal. | J’ai dû comprendre pourquoi les données devaient d’abord être lues comme du texte pour repérer les cellules vides, les espaces, les majuscules et les formats différents. J’ai compris la différence entre `parse_dates` et `pd.to_datetime()`. `parse_dates` convertit les dates dès la lecture du CSV, ce qui est pratique pour une analyse directe. Lors d’un audit de qualité, j’ai compris qu’il est préférable de conserver d’abord les valeurs brutes afin de repérer les formats incohérents, puis d’utiliser `pd.to_datetime()` pour convertir et contrôler les dates. | 1h |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |
| 7 | | | | |

## Ce que je sais faire mieux qu'en septembre
(3 lignes)

## Ce qui me résiste encore
(3 lignes)

