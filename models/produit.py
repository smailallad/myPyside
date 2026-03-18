from dataclasses import dataclass

@dataclass
class Produit:
    id: int | None = None
    reference: str = ""
    designation: str = ""
    categorie_id: int | None = None
    categorie_nom: str | None = None
    prix_achat: float = 0
    prix_vente: float = 0
    stock: int = 0
    seuil_alerte: int = 0
    actif: bool = True
    photo_path: str | None = None
    created_at: str | None = None
    adapter: str | None = None