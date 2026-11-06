import csv
from collections import Counter

CHEMIN_SITES = "data/sites.csv"
CHEMIN_MATERIEL = "data/materiel.csv"
CHEMIN_ASSOCIATIONS = "data/associations.csv"
CHEMIN_RESERVATIONS = "data/reservations.csv"


def lire_csv(chemin):
    with open(chemin, encoding="utf-8", newline="") as fichier:
        lecteur = csv.DictReader(fichier)
        return list(lecteur)


def compter_par(lignes, colonne):
    compteurs = Counter()

    for ligne in lignes:
        compteurs[ligne[colonne]] += 1

    return compteurs


def total_par(lignes, colonne_groupe, colonne_valeur):
    totaux = Counter()

    for ligne in lignes:
        groupe = ligne[colonne_groupe]
        valeur = int(ligne[colonne_valeur])
        totaux[groupe] += valeur

    return totaux


class Site:
    def __init__(self, code_site, nom, commune, annee_ouverture, surface_m2):
        self.code_site = code_site
        self.nom = nom
        self.commune = commune
        self.annee_ouverture = int(annee_ouverture)
        self.surface_m2 = int(surface_m2)

    def anciennete(self, annee_reference):
        return annee_reference - self.annee_ouverture

    def __str__(self):
        return (
            f"{self.code_site} - {self.nom} "
            f"({self.commune}), {self.surface_m2} m2"
        )


def reservations_en_cours(reservations):
    liste_en_cours = []

    for reservation in reservations:
        if reservation["date_retour_reelle"].strip() == "":
            liste_en_cours.append(reservation)

    return liste_en_cours



def main():
    sites = lire_csv(CHEMIN_SITES)
    materiels = lire_csv(CHEMIN_MATERIEL)
    associations = lire_csv(CHEMIN_ASSOCIATIONS)
    reservations = lire_csv(CHEMIN_RESERVATIONS)

    print("Nombre de sites :", len(sites))
    print("Nombre de matériels :", len(materiels))
    print("Nombre d'associations :", len(associations))
    print("Nombre de réservations :", len(reservations))

    print("\n--- Sites ---")
    for ligne in sites:
        site = Site(**ligne)
        print(site, "-", site.anciennete(2026), "ans")

    print("\n--- Réservations par site ---")
    comptage_reservations = compter_par(reservations, "code_site")

    for code_site, nombre in comptage_reservations.most_common():
        print(code_site, ":", nombre)

    print("\n--- Quantité totale réservée par site ---")
    quantites_par_site = total_par(
        reservations,
        "code_site",
        "quantite"
    )

    for code_site, quantite in quantites_par_site.most_common():
        print(code_site, ":", quantite)

    print("\n--- Matériels par état ---")
    materiels_par_etat = compter_par(materiels, "etat")

    for etat, nombre in materiels_par_etat.items():
        print(etat, ":", nombre)

    categories = set()

    for materiel in materiels:
        categories.add(materiel["categorie"])

    print("\nNombre de catégories distinctes :", len(categories))

    en_cours = reservations_en_cours(reservations)
    print("Nombre de réservations en cours :", len(en_cours))


if __name__ == "__main__":
    main()