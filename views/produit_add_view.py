
from PySide6.QtCore import Qt, Signal
# from PySide6.QtWidgets import (QDialog,QVBoxLayout,QFormLayout,QLineEdit)
from PySide6.QtWidgets import (
    QCheckBox, QDialog, QFileDialog, QFormLayout, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit,
    QComboBox, QSpinBox, QDoubleSpinBox,
    QMessageBox, QWidget
)
from PySide6.QtGui import QPixmap
class ProduitAddView(QDialog):
    save_requested = Signal(dict)
    def __init__(self,produit=None,categories=None):
        super().__init__()
    
        self.setWindowTitle("Ajouter un produit" if not produit else "Modifier le produit")
        self.setModal(True)
        
        widget_form = QWidget()
        widget_form.setProperty("class", "bordered")

        layout_form = QFormLayout(widget_form)

        self.reference_produit = QLineEdit(text=produit["reference"] if produit else "")
        layout_form.addRow("Référence :", self.reference_produit)

        self.designation_produit = QLineEdit(text=produit["designation"] if produit else "")
        layout_form.addRow("Désignation :", self.designation_produit)

        self.categorie_produit = QComboBox()
        layout_form.addRow("Catégorie :", self.categorie_produit)
        if categories:
            for cat in categories:
                self.categorie_produit.addItem(cat["nom"], cat["id"])

        if produit:
                index = self.categorie_produit.findData(produit["categorie_id"])
                if index >= 0:
                    self.categorie_produit.setCurrentIndex(index)        

        self.seuil_alerte_produit = QSpinBox(value=produit["seuil_alerte"] if produit else 0)
        layout_form.addRow("Seuil d'alerte :", self.seuil_alerte_produit)

        widget_photo_container = QWidget()
        widget_photo_container.setProperty("class", "bordered")

        layout_photo = QVBoxLayout(widget_photo_container)
        layout_photo.addWidget(QLabel("Photo du produit:"))
        self.lbl_photo_preview= QLabel()
        self.btn_add_photo = QPushButton("Ajouter/Modifier la photo")
        self.btn_add_photo.setProperty("type","primary")

        widget_photo = QWidget()
        widget_photo.setFixedWidth(200)

        # layout_photo.addWidget(widget_photo)
        # layout_photo.addWidget(self.lbl_photo_preview)
        # layout_photo.addWidget(self.btn_add_photo)

        #===
        self.photo_label = QLabel("Cliquer pour ajouter une photo")
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setFixedSize(180,180)
        self.photo_label.setProperty("class", "bordered")

        layout_photo.addWidget(self.photo_label)

        self.photo_label.mousePressEvent = self.choisir_photo
        #===

        widget_btn = QWidget()
        widget_btn.setProperty("class", "bordered")

        layout_btn = QVBoxLayout(widget_btn)

        self.btn_save = QPushButton("Enregistrer")
        self.btn_save.setProperty("type","primary")
        self.btn_cancel = QPushButton("Annuler")
        self.btn_cancel.setProperty("type","default")

        layout_btn.addWidget(self.btn_save)
        layout_btn.addWidget(self.btn_cancel)

        self.layout = QHBoxLayout()

        self.layout.addWidget(widget_form)
        self.layout.addWidget(widget_photo_container)
        self.layout.addWidget(widget_btn)

        self.setLayout(self.layout)

        self.setLayout(self.layout)

    def choisir_photo(self, event):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir une photo",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if file_path:
            pixmap = QPixmap(file_path)

            pixmap = pixmap.scaled(
                self.photo_label.width(),
                self.photo_label.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.photo_label.setPixmap(pixmap)

            self.photo_path = file_path