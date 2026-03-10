from core.database import get_connection

def create_tables():

    cnx, cursor = get_connection()

    # table catégories
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            nom VARCHAR(100) UNIQUE NOT NULL COLLATE NOCASE
        )
    """)

    # table produits
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produits (
            id INTEGER PRIMARY KEY,
            reference VARCHAR(50) NOT NULL UNIQUE COLLATE NOCASE,
            designation VARCHAR(150) NOT NULL,
            categorie_id INTEGER NOT NULL,
            prix_achat DECIMAL(10,2) NOT NULL DEFAULT 0,
            prix_vente DECIMAL(10,2) NOT NULL DEFAULT 0,
            stock INTEGER DEFAULT 0 NOT NULL,
            seuil_alerte INTEGER DEFAULT 5 NOT NULL,
            actif BOOLEAN DEFAULT TRUE NOT NULL,
            photo_path VARCHAR(50),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (categorie_id) REFERENCES categories(id)
        )
    """)

    #table vehicules
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicules (
            id INTEGER PRIMARY KEY,
            nom VARCHAR(100) UNIQUE NOT NULL COLLATE NOCASE,
            annee INTEGER NOT NULL
        )
    """)

    #table produit_vehicules
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produit_vehicules (
            id INTEGER PRIMARY KEY,
            produit_id INTEGER,
            vehicule_id INTEGER,
            FOREIGN KEY (produit_id) REFERENCES produits(id),
            FOREIGN KEY (vehicule_id) REFERENCES vehicules(id)
        )
    """)

    cnx.commit()
    cnx.close()