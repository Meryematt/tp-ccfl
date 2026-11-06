import pandas as pd

CHEMIN_SITES = "data/sites.csv"
CHEMIN_MATERIEL = "data/materiel.csv"
CHEMIN_ASSOCIATIONS = "data/associations.csv"
CHEMIN_RESERVATIONS = "data/reservations.csv"


def main():
    df_sites = pd.read_csv(CHEMIN_SITES)

    df_materiel = pd.read_csv(CHEMIN_MATERIEL)

    # .info() montre que la colonne "valeur_achat" est de type str
    # On remarque aussi que certaines valeurs utilisent une virgule comme séparateur décimal.
    df_materiel["valeur_achat"] = pd.to_numeric(
        df_materiel["valeur_achat"].str.replace(",", ".", regex=False),
        errors="coerce"
    )

    df_associations = pd.read_csv(CHEMIN_ASSOCIATIONS)

    df_reservations = pd.read_csv(
        CHEMIN_RESERVATIONS,
        parse_dates=[
            "date_debut",
            "date_fin_prevue",
            "date_retour_reelle"
        ]
    )

    print("--- Informations matériel ---")
    print("Shape :", df_materiel.shape)
    df_materiel.info()

    print("\nValeurs manquantes :")
    print(df_materiel.isna().sum())

    print("\n--- Informations réservations ---")
    print("Shape :", df_reservations.shape)
    df_reservations.info()

    print("\nValeurs manquantes :")
    print(df_reservations.isna().sum())

    print("\nType de valeur_achat :", df_materiel["valeur_achat"].dtype)
    print(df_materiel["valeur_achat"].head())

    print("\n--- Top 10 des matériels les plus chers ---")

    top_10_chers = (
        df_materiel[
            ["reference", "designation", "categorie", "valeur_achat"]
        ]
        .sort_values("valeur_achat", ascending=False)
        .head(10)
    )

    print(top_10_chers)

    print("\n--- Nombre de matériels par catégorie ---")

    materiels_par_categorie = (
        df_materiel
        .groupby("categorie")
        .size()
        .sort_values(ascending=False)
    )

    print(materiels_par_categorie)

    print("\n--- Réservations et quantités par site ---")

    reservations_par_site = (
        df_reservations
        .groupby("code_site")
        .agg(
            nb_reservations=("id_reservation", "size"),
            quantite_totale=("quantite", "sum")
        )
        .sort_values("nb_reservations", ascending=False)
    )

    print(reservations_par_site)

    
    print("\n--- Vérification des doublons de matériel ---")

    doublons_materiel = df_materiel[df_materiel.duplicated(subset="id_materiel", keep=False)]

    print(doublons_materiel)

    df_materiel_unique = df_materiel.drop_duplicates(subset="id_materiel")

    df_complet = df_reservations.merge(
        df_materiel_unique,
        on="id_materiel",
        how="left")

    df_complet = df_complet.merge(
        df_associations,
        on="id_association",
        how="left")

    print("\n--- Vérification de la fusion ---")
    print("Nombre de lignes après fusion :", df_complet.shape[0])

    materiels_manquants = df_complet["designation"].isna().sum()
    print("Réservations sans matériel correspondant :", materiels_manquants)


    print("\n--- Top 10 des matériels les plus réservés ---")

    top_10_reserves = (
        df_complet
        .dropna(subset=["designation"])
        .groupby(["id_materiel", "designation"])
        .size()
        .reset_index(name="nombre_reservations")
        .sort_values("nombre_reservations", ascending=False)
        .head(10)
    )

    print(top_10_reserves)

    top_10_reserves.to_csv(
        "sorties/top10_materiel.csv",
        index=False,
        encoding="utf-8"
    )

    print("\nFichier créé : sorties/top10_materiel.csv")

if __name__ == "__main__":
    main()