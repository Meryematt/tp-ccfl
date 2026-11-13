DROP TABLE IF EXISTS reservation;
DROP TABLE IF EXISTS materiel;
DROP TABLE IF EXISTS association;
DROP TABLE IF EXISTS site;

CREATE TABLE site (
    code_site VARCHAR(7) PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    commune VARCHAR(100) NOT NULL,
    annee_ouverture INTEGER NOT NULL,
    surface_m2 INTEGER NOT NULL CHECK (surface_m2 > 0)
);

CREATE TABLE materiel (
    id_materiel INTEGER PRIMARY KEY,
    reference VARCHAR(20) NOT NULL,
    designation VARCHAR(150) NOT NULL,
    categorie VARCHAR(50) NOT NULL,
    etat VARCHAR(30) NOT NULL,
    annee_achat INTEGER,
    code_site VARCHAR(7) NOT NULL,
    valeur_achat NUMERIC(8, 2),
    CONSTRAINT fk_materiel_site
        FOREIGN KEY (code_site)
        REFERENCES site(code_site)
);

CREATE TABLE association (
    id_association INTEGER PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    type_association VARCHAR(50) NOT NULL,
    commune VARCHAR(100) NOT NULL,
    code_postal VARCHAR(5),
    date_convention DATE NOT NULL,
    code_site VARCHAR(7) NOT NULL,
    convention_active BOOLEAN NOT NULL,
    CONSTRAINT fk_association_site
        FOREIGN KEY (code_site)
        REFERENCES site(code_site)
);

CREATE TABLE reservation (
    id_reservation CHAR(7) PRIMARY KEY,
    id_materiel INTEGER NOT NULL,
    id_association INTEGER NOT NULL,
    code_site VARCHAR(7) NOT NULL,
    quantite INTEGER NOT NULL CHECK (quantite > 0),
    date_debut DATE NOT NULL,
    date_fin_prevue DATE NOT NULL,
    date_retour_reelle DATE,
    CONSTRAINT fk_reservation_materiel
        FOREIGN KEY (id_materiel)
        REFERENCES materiel(id_materiel),
    CONSTRAINT fk_reservation_association
        FOREIGN KEY (id_association)
        REFERENCES association(id_association),
    CONSTRAINT fk_reservation_site
        FOREIGN KEY (code_site)
        REFERENCES site(code_site),
    CONSTRAINT ck_reservation_dates
        CHECK (date_fin_prevue >= date_debut)
);

CREATE INDEX idx_reservation_code_site
    ON reservation(code_site);

CREATE INDEX idx_reservation_date_debut
    ON reservation(date_debut);

CREATE INDEX idx_reservation_id_materiel
    ON reservation(id_materiel);
