
import re
from PySide6.QtCore import Qt, Signal

from PySide6.QtWidgets import (
    QCheckBox, QDialog, QFileDialog, QFormLayout, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit,
    QComboBox, QSpinBox, QWidget
)
import qtawesome as qta
from PySide6.QtGui import QPixmap

from models.produit import Produit

class ProduitAddView(QDialog):
    # save_requested = Signal(dict)
    def __init__(self,produit: Produit | None = None,categories=None):
        super().__init__()

        self.setWindowTitle("Ajouter un produit" if not produit else "Modifier le produit")
        self.setModal(True)
        self.setMinimumWidth(1000)
        
        widget_form = QWidget()
        widget_form.setProperty("class", "bordered")

        layout_form = QFormLayout(widget_form)

        self.reference_produit = QLineEdit(text=produit.reference if produit else "")
        layout_form.addRow("Référence :", self.reference_produit)

        self.designation_produit = QLineEdit(text=produit.designation if produit else "")
        layout_form.addRow("Désignation :", self.designation_produit)

        self.categorie_produit = QComboBox()
        layout_form.addRow("Catégorie :", self.categorie_produit)
        if categories:
            for cat in categories:
                self.categorie_produit.addItem(cat["nom"], cat["id"])

        if produit:
                index = self.categorie_produit.findData(produit.categorie_id)
                if index >= 0:
                    self.categorie_produit.setCurrentIndex(index)        

        self.seuil_alerte_produit = QSpinBox(value=produit.seuil_alerte if produit else 0)
        layout_form.addRow("Seuil d'alerte :", self.seuil_alerte_produit)
        if produit:
            self.actif =QCheckBox()
            self.actif.setChecked(True if produit.actif else False)
            layout_form.addRow("Actif :",self.actif)

        self.photo_path =produit.photo_path if produit and produit.photo_path else None
        
        widget_photo = QWidget()
        widget_photo.setProperty("class","bordered")
        widget_photo.setFixedWidth(220)
        layout_photo = QVBoxLayout(widget_photo)

        self.photo_preview = QLabel("Aucune photo sélectionnée")
        self.photo_preview.setAlignment(Qt.AlignCenter)
        self.photo_preview.setFixedSize(200,200)
        
        layout_photo.addWidget(self.photo_preview)

        layout_photo.addStretch()

        widget_btn = QWidget()
        widget_btn.setProperty("class", "bordered")

        layout_btn = QVBoxLayout(widget_btn)
        
        self.btn_add_photo = QPushButton("Ajouter une photo")
        self.btn_add_photo.setAttribute(Qt.WA_StyledBackground, True)
        self.btn_add_photo.setIcon(qta.icon("fa5s.plus", color='white', color_active='white', color_disabled='gray'))
        self.btn_add_photo.setProperty("type","success")

        self.btn_delete_photo = QPushButton("Supprimer la photo")
        self.btn_delete_photo.setAttribute(Qt.WA_StyledBackground, True)
        self.btn_delete_photo.setIcon(qta.icon("fa5s.minus", color='white', color_active='white', color_disabled='gray'))
        self.btn_delete_photo.setProperty("type","danger")

        self.btn_save = QPushButton("Enregistrer")
        self.btn_save.setProperty("type","primary")

        self.btn_cancel = QPushButton("Annuler")
        self.btn_cancel.setProperty("type","default")

        layout_btn.addWidget(self.btn_add_photo)
        layout_btn.addWidget(self.btn_delete_photo)
        layout_btn.addStretch()
        layout_btn.addWidget(self.btn_save)
        layout_btn.addWidget(self.btn_cancel)
        
        self.layout = QHBoxLayout()

        self.layout.addWidget(widget_form, stretch=1) # Le formulaire s'étire
        self.layout.addWidget(widget_photo, stretch=0) # La photo reste à 200px
        self.layout.addWidget(widget_btn, stretch=0) # Les boutons restent serrés

        self.setLayout(self.layout)

        self.btn_add_photo.clicked.connect(self.choisir_photo)
        self.btn_delete_photo.clicked.connect(self.delete_photo)

        self.preview_photo(self.photo_path)

    def choisir_photo(self, event):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir une photo",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        self.preview_photo(file_path)
        
    def preview_photo(self,file_path):
        if file_path:
            pixmap = QPixmap(file_path)

            pixmap = pixmap.scaled(
                self.photo_preview.width(),
                self.photo_preview.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.photo_preview.setPixmap(pixmap)

            self.photo_path = file_path

    def delete_photo(self):
        self.photo_preview.clear()
        self.photo_preview.setText("Aucune photo sélectionnée")
        self.photo_path = None 
    
    # Dans views/produit/produit_add_view.py

    def highlight_error(self, field_name):
        # On remet tous les styles par défaut d'abord
        self.reference_produit.setStyleSheet("")
        self.designation_produit.setStyleSheet("")
        
        # On colore le champ concerné
        if field_name == "reference":
            self.reference_produit.setStyleSheet("border: 1px solid red;")
            self.reference_produit.setFocus()
        elif field_name == "designation":
            self.designation_produit.setStyleSheet("border: 1px solid red;")
            self.designation_produit.setFocus()
