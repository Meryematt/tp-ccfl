-- Question 1 :
-- Par site : nombre de réservations, quantité totale réservée
-- et nombre d'associations distinctes.
-- Les sites sans réservation doivent aussi apparaître.

SELECT
    s.code_site,
    s.nom,
    COUNT(r.id_reservation) AS nombre_reservations,
    COALESCE(SUM(r.quantite), 0) AS quantite_totale,
    COUNT(DISTINCT r.id_association) AS nombre_associations
FROM site AS s
LEFT JOIN reservation AS r
    ON r.code_site = s.code_site
GROUP BY
    s.code_site,
    s.nom
ORDER BY nombre_reservations DESC;

-- Nombre de lignes attendu : 5.
-- POL-HAZ doit apparaître en tête.


-- Question 2 :
-- Nombre de réservations par mois de début de prêt.

SELECT
    TO_CHAR(date_debut, 'YYYY-MM') AS mois,
    COUNT(*) AS nombre_reservations
FROM reservation
GROUP BY
    TO_CHAR(date_debut, 'YYYY-MM')
ORDER BY mois;

-- Nombre de lignes attendu : 13.
-- Octobre 2026 est plus bas, car le mois est incomplet.


-- Question 3 :
-- Les 10 matériels les plus réservés.

SELECT
    m.id_materiel,
    m.designation,
    m.categorie,
    COUNT(r.id_reservation) AS nombre_reservations
FROM materiel AS m
JOIN reservation AS r
    ON r.id_materiel = m.id_materiel
GROUP BY
    m.id_materiel,
    m.designation,
    m.categorie
ORDER BY
    nombre_reservations DESC,
    m.id_materiel
LIMIT 10;

-- Nombre de lignes attendu : 10.


-- Question 4 :
-- Taux de retard global puis par site.
-- Seules les réservations closes sont prises en compte.

SELECT
    'GLOBAL' AS code_site,
    'Tous les sites' AS nom,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE date_retour_reelle > date_fin_prevue
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS taux_retard_pourcent
FROM reservation
WHERE date_retour_reelle IS NOT NULL

UNION ALL

SELECT
    s.code_site,
    s.nom,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE r.date_retour_reelle > r.date_fin_prevue
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS taux_retard_pourcent
FROM site AS s
JOIN reservation AS r
    ON r.code_site = s.code_site
WHERE r.date_retour_reelle IS NOT NULL
GROUP BY
    s.code_site,
    s.nom
ORDER BY code_site;

-- Nombre de lignes attendu : 6.
-- Le taux GLOBAL doit être compris entre 30 % et 35 %.


-- Question 5 :
-- Catégories dont le nombre de réservations est supérieur
-- à la moyenne des catégories.

WITH reservations_par_categorie AS (
    SELECT
        m.categorie,
        COUNT(r.id_reservation) AS nombre_reservations
    FROM materiel AS m
    JOIN reservation AS r
        ON r.id_materiel = m.id_materiel
    GROUP BY m.categorie
),

moyenne_categories AS (
    SELECT
        AVG(nombre_reservations) AS moyenne_reservations
    FROM reservations_par_categorie
)

SELECT
    r.categorie,
    r.nombre_reservations
FROM reservations_par_categorie AS r
CROSS JOIN moyenne_categories AS m
WHERE r.nombre_reservations > m.moyenne_reservations
ORDER BY r.nombre_reservations DESC;

-- Nombre de lignes attendu : 2.


-- Question 6 :
-- Pour chaque site, matériel le plus réservé.
-- Une ligne par site.

WITH classement_materiel AS (
    SELECT
        s.code_site,
        s.nom AS nom_site,
        m.id_materiel,
        m.designation,
        COUNT(r.id_reservation) AS nombre_reservations,
        ROW_NUMBER() OVER (
            PARTITION BY s.code_site
            ORDER BY
                COUNT(r.id_reservation) DESC,
                m.id_materiel
        ) AS rang
    FROM site AS s
    JOIN reservation AS r
        ON r.code_site = s.code_site
    JOIN materiel AS m
        ON m.id_materiel = r.id_materiel
    GROUP BY
        s.code_site,
        s.nom,
        m.id_materiel,
        m.designation
)

SELECT
    code_site,
    nom_site,
    id_materiel,
    designation,
    nombre_reservations
FROM classement_materiel
WHERE rang = 1
ORDER BY code_site;

-- Nombre de lignes attendu : 5.


-- Question 7 :
-- Durée réelle moyenne de prêt, globalement puis par catégorie.
-- Seules les réservations closes sont prises en compte.

WITH durees_moyennes AS (
    SELECT
        0 AS ordre,
        'GLOBAL' AS categorie,
        ROUND(
            AVG(date_retour_reelle - date_debut),
            1
        ) AS duree_moyenne_jours
    FROM reservation
    WHERE date_retour_reelle IS NOT NULL

    UNION ALL

    SELECT
        1 AS ordre,
        m.categorie,
        ROUND(
            AVG(r.date_retour_reelle - r.date_debut),
            1
        ) AS duree_moyenne_jours
    FROM materiel AS m
    JOIN reservation AS r
        ON r.id_materiel = m.id_materiel
    WHERE r.date_retour_reelle IS NOT NULL
    GROUP BY m.categorie
)

SELECT
    categorie,
    duree_moyenne_jours
FROM durees_moyennes
ORDER BY
    ordre,
    categorie;

-- La durée globale attendue est proche de 6 jours.


-- Analyse des coûts :
-- Les requêtes utilisant plusieurs jointures et agrégats sont les plus coûteuses.
-- Les requêtes 3 et 6 comptent les réservations par matériel et peuvent traiter beaucoup de lignes.
-- La question 6 utilise aussi une fonction fenêtre pour classer les matériels par site.
-- Les index sur reservation(code_site), reservation(date_debut) et reservation(id_materiel)
-- réduisent le coût des jointures, des regroupements par site et de l'analyse mensuelle.