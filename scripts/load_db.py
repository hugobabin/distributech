import os
import pandas as pd
import mysql.connector as mysql
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def load_db():
    print("Execution de : Load") 
    # Charger les variables d'environnement
    load_dotenv()

    # Connexion à la base MySQL
    try:
        conn = mysql.connect(
            host='localhost',
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database='distributech',
            port=3306
        )
        print("Connexion à MySQL réussie")
    except Exception as e:
        print("Erreur de connexion :", e)
        return

    cursor = conn.cursor()

    # Chemin vers les fichiers transformés
    DATA_PATH = "../data/transform"

    # Liste des fichiers CSV à charger
    fichiers_csv = {
        "regions": "regions_transforme.csv",
        "revendeurs": "revendeurs_transforme.csv",
        "produits": "produits_transforme.csv",
        "productions": "productions_transforme.csv",
        "paniers": "paniers_transforme.csv",
        "commandes": "commandes_transforme.csv",
        "commandes_produits": "commandes_produits_transforme.csv",
    }

    # Fonction d'insertion
    def inserer_donnees(table, df):
        colonnes = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        requete = f"INSERT INTO {table} ({colonnes}) VALUES ({placeholders})"
        
        for _, ligne in df.iterrows():
            cursor.execute(requete, tuple(ligne))

    # Insérer chaque fichier dans la table correspondante
    for table, fichier in fichiers_csv.items():
        chemin_fichier = os.path.join(DATA_PATH, fichier)
        if os.path.exists(chemin_fichier):
            df = pd.read_csv(chemin_fichier)
            print(f"Insertion des données dans la table `{table}` depuis `{fichier}`")
            inserer_donnees(table, df)
        else:
            print(f"Fichier introuvable : {fichier}")

    # Commit des insertions
    conn.commit()

    # Appel de la procédure stockée (décommenter si besoin)
    # try:
    #     cursor.callproc("proc_suivre_stock")
    #     print("Suivi de stock mis à jour avec succès.")
    # except Exception as e:
    #     print("Erreur lors de l'appel à la procédure :", e)

    # Fermer connexion
    cursor.close()
    conn.close()

    print()
# Exécution si script principal
if __name__ == "__main__":
    load_db()