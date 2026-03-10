class Produit:
    def __init__(
            self, id=None, 
            reference="", 
            designation="",
            categorie_id=None, 
            prix_achat=0,
            prix_vente=0, 
            stock=0,
            seuil_alerte=0, 
            actif=True,
            photo_path=None,
            created_at=None
            ):
        
        self.id = id
        self.reference = reference
        self.designation = designation
        self.categorie_id = categorie_id
        self.prix_achat = prix_achat
        self.prix_vente = prix_vente
        self.stock = stock
        self.seuil_alerte = seuil_alerte
        self.actif = actif
        self.photo_path = photo_path
        self.created_at = created_at 