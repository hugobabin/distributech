from extraire_donnees import extraire_donnees
from transform_data import transformer_donnees
from create_db import create_db
from load_db import load_db
from procedure import exporter_stock_disponible_csv

def main():
    print("\n===EXTRACTION===")
    donnees_brutes = extraire_donnees()

    print("\n===TRANSFORMATION===")
    transformer_donnees(donnees_brutes)

    print("\n===CRÉATION BASE DE DONNÉES===")
    create_db()

    print("\n===CHARGEMENT DES DONNÉES===")
    load_db()

    print("\n===EXPORT STOCK DISPONIBLE===")
    exporter_stock_disponible_csv()

if __name__ == "__main__":
    main()