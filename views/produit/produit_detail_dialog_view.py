from PySide6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QWidget
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from models.produit import Produit
from core.my_hr import MyHr

import qtawesome as qta
import core.utils as Utils

class ProduitDetailDialogView(QDialog):

    def __init__(self, produit: Produit):
        super().__init__()

        self.setWindowTitle("Fiche Produit")
        self.setMinimumWidth(600)
        layout_self = QVBoxLayout(self)

        widget_main = QWidget()
        widget_main.setProperty("class", "bordered")
        layout_self.addWidget(widget_main)

        layout_main = QVBoxLayout(widget_main)
        # ===== TITRE =====
        title = QLabel("FICHE PRODUIT")
        title.setAlignment(Qt.AlignCenter)
        title.setProperty("class","titre2")
        # title.setStyleSheet("font-size:18px; font-weight:bold;")
        layout_main.addWidget(title)
        layout_main.addWidget(MyHr())

        # ===== CONTENU =====
        layout_content = QHBoxLayout()

        # ===== PHOTO =====
        photo_label = QLabel()
        photo_label.setAlignment(Qt.AlignCenter)
        photo_label.setFixedSize(250, 250)
        photo_label.setProperty("class","bordered")
        # photo_label.setStyleSheet("border:1px solid #ccc;")

        if produit.photo_path:
            pixmap = QPixmap(produit.photo_path)
            photo_label.setPixmap(
                pixmap.scaled(
                    240,
                    240,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )
        else:
            photo_label.setText("Aucune photo")

        layout_content.addWidget(photo_label)

        # ===== INFOS =====
        grid = QGridLayout()
        grid.setSpacing(5)

        label_reference=QLabel("Référence :")
        label_reference.setProperty("class","titre4")
        grid.addWidget(label_reference, 0, 0)
        text_reference=QLabel(produit.reference)
        text_reference.setProperty("class","fields")
        grid.addWidget(text_reference, 0, 1)

        label_designation=QLabel("Désignation : ")
        label_designation.setProperty("class","titre4")
        grid.addWidget(label_designation, 1, 0)
        text_designation=QLabel(produit.designation)
        text_designation.setWordWrap(True)
        label_designation.setMinimumHeight(40)
        text_designation.setProperty("class","fields")
        grid.addWidget(text_designation, 1, 1)

        label_categorie=QLabel("Catégorie : ")
        label_categorie.setProperty("class","titre4")
        grid.addWidget(label_categorie, 2, 0)
        text_categorie=QLabel(produit.categorie_nom)
        text_categorie.setProperty("class","fields")
        grid.addWidget(text_categorie, 2, 1)

        # ===== STOCK BADGE =====
        label_stock=QLabel("Stock :")
        label_stock.setProperty("class","titre4")
        grid.addWidget(label_stock, 3, 0)
        text_stock = QLabel(str(produit.stock))
        text_stock.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        if produit.stock <= produit.seuil_alerte:
            text_stock.setProperty("class","fields-red align_right")
        else:
            text_stock.setProperty("class","fields-green align_right")
        grid.addWidget(text_stock, 3, 1)

        label_seuil=QLabel("Seuil :")
        label_seuil.setProperty("class","titre4")
        grid.addWidget(label_seuil, 4, 0)
        text_seuil=QLabel(str(produit.seuil_alerte))
        text_seuil.setProperty("class","fields align_right")
        text_seuil.setAlignment(Qt.AlignRight)
        grid.addWidget(text_seuil, 4, 1)
        
        label_achat=QLabel("Prix d'achat :")
        label_achat.setProperty("class","titre4")
        grid.addWidget(label_achat, 5, 0)   
        text_prix_achat = QLabel(f"{Utils.Utils.format_prix(produit.prix_achat)} DA")
        text_prix_achat.setProperty("class","fields align_right")
        text_prix_achat.setAlignment(Qt.AlignRight)
        grid.addWidget(text_prix_achat, 5, 1)

        label_vente=QLabel("Prix de vente :")
        label_vente.setProperty("class","titre4")
        grid.addWidget(label_vente, 6, 0)
        text_prix_vente = QLabel(f"{Utils.Utils.format_prix(produit.prix_vente)} DA")
        text_prix_vente.setProperty("class","fields align_right")
        text_prix_vente.setAlignment(Qt.AlignRight)
        grid.addWidget(text_prix_vente, 6, 1)

        label_actif=QLabel("Actif :")
        label_actif.setProperty("class","titre4")
        grid.addWidget(label_actif, 7, 0)
        text_seuil=QLabel("Oui" if produit.actif else "Non")
        text_seuil.setProperty("class","fields")
        grid.addWidget(text_seuil, 7, 1)

        grid.setColumnStretch(1,1)

        info_widget = QWidget()
        info_widget.setLayout(grid)

        layout_content.addWidget(info_widget)

        layout_main.addLayout(layout_content)

        # ===== BOUTON =====
        btn_close = QPushButton("Fermer")
        btn_close.setIcon(qta.icon("fa5s.times",color="white"))
        btn_close.setProperty("type","default")
        btn_close.clicked.connect(self.accept)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_close)

        # # ===== HR (Ligne de séparation) =====
        # hr = QWidget()
        # hr.setFixedHeight(1)
        # hr.setStyleSheet("background-color: #e0e0e0;")

        # # Utiliser un layout pour appliquer les marges autour du hr
        # hr_container = QVBoxLayout()
        # hr_container.setContentsMargins(0, 30, 0, 16)
        # hr_container.addWidget(hr)

        # hr_widget = QWidget()
        # hr_widget.setLayout(hr_container)

        # layout_main.addWidget(hr_widget)
        
        layout_main.addWidget(MyHr())
        
        layout_main.addLayout(btn_layout)