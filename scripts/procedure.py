import mysql.connector as mysql
from dotenv import load_dotenv
import os
import pandas as pd
from pathlib import Path

load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

def exporter_stock_disponible_csv(date_saisie):
    print("Execution de : Procedure")
    try:
        conn = mysql.connect(
            host='localhost',
            user=user,
            password=password,
            database='distributech',
            port=3306
        )
        cursor = conn.cursor()

        # Récupérer la liste des produits avec leur nom
        cursor.execute("""
            SELECT product_id, product_name
            FROM produits
        """)
        produits = cursor.fetchall()
        df_produits = pd.DataFrame(produits, columns=["product_id", "product_name"])

        # Quantité produite par produit
        cursor.execute(f"""
            SELECT product_id, SUM(quantity) AS quantite_produite
            FROM productions
            WHERE date_production <= DATE '{date_saisie}' 
            GROUP BY product_id
        """)
        prod_data = {row[0]: row[1] for row in cursor.fetchall()}

        # Quantité vendue par produit
        cursor.execute(f"""
            SELECT commandes_produits.product_id, SUM(commandes_produits.quantity) AS quantite_vendue
            FROM commandes_produits
            JOIN commandes ON commandes_produits.commande_id
            WHERE commandes.commande_date <= DATE '{date_saisie}'
            GROUP BY product_id
        """)
        vente_data = {row[0]: row[1] for row in cursor.fetchall()}

        # Calcul du stock disponible (produit - vendu) pour chaque produit
        stocks = []
        all_product_ids = set(prod_data.keys()) | set(vente_data.keys()) | set(df_produits["product_id"])
        for product_id in all_product_ids:
            produite = prod_data.get(product_id, 0)
            vendue = vente_data.get(product_id, 0)
            stock_disponible = produite - vendue
            stocks.append((product_id, stock_disponible))

        df_stock = pd.DataFrame(stocks, columns=["product_id", "stock_disponible"])

        # Joindre avec les noms de produits
        df_final = pd.merge(df_produits, df_stock, on="product_id", how="left").fillna(0)

        # Sauvegarde CSV
        output_dir = Path("../data/export")
        output_dir.mkdir(parents=True, exist_ok=True)
        csv_path = output_dir / f"stock_disponible_{date_saisie}.csv"
        df_final.to_csv(csv_path, index=False)

        print(f"CSV exporté : {csv_path}")

    except mysql.Error as e:
        print("Erreur lors de l’export du stock :", e)

    finally:
        cursor.close()
        conn.close()
    print("Fermeture.")
if __name__ == "__main__":
    exporter_stock_disponible_csv()
