## MCD - Schéma textuel

### Entités et propriétés

- **SITE** : code_site, nom, commune, annee_ouverture, surface_m2.
- **MATERIEL** : id_materiel, reference, designation, categorie, etat, annee_achat, valeur_achat.
- **ASSOCIATION** : id_association, nom, type_association, commune, code_postal, date_convention, convention_active.
- **RESERVATION** : id_reservation, quantite, date_debut, date_fin_prevue, date_retour_reelle.

### Associations et cardinalités

```text
SITE (0,N) ── stocke ── (1,1) MATERIEL

SITE (0,N) ── rattache ── (1,1) ASSOCIATION

ASSOCIATION (0,N) ── effectue ── (1,1) RESERVATION

MATERIEL (0,N) ── est concerné par ── (1,1) RESERVATION

SITE (0,N) ── est le site de retrait de ── (1,1) RESERVATION
```


## MLD - Relations, clés et types

```text
SITE(
    code_site VARCHAR(7) PK,
    nom VARCHAR(100),
    commune VARCHAR(100),
    annee_ouverture INTEGER,
    surface_m2 INTEGER
)

MATERIEL(
    id_materiel INTEGER PK,
    reference VARCHAR(20),
    designation VARCHAR(150),
    categorie VARCHAR(50),
    etat VARCHAR(30),
    annee_achat INTEGER NULL,
    code_site VARCHAR(7) FK -> SITE(code_site),
    valeur_achat NUMERIC(8,2) NULL
)

ASSOCIATION(
    id_association INTEGER PK,
    nom VARCHAR(150),
    type_association VARCHAR(50),
    commune VARCHAR(100),
    code_postal VARCHAR(5) NULL,
    date_convention DATE,
    code_site VARCHAR(7) FK -> SITE(code_site),
    convention_active BOOLEAN
)

RESERVATION(
    id_reservation CHAR(7) PK,
    id_materiel INTEGER FK -> MATERIEL(id_materiel),
    id_association INTEGER FK -> ASSOCIATION(id_association),
    code_site VARCHAR(7) FK -> SITE(code_site),
    quantite INTEGER,
    date_debut DATE,
    date_fin_prevue DATE,
    date_retour_reelle DATE NULL
)
```


## Justifications des choix de modélisation

- `id_reservation` est une clé de type `CHAR(7)` car les identifiants suivent le format fixe `R250000`.
- Cet identifiant contient une lettre et ne doit donc pas être traité comme un nombre.
- `valeur_achat` utilise le type `NUMERIC(8,2)` afin de conserver une valeur monétaire exacte à deux décimales.
- Un type `FLOAT` est déconseillé pour un montant : il peut introduire des erreurs d'arrondi.
- `convention_active` devient un booléen : `oui` est converti en `TRUE` et `non` en `FALSE` au chargement.
- Un booléen évite les variantes de saisie possibles avec un champ texte.
- `date_retour_reelle` peut être nulle, car une date absente correspond à un prêt encore en cours.
- Cette absence est une situation métier normale et ne doit pas être remplacée par une date inventée.
- `code_site` sur `materiel` indique le site de stockage du matériel.
- `code_site` sur `association` indique le pôle de rattachement habituel de l'association.
- `code_site` sur `reservation` indique le site réellement concerné par le retrait et le retour.
- Cette dernière information est conservée pour l'historique et le suivi opérationnel, même si elle correspond souvent au site de rattachement.
