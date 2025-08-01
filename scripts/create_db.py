import mysql.connector as mysql
from dotenv import load_dotenv
import os

load_dotenv()
    # Connexion initiale au serveur MySQL (pas à une base spécifique)
def create_db():
    print("Execution de : Create") 
    try:
        conn = mysql.connect(
            host='localhost',
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=3306
        )
        print("Connexion à MySQL réussie.")
    except mysql.Error as e:
        print("Erreur lors de la connexion à MySQL :", e)
    cur = conn.cursor()

    # Création de la BDD si elle n'existe pas
    try:
        cur.execute("CREATE DATABASE IF NOT EXISTS distributech")
        print("Base de données 'distributech' créée ou déjà existante.")
    except Exception as e:
        print("Erreur lors de la création de la base de données :", e)
    # Fermeture de la première connexion
    
    cur.close()
    conn.close()
    print("Fermeture.")
    #ouverture 2eme connection (dans distributech)
    try:
        conn = mysql.connect(
            host='localhost',
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database='distributech',
            port=3306
        )
        print("Connexion à MySQL réussie.")
    except Exception as e:
        print("Erreur lors de la création de la base de données :", e)
    cur = conn.cursor()
    
    #drop si table déjà existante
    print("Tentative de drop des tables")

    try:
        cur.execute("DROP TABLE IF EXISTS commandes_produits")
        cur.execute("DROP TABLE IF EXISTS productions")
        cur.execute("DROP TABLE IF EXISTS commandes")
        cur.execute("DROP TABLE IF EXISTS paniers")
        cur.execute("DROP TABLE IF EXISTS revendeurs")
        cur.execute("DROP TABLE IF EXISTS produits")
        cur.execute("DROP TABLE IF EXISTS regions")
        print("Tables drop avec succès")
    except Exception as e:
        print("Erreur lors du drop des tables :", e)
    
    
    # Création des tables
    print("Création des tables")
    # Création de la table regions
    try:
        cur.execute("""
            CREATE TABLE regions (
                region_id INT PRIMARY KEY AUTO_INCREMENT,
                region_name VARCHAR(255) NOT NULL
            );
        """)
        print("1/7 Table 'regions' créée avec succès.")
    except Exception as e:
        print("Erreur lors de la création de 'regions' :", e)

    # Création de la table revendeurs
    try:
        cur.execute("""
            CREATE TABLE revendeurs (
                revendeur_id INT PRIMARY KEY AUTO_INCREMENT,
                revendeur_name VARCHAR(255) NOT NULL,
                region_id INT NOT NULL,
                FOREIGN KEY (region_id) REFERENCES regions(region_id)
            );
        """)
        print("2/7 Table 'revendeurs' créée avec succès.")
    except Exception as e:
        print("Erreur lors de la création de 'revendeurs' :", e)

    # Création de la table produits
    try:
        cur.execute("""
            CREATE TABLE produits (
                product_id INT PRIMARY KEY AUTO_INCREMENT,
                product_name VARCHAR(255) NOT NULL,
                cout_unitaire DECIMAL(10,2) NOT NULL
            );
        """)
        print("3/7 Table 'produits' créée avec succès.")
    except Exception as e:
        print("Erreur lors de la création de 'produits' :", e)

    # Création de la table productions
    try:
        cur.execute("""
            CREATE TABLE productions (
                production_id INT PRIMARY KEY AUTO_INCREMENT,
                product_id INT NOT NULL,
                quantity INT NOT NULL,
                date_production DATE NOT NULL,
                FOREIGN KEY (product_id) REFERENCES produits(product_id)
            );
        """)
        print("4/7 Table 'productions' créée avec succès.")
    except Exception as e:
        print("Erreur lors de la création de 'productions' :", e)

    # Création de la table paniers
    try:
        cur.execute("""
            CREATE TABLE paniers (
                panier_id INT PRIMARY KEY AUTO_INCREMENT,
                total_panier DECIMAL(10,2) NOT NULL
            );
        """)
        print("5/7 Table 'paniers' créée avec succès.")
    except Exception as e:
        print("Erreur lors de la création de 'paniers' :", e)

    # Création de la table commandes
    try:
        cur.execute("""
            CREATE TABLE commandes (
                commande_id INT PRIMARY KEY AUTO_INCREMENT,
                numero_commande VARCHAR(255) NOT NULL UNIQUE,
                commande_date DATE NOT NULL,
                revendeur_id INT NOT NULL,
                panier_id INT NOT NULL,
                FOREIGN KEY (revendeur_id) REFERENCES revendeurs(revendeur_id),
                FOREIGN KEY (panier_id) REFERENCES paniers(panier_id)
            );
        """)
        print("6/7 Table 'commandes' créée avec succès.")
    except Exception as e:
        print("Erreur lors de la création de 'commandes' :", e)

    # Création de la table commandes_produits
    try:
        cur.execute("""
            CREATE TABLE commandes_produits (
                commande_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL,
                unit_price DECIMAL (10,2) NOT NULL,
                total_ligne DECIMAL (10,2) NOT NULL,
                FOREIGN KEY (commande_id) REFERENCES commandes(commande_id),
                FOREIGN KEY (product_id) REFERENCES produits(product_id)
            );
        """)
        print("7/7 Table 'commandes_produits' créée avec succès.")
    except Exception as e:
        print("Erreur lors de la création de 'commandes_produits' :", e)
    # On charge les donnees
    #On commit et on ferme tout
    conn.commit()
    conn.close()
    print("Fermeture.")

if __name__ == "__main__":
    create_db()
