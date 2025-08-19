## Contexte

Le projet Distributech est un projet qui propose une approche ETL afin d'extraire des données en provenance de deux sources (un fichier CSV et une base de données SQLite). Le système permet par ailleurs en lancant le main d'exporter les stocks à date donnée en argument (si aucun n'est fourni, la date du jour est prise en compte).

## Collaborateurs

- https://github.com/khaoulaMili123
- https://github.com/CortoGyt

## Librairies utilisées

- pandas
- mysql-connector-python

## Installation et utilisation

- git clone https://github.com/hugobabin/distributech (dans le répertoire où vous souhaitez)
- docker-compose up -d (dans le répertoire bdd)
- python3 -m venv .venv (dans la racine du projet)
- source .venv/bin/activate (dans la racine du projet)
- pip install -r requirements.txt (dans la racine du projet)
- python3 main.py 2025 08 01 (date optionnelle comme expliqué dans contexte, à exécuter dans le répertoire scripts du projet)

Les exports sont au format CSV et sont disponibles dans le sous-répertoire export du répertoire data.
Merci pour la lecture ;)

