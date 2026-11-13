# TP CCFL - Pilotage du prêt de matériel aux associations

Projet d'exploration, de nettoyage, de chargement PostgreSQL et d'analyse SQL
des données de prêt de matériel de la CCFL.


## Prérequis

- Python 3.11 ou version plus récente ;
- PostgreSQL 14 ou version plus récente ;
- les commandes `psql` et `createdb` accessibles dans le terminal.

## Installation sur macOS

Depuis la racine du projet :

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Ouvrir ensuite `.env` et renseigner les paramètres PostgreSQL locaux.

## Installation sur Windows

Dans PowerShell, depuis la racine du projet :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Si PowerShell bloque l'activation, utiliser l'invite de commandes Windows :

```cmd
.venv\Scripts\activate.bat
```

## Configuration PostgreSQL

Le fichier `.env` est local et ne doit pas être envoyé sur GitHub. Il est créé
à partir de `.env.example` et contient les variables suivantes :

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ccfl
DB_USER=votre_utilisateur_postgresql
DB_PASSWORD=
```

Créer la base une seule fois, puis créer les tables :

```bash
createdb ccfl
psql -d ccfl -f etape04/schema.sql
```

Le script `schema.sql` peut être relancé sans erreur.

## Ordre d'exécution

Les commandes suivantes sont à lancer depuis la racine du projet :

```bash
python etape01/exploration.py
python etape02/analyse_pandas.py
python etape03/qualite.py
psql -d ccfl -f etape04/schema.sql
python etape05/chargement.py
psql -d ccfl -f etape06/analyses.sql
```

## Fichiers produits

- Étape 2 : `sorties/top10_materiel.csv`.
- Étape 3 : fichiers nettoyés et `sorties/rapport_qualite.md`.
- Étape 4 : `etape04/modelisation.md` et `etape04/schema.sql`.
- Étape 5 : `etape05/chargement.py`, `sorties/chargement.log` et, si besoin, `sorties/rejets_chargement.csv`.
- Étape 6 : `etape06/analyses.sql`.

