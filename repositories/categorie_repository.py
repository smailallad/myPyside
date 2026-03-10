from core.database import get_connection

class CategorieRepository:
    def get_list_all_categories(self):
        cnx, cursor = get_connection()
        cursor.execute("SELECT id, nom FROM categories order by nom")
        rows = cursor.fetchall()
        categories = [dict(row) for row in rows]
        cursor.close()
        cnx.close()
        return categories