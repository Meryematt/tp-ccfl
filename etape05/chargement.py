from dotenv import load_dotenv
import logging
import os

from sqlalchemy import URL, create_engine, text
import time
from sqlalchemy.engine import Connection

import pandas as pd
from pathlib import Path

load_dotenv()

logging.basicConfig(
    filename="sorties/chargement.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


CHEMIN_SITES = Path("data/sites.csv")
CHEMIN_MATERIEL = Path("sorties/materiel_propre.csv")
CHEMIN_ASSOCIATIONS = Path("sorties/associations_propre.csv")
CHEMIN_RESERVATIONS = Path("sorties/reservations_propre.csv")

def creer_engine():
    url = URL.create(
        "postgresql+psycopg",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD") or None,
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME", "ccfl")
    )

    return create_engine(url)

def lire_donnees():
    df_sites = pd.read_csv(CHEMIN_SITES)

    df_materiel = pd.read_csv(CHEMIN_MATERIEL)

    df_associations = pd.read_csv(
        CHEMIN_ASSOCIATIONS,
        parse_dates=["date_convention"]
    )

    df_associations["convention_active"] = (
        df_associations["convention_active"]
        .map({
            "oui": True,
            "non": False
        })
    )

    df_reservations = pd.read_csv(
        CHEMIN_RESERVATIONS,
        parse_dates=[
            "date_debut",
            "date_fin_prevue",
            "date_retour_reelle"
        ]
    )

    return (
        df_sites,
        df_materiel,
        df_associations,
        df_reservations
    )

def preparer_lignes(dataframe):
    dataframe = dataframe.astype(object).where(
        dataframe.notna(),
        None
    )

    return dataframe.to_dict(orient="records")

def vider_tables(connexion):
    connexion.execute(
        text("""
            TRUNCATE TABLE
                reservation,
                materiel,
                association,
                site
        """)
    )

def inserer_par_lots(
    connexion: Connection,
    requete,
    lignes: list,
    nom_table: str
) -> tuple:
    nombre_inserees = 0
    rejets = []
    debut = time.perf_counter()

    for position in range(0, len(lignes), 500):
        lot = lignes[position:position + 500]

        try:
            with connexion.begin_nested():
                connexion.execute(requete, lot)

            nombre_inserees += len(lot)

        except Exception:
            for ligne in lot:
                try:
                    with connexion.begin_nested():
                        connexion.execute(requete, ligne)

                    nombre_inserees += 1

                except Exception as erreur:
                    ligne_rejetee = ligne.copy()
                    ligne_rejetee["table"] = nom_table
                    ligne_rejetee["motif_rejet"] = str(erreur)
                    rejets.append(ligne_rejetee)

    duree = time.perf_counter() - debut

    logging.info(
        "%s : %s lues, %s insérées, %s rejetées, %.2f secondes",
        nom_table,
        len(lignes),
        nombre_inserees,
        len(rejets),
        duree
    )

    return nombre_inserees, rejets

def charger_sites(
    connexion: Connection,
    dataframe: pd.DataFrame
) -> tuple:
    requete = text("""
        INSERT INTO site (
            code_site, nom, commune,
            annee_ouverture, surface_m2
        )
        VALUES (
            :code_site, :nom, :commune,
            :annee_ouverture, :surface_m2
        )
    """)

    lignes = preparer_lignes(dataframe)

    return inserer_par_lots(
        connexion,
        requete,
        lignes,
        "site"
    )


def charger_materiels(
    connexion: Connection,
    dataframe: pd.DataFrame
) -> tuple:
    requete = text("""
        INSERT INTO materiel (
            id_materiel, reference, designation,
            categorie, etat, annee_achat,
            code_site, valeur_achat
        )
        VALUES (
            :id_materiel, :reference, :designation,
            :categorie, :etat, :annee_achat,
            :code_site, :valeur_achat
        )
    """)

    lignes = preparer_lignes(dataframe)

    return inserer_par_lots(
        connexion,
        requete,
        lignes,
        "materiel"
    )

def charger_associations(
    connexion: Connection,
    dataframe: pd.DataFrame
) -> tuple:
    requete = text("""
        INSERT INTO association (
            id_association, nom, type_association,
            commune, code_postal, date_convention,
            code_site, convention_active
        )
        VALUES (
            :id_association, :nom, :type_association,
            :commune, :code_postal, :date_convention,
            :code_site, :convention_active
        )
    """)

    lignes = preparer_lignes(dataframe)

    return inserer_par_lots(
        connexion,
        requete,
        lignes,
        "association"
    )


def charger_reservations(
    connexion: Connection,
    dataframe: pd.DataFrame
) -> tuple:
    requete = text("""
        INSERT INTO reservation (
            id_reservation, id_materiel,
            id_association, code_site, quantite,
            date_debut, date_fin_prevue,
            date_retour_reelle
        )
        VALUES (
            :id_reservation, :id_materiel,
            :id_association, :code_site, :quantite,
            :date_debut, :date_fin_prevue,
            :date_retour_reelle
        )
    """)

    lignes = preparer_lignes(dataframe)

    return inserer_par_lots(
        connexion,
        requete,
        lignes,
        "reservation"
    )

def main():
    engine = creer_engine()

    (
        df_sites,
        df_materiel,
        df_associations,
        df_reservations
    ) = lire_donnees()

    tous_les_rejets = []

    with engine.begin() as connexion:
        vider_tables(connexion)

        _, rejets = charger_sites(
            connexion,
            df_sites
        )
        tous_les_rejets.extend(rejets)

        _, rejets = charger_materiels(
            connexion,
            df_materiel
        )
        tous_les_rejets.extend(rejets)

        _, rejets = charger_associations(
            connexion,
            df_associations
        )
        tous_les_rejets.extend(rejets)

        _, rejets = charger_reservations(
            connexion,
            df_reservations
        )
        tous_les_rejets.extend(rejets)

    if tous_les_rejets:
        df_rejets = pd.DataFrame(tous_les_rejets)

        df_rejets.to_csv(
            "sorties/rejets_chargement.csv",
            index=False,
            encoding="utf-8"
        )

        print("Rejets enregistrés dans sorties/rejets_chargement.csv")

    else:
        print("Aucun rejet de chargement.")

    print("Chargement terminé.")


if __name__ == "__main__":
    main()