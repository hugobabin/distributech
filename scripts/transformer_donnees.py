# transformer_donnees.py

import pandas as pd
from extraire_donnees import extraire_donnees
from pathlib import Path
from typing import Dict

"""
Récupère les données brutes d'extraction et les transforme.
Enregistre les DataFrames transformés dans des fichiers CSV.
Renvoie un dictionnaire de DataFrames pandas transformés.
"""
def transformer_donnees() -> Dict[str, pd.DataFrame]:

    # Charge les données brutes d'extraction
    donnees_brutes = extraire_donnees()

    # Initialise un dictionnaire pour stocker les DataFrames transformés
    donnees_transformees = {}

    # Parcourt les données brutes
    for nom, df in donnees_brutes.items():

        # Supprime les doublons
        df = df.drop_duplicates()

        # Supprime les colonnes entièrement vides
        df = df.dropna(axis=1, how="all")

        # Normalise le format des dates au format datetime
        for col in df.columns:
            if "date" in col.lower():
                df[col] = pd.to_datetime(df[col], errors="coerce")

        # Intègre le DataFrame transformé dans un nouveau dictionnaire
        donnees_transformees[nom] = df

    # Enregistre les données transformées dans des fichiers CSV individuels
    chemin_donnees_transformees = "../data/transform/"
    DOSSIER_SORTIE = Path(chemin_donnees_transformees)
    DOSSIER_SORTIE.mkdir(parents=True, exist_ok=True)
    for nom, df in donnees_transformees.items():
        chemin_fichier = chemin_donnees_transformees + f"{nom}_transforme.csv"
        df.to_csv(chemin_fichier, index=False)

    return donnees_transformees

"""
Mode dev si lancement direct du script.
Affiche les données transformées de chaque DataFrame du dictionnaire.
"""
if __name__ == "__main__":
    
    # Récupère les données transformées
    dfs = transformer_donnees()

    # Affiche les données de chaque DataFrame du dictionnaire
    for nom, df in dfs.items():
        print(f"\n--- {nom.upper()} ---")
        print(df.head())