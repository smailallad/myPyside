from core.form_dialog import FormDialog
from PySide6.QtCore import Signal

class ProduitAddView(FormDialog):
    save_requested = Signal(dict)
    def __init__(self,produit=None,categories=None):
        super().__init__("Ajouter produit")
        
        self.add_field("reference", "Référence",default_value=produit["reference"] if produit else "",min_length=3, max_length=50)
        self.add_field("designation", "Désignation",default_value=produit["designation"] if produit else "", min_length=2, max_length=100)
        self.add_field("prix_achat", "Prix d'achat", "float",default_value=produit["prix_achat"] if produit else 0 , min_value=0)
        self.add_field("prix_vente", "Prix de vente", "float", default_value=produit["prix_vente"] if produit else 0, min_value=0)
        # self.add_field("stock", "Stock", "int",default_value=produit["stock"] if produit else 0, min_value=0)
        self.add_field("categorie_id","Catégorie","combo",default_value=produit["categorie_id"] if produit else None,options=categories)       
        self.add_field("seuil_alerte", "Seuil d'alerte", "int", default_value=produit["seuil_alerte"] if produit else 0, min_value=0)
        self.add_field("actif", "Actif", "checkbox", default_value=produit["actif"] if produit else True,)

