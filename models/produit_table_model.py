from PySide6.QtCore import Qt, QAbstractTableModel
from PySide6.QtGui import QColor, QBrush, QPixmap, QIcon
from models.produit import Produit
import qtawesome as qta # Assure-toi que qtawesome est installé

import core.utils as utils

# Couleurs
COULEUR_FOND_ROUGE = "#FCC8C8" 
COULEUR_TEXTE_JAUNE = QColor(255, 255, 0)

class ProduitTableModel(QAbstractTableModel):

    def __init__(self, produits:list[Produit] | None = None):
        super().__init__()
        self.produits = produits or []
        self.headers = ["ID", "Référence", "Désignation", "Catégorie", "Stock", "Seuil", "Prix vente", "Actif"]
        
        # On prépare l'icône d'alerte une seule fois
        self.icon_alert = qta.icon("fa5s.exclamation-triangle", color="#D32F2F")

    def rowCount(self, parent=None):
        return len(self.produits)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role):
        if not index.isValid():
            return None
            
        produit = self.produits[index.row()]
        col = index.column()
        
        # Condition d'alerte stock
        is_alert = (produit.stock is not None and 
                    produit.seuil_alerte is not None and 
                    produit.stock <= produit.seuil_alerte)

        # 1. TEXTE (DisplayRole)
        if role == Qt.DisplayRole:
            if col == 0: return produit.id
            elif col == 1: return produit.reference
            elif col == 2: return produit.designation
            elif col == 3: return produit.categorie_nom
            elif col == 4: return produit.stock
            elif col == 5: return produit.seuil_alerte
            elif col == 6: return utils.Utils.format_prix(produit.prix_vente)
            elif col == 7: return "Oui" if produit.actif else "Non"

        # 2. ICÔNES (DecorationRole)
        if role == Qt.DecorationRole:
            # Photo du produit (Colonne ID)
            if col == 0 and produit.photo_path:
                pixmap = QPixmap(produit.photo_path)
                if not pixmap.isNull():
                    return pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # ICÔNE ALERTE (Colonne Stock)
            if col == 4 and is_alert:
                return self.icon_alert

        # 3. COULEURS (Background/Foreground)
        # if role in (Qt.BackgroundRole, Qt.ForegroundRole):
        #     if is_alert:
        #         if role == Qt.BackgroundRole:
        #             return QBrush(QColor(COULEUR_FOND_ROUGE))
        #         if role == Qt.ForegroundRole:
        #             return QBrush(COULEUR_TEXTE_JAUNE)

        # 4. ALIGNEMENT
        if role == Qt.TextAlignmentRole:
            if col in (0, 7): return Qt.AlignCenter
            if col in (4, 5, 6): return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignLeft | Qt.AlignVCenter

        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]

    def setProduits(self, produits):
        self.beginResetModel()
        self.produits = produits
        self.endResetModel()