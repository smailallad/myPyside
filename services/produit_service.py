import math

class ProduitService:

    def __init__(self, repository):
        self.repository = repository
     
    def add_produit(self, produit):
        return self.repository.add_produit(produit=produit)

    def get_produits(self,search_value="",categorie=None,actif=None,stock=None,order_by="id",order="ASC",page=1,limit=100):
        
        try:
            page = max(1, int(page))
            limit = max(1, int(limit))

            # total_rows =self.repository.count_produits(search_value) # ajouter categorie
            offset = (page - 1) * limit
            total_rows, produits = self.repository.get_produits(search_value=search_value,categorie=categorie,actif=actif,stock=stock,order_by=order_by,order=order,offset=offset,limit=limit)
            total_pages = math.ceil(total_rows / limit)
            if total_pages<=0:
                total_pages=1

            return {
                "success": True,
                "produit": produits,
                "page": page,
                "total_pages": total_pages,
                "total_rows": total_rows
            }

        except Exception as e:
            print("Error in get_produits:", e)
            return {
                "success": False,
                "message": str(e)
            }
        #   return get_produits(search_value)

    def get_produit_by_id(self,id):
        return self.repository.get_produit_by_id(id)

    def update_produit(self,id, produit):
        return self.repository.update_produit(id, produit)

    def delete_produit(self,id):
        return self.repository.delete_produit(id)

    def update_photo_produit(self,id,photo_path):
        return self.repository.update_photo_produit(id=id,photo_path=photo_path)

    def delete_photo_produit(self,id):
        return self.repository.delete_photo_produit(id=id)