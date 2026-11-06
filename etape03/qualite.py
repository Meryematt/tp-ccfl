import pandas as pd

CHEMIN_MATERIEL = "data/materiel.csv"
CHEMIN_ASSOCIATIONS = "data/associations.csv"
CHEMIN_RESERVATIONS = "data/reservations.csv"

ANNEE_COURANTE = 2026


def ajouter_anomalie(anomalies, fichier, colonne, description, masque, dataframe):
    lignes_concernees = dataframe[masque]

    anomalies.append({
        "fichier": fichier,
        "colonne": colonne,
        "description": description,
        "nombre": len(lignes_concernees),
        "pourcentage": round(len(lignes_concernees) / len(dataframe) * 100, 2)
    })

    print("\n---", description, "---")
    print("Nombre :", len(lignes_concernees))
    print(lignes_concernees.head(3))


def main():
    anomalies = []

    df_materiel = pd.read_csv(
        CHEMIN_MATERIEL,
        dtype="string",
        keep_default_na=False)

    df_associations = pd.read_csv(
        CHEMIN_ASSOCIATIONS,
        dtype="string",
        keep_default_na=False)

    df_reservations = pd.read_csv(
        CHEMIN_RESERVATIONS,
        dtype="string",
        keep_default_na=False)

    # ----- Anomalies matériel -----

    ajouter_anomalie(
        anomalies,
        "materiel.csv",
        "ligne complète",
        "Doublons stricts",
        df_materiel.duplicated(),
        df_materiel
    )

    ajouter_anomalie(
        anomalies,
        "materiel.csv",
        "annee_achat",
        "Années d'achat vides",
        df_materiel["annee_achat"].str.strip() == "",
        df_materiel
    )

    annees_achat = pd.to_numeric(
        df_materiel["annee_achat"],
        errors="coerce"
    )

    ajouter_anomalie(
        anomalies,
        "materiel.csv",
        "annee_achat",
        "Années d'achat postérieures à 2026",
        annees_achat > ANNEE_COURANTE,
        df_materiel
    )

    ajouter_anomalie(
        anomalies,
        "materiel.csv",
        "valeur_achat",
        "Valeurs d'achat vides",
        df_materiel["valeur_achat"].str.strip() == "",
        df_materiel
    )

    ajouter_anomalie(
        anomalies,
        "materiel.csv",
        "categorie",
        "Catégories entièrement en majuscules",
        df_materiel["categorie"].str.strip().str.isupper(),
        df_materiel
    )

    ajouter_anomalie(
        anomalies,
        "materiel.csv",
        "categorie",
        "Catégories avec espaces parasites",
        df_materiel["categorie"] != df_materiel["categorie"].str.strip(),
        df_materiel
    )

    ajouter_anomalie(
        anomalies,
        "materiel.csv",
        "valeur_achat",
        "Valeurs d'achat avec virgule décimale",
        df_materiel["valeur_achat"].str.contains(",", regex=False),
        df_materiel
    )

    # ----- Anomalies associations -----

    ajouter_anomalie(
        anomalies,
        "associations.csv",
        "code_postal",
        "Codes postaux vides",
        df_associations["code_postal"].str.strip() == "",
        df_associations
    )

    ajouter_anomalie(
        anomalies,
        "associations.csv",
        "type_association",
        "Types d'association inconnus",
        df_associations["type_association"] == "inconnu",
        df_associations
    )

    ajouter_anomalie(
        anomalies,
        "associations.csv",
        "date_convention",
        "Dates de convention au format JJ/MM/AAAA",
        df_associations["date_convention"].str.contains(
            r"^\d{2}/\d{2}/\d{4}$",
            regex=True
        ),
        df_associations
    )

    # ----- Anomalies réservations -----

    ajouter_anomalie(
        anomalies,
        "reservations.csv",
        "ligne complète",
        "Doublons stricts",
        df_reservations.duplicated(),
        df_reservations
    )

    ajouter_anomalie(
        anomalies,
        "reservations.csv",
        "id_materiel",
        "Réservations sans matériel correspondant",
        ~df_reservations["id_materiel"].isin(df_materiel["id_materiel"]),
        df_reservations
    )

    dates_debut = pd.to_datetime(
        df_reservations["date_debut"],
        errors="coerce"
    )

    dates_retour = pd.to_datetime(
        df_reservations["date_retour_reelle"],
        errors="coerce"
    )

    ajouter_anomalie(
        anomalies,
        "reservations.csv",
        "date_retour_reelle",
        "Retours antérieurs au début du prêt",
        (dates_retour.notna()) & (dates_retour < dates_debut),
        df_reservations
    )

    quantites = pd.to_numeric(
        df_reservations["quantite"],
        errors="coerce"
    )

    ajouter_anomalie(
        anomalies,
        "reservations.csv",
        "quantite",
        "Réservations avec quantité égale à zéro",
        quantites == 0,
        df_reservations
    )

    prets_en_cours = (
        df_reservations["date_retour_reelle"].str.strip() == ""
    ).sum()

    print("\n--- Cas métier normal ---")
    print("Prêts en cours :", prets_en_cours)
    print("Nombre de catégories d'anomalies :", len(anomalies))

    
    
    # ----- Nettoyage du matériel -----

    materiel_propre = df_materiel.drop_duplicates().copy()

    materiel_propre["categorie"] = (
        materiel_propre["categorie"]
        .str.strip()
        .str.capitalize()
    )

    materiel_propre["valeur_achat"] = pd.to_numeric(
        materiel_propre["valeur_achat"].str.replace(",", ".", regex=False),
        errors="coerce"
    )

    annees_propres = pd.to_numeric(
        materiel_propre["annee_achat"],
        errors="coerce"
    )

    materiel_propre.loc[
        annees_propres > ANNEE_COURANTE,
        "annee_achat"
    ] = ""

    # ----- Nettoyage des associations -----

    associations_propre = df_associations.copy()

    dates_iso = pd.to_datetime(
        associations_propre["date_convention"],
        format="%Y-%m-%d",
        errors="coerce"
    )

    dates_francaises = pd.to_datetime(
        associations_propre["date_convention"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    associations_propre["date_convention"] = (
        dates_iso
        .fillna(dates_francaises)
        .dt.strftime("%Y-%m-%d")
        .fillna("")
    )

    # ----- Nettoyage des réservations -----

    reservations_propre = df_reservations.drop_duplicates().copy()

    dates_debut_propres = pd.to_datetime(
        reservations_propre["date_debut"],
        errors="coerce"
    )

    dates_retour_propres = pd.to_datetime(
        reservations_propre["date_retour_reelle"],
        errors="coerce"
    )

    quantites_propres = pd.to_numeric(
        reservations_propre["quantite"],
        errors="coerce"
    )

    materiel_inexistant = ~reservations_propre["id_materiel"].isin(
        materiel_propre["id_materiel"]
    )

    retour_impossible = (
        dates_retour_propres.notna()
        & (dates_retour_propres < dates_debut_propres)
    )

    quantite_nulle = quantites_propres == 0

    reservations_propre = reservations_propre[
        ~(materiel_inexistant | retour_impossible | quantite_nulle)
    ].copy()

    # ----- Exports CSV -----

    materiel_propre.to_csv(
        "sorties/materiel_propre.csv",
        index=False,
        encoding="utf-8",
        na_rep=""
    )

    associations_propre.to_csv(
        "sorties/associations_propre.csv",
        index=False,
        encoding="utf-8",
        na_rep=""
    )

    reservations_propre.to_csv(
        "sorties/reservations_propre.csv",
        index=False,
        encoding="utf-8",
        na_rep=""
    )

    # ----- Rapport Markdown -----

    prets_en_cours_apres = (
        reservations_propre["date_retour_reelle"].str.strip() == ""
    ).sum()

    with open(
        "sorties/rapport_qualite.md",
        "w",
        encoding="utf-8"
    ) as fichier:

        fichier.write("# Rapport de qualité des données CCFL\n\n")

        fichier.write(
            "| Fichier | Colonne | Anomalie | Nombre | Pourcentage | Traitement |\n"
        )
        fichier.write(
            "|---|---|---|---:|---:|---|\n"
        )

        for anomalie in anomalies:
            fichier.write(
                f"| {anomalie['fichier']} "
                f"| {anomalie['colonne']} "
                f"| {anomalie['description']} "
                f"| {anomalie['nombre']} "
                f"| {anomalie['pourcentage']} % "
                f"| Voir règles de nettoyage du script |\n"
            )

        fichier.write("\n## Nombre de lignes avant et après\n\n")
        fichier.write(
            f"- Matériel : {len(df_materiel)} avant, "
            f"{len(materiel_propre)} après.\n"
        )
        fichier.write(
            f"- Associations : {len(df_associations)} avant, "
            f"{len(associations_propre)} après.\n"
        )
        fichier.write(
            f"- Réservations : {len(df_reservations)} avant, "
            f"{len(reservations_propre)} après.\n"
        )

        fichier.write("\n## Prêts en cours\n\n")
        fichier.write(
            f"- Avant nettoyage : {prets_en_cours}\n"
        )
        fichier.write(
            f"- Après nettoyage : {prets_en_cours_apres}\n"
        )
        fichier.write(
            "- Une date de retour vide correspond à un prêt en cours "
            "et non à une anomalie.\n"
        )

        fichier.write("\n## Points d'attention pour la direction\n\n")
        fichier.write(
            "- Les catégories de matériel doivent être harmonisées "
            "dès la saisie.\n"
        )
        fichier.write(
            "- Les années d'achat futures ont été rendues vides, "
            "car leur valeur doit être confirmée.\n"
        )
        fichier.write(
            "- Les valeurs d'achat absentes restent absentes : "
            "aucune valeur n'a été inventée.\n"
        )
        fichier.write(
            "- Les réservations sans matériel correspondant ont été "
            "écartées pour garantir une base cohérente.\n"
        )
        fichier.write(
            "- Les prêts en cours sont conservés, car ils décrivent "
            "une situation normale du service.\n"
        )

    print("\nFichiers propres et rapport créés dans sorties/")


if __name__ == "__main__":
    main()