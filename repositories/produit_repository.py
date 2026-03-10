import os
import sqlite3

from core.database import get_connection
from models.produit import Produit

class ProduitRepository:
    def add_produit(self, produit):
        cnx, cursor = get_connection()
        try:
            # fields = list(produit.keys())
            # values = list(produit.values())
            fields = []
            values = []

            for k, v in produit.items():
                if k == "reference" and isinstance(v, str):
                    v = v.upper()
                fields.append(k)
                values.append(v)

            placeholders = ", ".join(["?"] * len(fields))
            columns = ", ".join(fields)

            sql = f"""
            INSERT INTO produits ({columns})
            VALUES ({placeholders})
            """
            
            cursor.execute(sql, values)
            cnx.commit()
            # Récupérer l'ID du produit inséré
            produit_id = cursor.lastrowid
            return True, produit_id

        except sqlite3.IntegrityError as e:
            # Erreurs de contraintes (UNIQUE, NOT NULL, FOREIGN KEY…)
            if "UNIQUE" in str(e):
                return False, "Ce produit existe déjà"
            elif "NOT NULL" in str(e):
                return False, "Un champ obligatoire est manquant"
            else:
                return False, f"Erreur d'intégrité : {e}"

        except sqlite3.Error as e:
            # Autres erreurs SQLite
            print(e)
            return False, f"Erreur base de données : {e}"

        finally:
            cursor.close()
            cnx.close()

    def get_produits(self, search_value="",order_by="id",order="ASC",offset=0,limit=100):
        if order_by not in ["id", "reference", "designation", "categorie", "prix_achat", "prix_vente", "stock", "seuil_alerte", "actif",]:
            order_by = "categories.id"

        if order_by== "id":
            order_by="produits.id"

        if order_by=="categorie":
            order_by="categories.nom"

        if order.upper() not in ["ASC", "DESC"]:
            order = "ASC"

        cnx, cursor = get_connection()
        # sql= """ SELECT produits.id,reference,designation,categorie_id,categories.nom as categorie_nom,prix_achat,prix_vente,stock,seuil_alerte,actif,created_at,photo_path
        #          FROM produits
        #          INNER JOIN categories ON produits.categorie_id=categories.id
        #     """
        sql="""
                SELECT
                produits.id,
                produits.reference,
                produits.designation,
                produits.prix_achat,
                produits.prix_vente,
                produits.stock,
                produits.seuil_alerte,
                produits.actif,
                produits.photo_path,
                categories.nom as categorie_nom,
                categories.id as categorie_id,
                GROUP_CONCAT(vehicules.nom || ' annee ' || vehicules.annee || ' ')  AS adapter
            FROM produits
            LEFT JOIN categories ON produits.categorie_id = categories.id
            LEFT JOIN produit_vehicules  ON produits.id = produit_vehicules.produit_id
            LEFT JOIN vehicules ON produit_vehicules.vehicule_id = vehicules.id
            """
        params=[]

        if search_value:
            sql+=" WHERE produits.id = ? OR produits.reference LIKE ? OR produits.designation LIKE ? OR categories.nom LIKE ? OR vehicules.nom LIKE ? "
            params.append(search_value)
            params.append(f"%{search_value}%")
            params.append(f"%{search_value}%")
            params.append(f"%{search_value}%")
            params.append(f"%{search_value}%")

        sql += f" GROUP BY produits.id, produits.reference, produits.designation, produits.prix_achat, produits.prix_vente, produits.stock, produits.seuil_alerte, produits.actif,produits.photo_path"
        sql += f" ORDER BY {order_by} {order} LIMIT ? OFFSET ?"
        params.extend([limit,offset])
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        produits = [dict(row) for row in rows]
        # produits = [Produit(**p) for p in rows]
        cursor.close()
        cnx.close()
        return produits

    def count_produits(self,search_value=""):
        cnx, cursor = get_connection()

        sql = "SELECT COUNT(*) FROM produits INNER JOIN categories ON produits.categorie_id=categories.id"
        params = []

        if search_value:
            sql += " WHERE produits.id= ? OR produits.reference LIKE ? OR produits.designation LIKE ?"
            params.append(search_value)
            params.append(f"%{search_value}%")
            params.append(f"%{search_value}%")

        cursor.execute(sql, params)
        total = cursor.fetchone()[0]

        cursor.close()
        cnx.close()
        return total

    def get_produit_by_id(self,produit_id):
        cnx, cursor = get_connection()
        cursor.execute("""
            SELECT produits.id,reference,designation,categorie_id,categories.nom as categorie_nom,prix_achat,prix_vente,stock,seuil_alerte,actif,created_at,photo_path
            FROM produits INNER JOIN categories ON produits.categorie_id=categories.id
            WHERE produits.id = ?
        """,
            (produit_id,)
        )
        produit = cursor.fetchone()
        cursor.close()
        cnx.close()
        return produit

    def update_produit(self,id,produit):
        cnx, cursor = get_connection()
        try:
            fields = []
            values = []

            for k, v in produit.items():
                if k == "reference" and isinstance(v, str):
                    v = v.upper()
                fields.append(k+"=?")
                values.append(v)

            values.append(id)  # Ajouter l'ID à la fin pour la clause WHERE
            columns = ", ".join(fields)

            sql = f"""
            UPDATE produits SET {columns} WHERE id= ?
            """
      
            cursor.execute(sql, values)
        #     cursor.execute("""
        #                     UPDATE produits SET reference=?, designation = ? , categorie_id=?, prix_achat=?, prix_vente=?, stock=?, seuil_alerte=?, actif=?
        #                     WHERE id = ?
        #                 """,
        #     (produit["reference"].upper(), produit["designation"], produit["categorie_id"], produit["prix_achat"], produit["prix_vente"], produit["stock"], produit["seuil_alerte"], produit["actif"], id)
        # )
            cnx.commit()
            return True, None

        except sqlite3.IntegrityError as e:
            # Erreurs de contraintes (UNIQUE, NOT NULL, FOREIGN KEY…)
            if "UNIQUE" in str(e):
                return False, "Ce produit existe déjà"
            elif "NOT NULL" in str(e):
                return False, "Un champ obligatoire est manquant"
            else:
                return False, f"Erreur d'intégrité : {e}"

        except sqlite3.Error as e:
            # Autres erreurs SQLite
            return False, f"Erreur base de données : {e}"

        finally:
            cursor.close()
            cnx.close()

    def update_photo_produit(self,id,photo_path):
        cnx, cursor = get_connection()
        try:
            cursor.execute("""
                        SELECT photo_path
                        FROM produits
                        WHERE id = ?
                        """, (id,))
            produit = cursor.fetchone()
            path = produit["photo_path"]

            if path and os.path.isfile(path) and path!=photo_path:
                os.remove(path)

            cursor.execute("""
                            UPDATE produits SET photo_path=?
                            WHERE id = ?
                        """,
                            (photo_path,id)
            )
            cnx.commit()
            return True, None

        except Exception as e:
            return False, f"Erreur de sauvgarde de la photo : {e}"

        finally:
            cursor.close()
            cnx.close()
    
    def delete_photo_produit(self, id):
        cnx, cursor = get_connection()
        try:
            cursor.execute("""
                        SELECT photo_path
                        FROM produits
                        WHERE id = ?
                        """, (id,))
            produit = cursor.fetchone()
            path = produit["photo_path"]

            if path and os.path.isfile(path):
                os.remove(path)

            cursor.execute("""
                            UPDATE produits SET photo_path=NULL
                            WHERE id = ?
                        """,
                            (id,)
            )
            cnx.commit()
            return True, None

        except Exception as e:
            return False, f"Erreur de suppression de la photo : {e}"

        finally:
            cursor.close()
            cnx.close()

    def delete_produit(self,id):
        cnx, cursor = get_connection()
        try:
            cursor.execute(
                "DELETE FROM produits WHERE id = ?",
                (id,)
            )
            cnx.commit()
            return True, None
        except Exception as e:
            return False, f"Erreur lors de la suppression : {e}"
        finally:
            cursor.close()
            cnx.close()
