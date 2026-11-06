# Rapport de qualité des données CCFL

| Fichier | Colonne | Anomalie | Nombre | Pourcentage | Traitement |
|---|---|---|---:|---:|---|
| materiel.csv | ligne complète | Doublons stricts | 7 | 1.91 % | Voir règles de nettoyage du script |
| materiel.csv | annee_achat | Années d'achat vides | 9 | 2.45 % | Voir règles de nettoyage du script |
| materiel.csv | annee_achat | Années d'achat postérieures à 2026 | 5 | 1.36 % | Voir règles de nettoyage du script |
| materiel.csv | valeur_achat | Valeurs d'achat vides | 11 | 3.0 % | Voir règles de nettoyage du script |
| materiel.csv | categorie | Catégories entièrement en majuscules | 6 | 1.63 % | Voir règles de nettoyage du script |
| materiel.csv | categorie | Catégories avec espaces parasites | 5 | 1.36 % | Voir règles de nettoyage du script |
| materiel.csv | valeur_achat | Valeurs d'achat avec virgule décimale | 5 | 1.36 % | Voir règles de nettoyage du script |
| associations.csv | code_postal | Codes postaux vides | 9 | 4.29 % | Voir règles de nettoyage du script |
| associations.csv | type_association | Types d'association inconnus | 7 | 3.33 % | Voir règles de nettoyage du script |
| associations.csv | date_convention | Dates de convention au format JJ/MM/AAAA | 6 | 2.86 % | Voir règles de nettoyage du script |
| reservations.csv | ligne complète | Doublons stricts | 18 | 0.39 % | Voir règles de nettoyage du script |
| reservations.csv | id_materiel | Réservations sans matériel correspondant | 21 | 0.45 % | Voir règles de nettoyage du script |
| reservations.csv | date_retour_reelle | Retours antérieurs au début du prêt | 15 | 0.32 % | Voir règles de nettoyage du script |
| reservations.csv | quantite | Réservations avec quantité égale à zéro | 6 | 0.13 % | Voir règles de nettoyage du script |

## Nombre de lignes avant et après

- Matériel : 367 avant, 360 après.
- Associations : 210 avant, 210 après.
- Réservations : 4618 avant, 4560 après.

## Prêts en cours

- Avant nettoyage : 72
- Après nettoyage : 71
- Une date de retour vide correspond à un prêt en cours et non à une anomalie.

## Points d'attention pour la direction

- Les catégories de matériel doivent être harmonisées dès la saisie.
- Les années d'achat futures ont été rendues vides, car leur valeur doit être confirmée.
- Les valeurs d'achat absentes restent absentes : aucune valeur n'a été inventée.
- Les réservations sans matériel correspondant ont été écartées pour garantir une base cohérente.
- Les prêts en cours sont conservés, car ils décrivent une situation normale du service.
