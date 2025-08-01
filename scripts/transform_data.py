# transformer_donnees.py

import pandas as pd
from pathlib import Path
from typing import Dict

def nettoyer_donnees(donnees_brutes, donnees_transformees):
    # Parcourt les données brutes
    print("Nettoyage des datas")
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

def transformer_donnees(donnees_brutes) -> Dict[str, pd.DataFrame]:
    """
    Récupère les données brutes d'extraction et les transforme.
    Enregistre les DataFrames transformés dans des fichiers CSV.
    Renvoie un dictionnaire de DataFrames pandas transformés.
    """
    print("Execution de : Transform") 
    # Initialise un dictionnaire pour stocker les DataFrames transformés
    donnees_transformees = {}

    # Nettoyage données
    nettoyer_donnees(donnees_brutes, donnees_transformees)
    
    # Récupère commandes
    commandes: pd.DataFrame = donnees_transformees["commandes"]
    print("Calculs")
    # Calcule total ligne pour chaque ligne de commande
    commandes["total_ligne"] = commandes["quantity"] * commandes["unit_price"]

    # DataFrame commandes_produits avec uniquement les données qui nous intéressent
    donnees_transformees["commandes_produits"] = commandes.copy()
    commandes_produits = donnees_transformees["commandes_produits"]
    commandes_produits.drop(["commande_date", "revendeur_id", "region_id"], axis=1, inplace=True)

    # Création d'un DataFrame paniers avec un id et un total
    donnees_transformees["paniers"] = commandes.groupby(["numero_commande"])[["total_ligne"]].sum().reset_index()
    paniers = donnees_transformees["paniers"]
    paniers.insert(1, "panier_id", range(1, len(paniers) + 1))
    paniers.rename(columns={"total_ligne": "total_panier"}, inplace=True)

    # Crée un mapping entre numero commande et panier id pour ajouter le bon panier id au DataFrame commandes
    id_panier_commande = dict(zip(paniers["numero_commande"], paniers["panier_id"]))
    commandes["panier_id"] = commandes["numero_commande"].map(id_panier_commande)

    # Supprime le numero commande du DataFrame paniers
    paniers.drop("numero_commande", axis=1, inplace=True)

    # Suppression des données superflues dans le DataFrame commandes
    commandes.drop(["product_id", "quantity", "unit_price", "total_ligne", "region_id"], axis=1, inplace=True)
    commandes.drop_duplicates(inplace=True)

    # Création d'un id pour chaque commande
    commandes.insert(0, "commande_id", range(1, len(commandes) + 1))

    # Mapping de id commande en fonction de numero commande pour ajouter id commande à commandes produits
    id_commandes_produits = dict(zip(commandes["numero_commande"], commandes["commande_id"]))
    commandes_produits["numero_commande"] = commandes_produits["numero_commande"].map(id_commandes_produits)
    commandes_produits.rename(columns={"numero_commande": "commande_id"}, inplace=True)
    print("Enregistrement CSV")
    # Enregistre les données transformées dans des fichiers CSV individuels
    chemin_donnees_transformees = "../data/transform/"
    DOSSIER_SORTIE = Path(chemin_donnees_transformees)
    DOSSIER_SORTIE.mkdir(parents=True, exist_ok=True)
    for nom, df in donnees_transformees.items():
        chemin_fichier = chemin_donnees_transformees + f"{nom}_transforme.csv"
        df.to_csv(chemin_fichier, index=False)
    print("Fermeture.")
    return donnees_transformees
    
if __name__ == "__main__":
    """
    Mode dev si lancement direct du script.
    Affiche les données transformées de chaque DataFrame du dictionnaire.
    """
    
    # Récupère les données transformées
    dfs = transformer_donnees("")

    # Affiche les données de chaque DataFrame du dictionnaire
    for nom, df in dfs.items():
        print(f"\n--- {nom.upper()} ---")
        print(df.head())
        