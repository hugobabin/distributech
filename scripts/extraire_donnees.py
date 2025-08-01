# extraire_donnee.py

import sqlite3
import pandas as pd
from typing import Dict

def extraire_donnees() -> Dict[str, pd.DataFrame]:
    print("Execution de : Extract") 
    # Chemins vers la base de données SQLite et le fichier CSV
    chemin_bdd = "../data/base_stock.sqlite"
    chemin_csv = "../data/commande_revendeur_tech_express.csv"

    """
    Extrait les donnéess de la base de données SQLite et du fichier CSV.
    Renvoie un dictionnaire de DataFrames pandas.
    """
    print("Extraction en cours")
    # Connecte à la base de données SQLite
    try :
        conn = sqlite3.connect(chemin_bdd)
        print("Connection à la BDD SqLite réussie.")
    except Exception as e :
        print("Erreur lors de la connection à la base SqLite", e)
        
    # Extrait les données vers des DataFrames pandas contenus dans un dictionnaire
    try :
        dataframes = {
            "productions": pd.read_sql_query("SELECT * FROM production", conn),
            "produits": pd.read_sql_query("SELECT * FROM produit", conn),
            "regions": pd.read_sql_query("SELECT * FROM region", conn),
            "revendeurs": pd.read_sql_query("SELECT * FROM revendeur", conn),
            "commandes": pd.read_csv(chemin_csv)
        }
        print("Dataframes OK.")
    except Exception as e :
        print("Erreur lors de l'extraction des données", e)
    # Ferme la connexion à la base de données
    conn.close()
    print("Fermeture.")

    # Retourne le dictionnaire de DataFrames
    return dataframes

"""
Mode dev si lancement direct du script.
Affiche les données de chaque DataFrame du dictionnaire.
"""
if __name__ == "__main__":

    # Récupère les données extraites
    dfs = extraire_donnees()

    # Affiche les données de chaque DataFrame du dictionnaire
    for nom, df in dfs.items():
        print(f"\n--- {nom.upper()} ---")
        print(df.head())