from models.produit import Produit
from models.produit_table_model import ProduitTableModel
from views.produit.produit_add_view import ProduitAddView
from PySide6.QtWidgets import QHeaderView, QMessageBox, QTableWidgetItem
from PySide6.QtCore import QTimer, Slot
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PIL import Image

import os
# import shutil
import core.utils as utils
import core.config as config
from views.produit.produit_detail_dialog_view import ProduitDetailDialogView

class ProduitController():

    def __init__(self, view,container,router):
        super().__init__()   # obligatoire pour QObject
        self.view = view
        self.model = ProduitTableModel([])
        self.view.table.setModel(self.model)
        self.view.table.setSortingEnabled(True)

        self.page=0
        self.limit=5
        self.total_pages=0
        self.total_rows=0
        self.order_by = "id"
        self.order = "ASC"
        
        self.produits: list[Produit] = []  # <-- liste de Produits
        # self.search_value="" # stocker le terme de recherche actuel
        self.pixmap_cache = {} # cache mémoire

        self.produit_service = container.resolve(config.Services.PRODUIT)
        self.categorie_service = container.resolve(config.Services.CATEGORIE)

        self.categories = self.categorie_service.liste_tout_categories()
        self.load_categories()

        self.view.combo_stock.addItem("Touts les produits", None)
        self.view.combo_stock.addItem("En repture de stock", True)

        self.view.combo_actif.addItem("Touts les produits", None)
        self.view.combo_actif.addItem("Les produits actif", True)
        self.view.combo_actif.addItem("Les produits non actif", False)

        # ----- Timer pour recherche automatique -----
        self.search_timer = QTimer()
        self.search_timer.setInterval(400)       # 400 ms après la frappe
        self.search_timer.setSingleShot(True)    # déclenche une seule fois
        self.view.search_input.textChanged.connect(self.search_timer.start)
        self.search_timer.timeout.connect(lambda: self.load_produits(reset_page=True))

        # Connecter les signaux
        self._connect_signals()

        # Initial load
        self.load_produits(reset_page=True)

        # Désactiver les boutons de modification et de suppression au démarrage
        self.view.btn_edit.setEnabled(False)
        self.view.btn_delete.setEnabled(False)

    def _connect_signals(self):
        self.view.btn_add.clicked.connect(self.add_produit)
        self.view.btn_edit.clicked.connect(self.update_produit)
        self.view.btn_delete.clicked.connect(self.delete_produit)
        self.view.btn_detail.clicked.connect(self.detail_produit)
        self.view.table.selectionModel().selectionChanged.connect(self.table_changer)
        self.view.table.doubleClicked.connect(lambda _: self.detail_produit())
        self.view.table.horizontalHeader().sortIndicatorChanged.connect(self.on_sort_changed)
        self.view.search_input.returnPressed.connect(lambda: self.load_produits(reset_page=True))
        self.view.combo_stock.currentIndexChanged.connect(lambda:self.load_produits(reset_page=True))
        self.view.combo_actif.currentIndexChanged.connect(lambda:self.load_produits(reset_page=True))
        self.view.combo_categorie.currentIndexChanged.connect(lambda:self.load_produits(reset_page=True))
        self.view.btn_reset_filters.clicked.connect(self.reset_filters)

        self.view.btn_first.clicked.connect(self.first_page)
        self.view.btn_prev.clicked.connect(self.prev_page)
        self.view.btn_next.clicked.connect(self.next_page)
        self.view.btn_last.clicked.connect(self.last_page)

    def apply_filter(self, status=None):
        self.view.combo_categorie.blockSignals(True)
        self.view.combo_stock.blockSignals(True)
        self.view.combo_actif.blockSignals(True)

        self.view.combo_categorie.setCurrentIndex(0)
        self.view.combo_actif.setCurrentIndex(0)
        self.view.combo_stock.setCurrentIndex(0)
        match status:
            case "actif":
                self.view.combo_actif.setCurrentIndex(1)
            case "non_actif":
                self.view.combo_actif.setCurrentIndex(2)
            case "alerte":
                self.view.combo_actif.setCurrentIndex(1)
                self.view.combo_stock.setCurrentIndex(1)
        self.load_produits(True)

        self.view.combo_categorie.blockSignals(False)
        self.view.combo_stock.blockSignals(False)
        self.view.combo_actif.blockSignals(False)

    def on_sort_changed(self, column, order):

        column_map = {
            0: "id",
            1: "reference",
            2: "designation",
            3: "prix_vente",
            4: "stock",
        }

        self.order_by = column_map.get(column, "id")
        self.order = "ASC" if order == Qt.AscendingOrder else "DESC"

        self.load_produits(reset_page=True)

    def get_produit_data(self,dialog):
        produit = {
            "reference": dialog.reference_produit.text(),
            "designation": dialog.designation_produit.text(),
            "categorie_id": dialog.categorie_produit.currentData(),
            "seuil_alerte": dialog.seuil_alerte_produit.value(),
            "photo_path": dialog.photo_path
        }
        
        # On ajoute 'actif' seulement si le widget existe dans le dialogue (cas edit)
        if hasattr(dialog, 'actif'):
            produit["actif"] = dialog.actif.isChecked()
        
        return produit
    
    def on_save(self, dialog, produit):
        # --- ÉTAPE DE VALIDATION ---
        is_valid, field_name,error_message = self.validate_produit_data(produit)
        
        if not is_valid:
            dialog.highlight_error(field_name)
            QMessageBox.warning(dialog, "Données invalides", error_message)
            return  # On sort de la fonction, le dialogue reste ouvert pour correction

        # --- ÉTAPE D'INSERTION (si valide) ---
        produit_id = None
        result, message = self.produit_service.add_produit(produit)
        if not result:
           
            QMessageBox.warning(dialog, "Erreur", message)
            return   # ❌ la fenêtre reste ouverte
        
        # on varifier si une photo a été sélectionnée et l'associer au produit après l'insertion
        # Copier la photo dans le dossier local 
        # et mettre à jour le chemin dans la base de données
        produit_id = message  # message contient l'ID retourné par add_produit
        if dialog.photo_path:
            try:
                self.upload_photo(produit_id, dialog.photo_path)
            except RuntimeError as e:
                QMessageBox.warning(dialog, "Erreur", str(e))
                return
        
        dialog.accept()   # ✅ ferme seulement si succès
        self.load_produits(reset_page=True)

    def on_update(self, dialog, produit_id, produit):
        # --- ÉTAPE DE VALIDATION ---
        is_valid, field_name,error_message = self.validate_produit_data(produit)
        
        if not is_valid:
            dialog.highlight_error(field_name)
            QMessageBox.warning(dialog, "Données invalides", error_message)
            return  # On sort de la fonction, le dialogue reste ouvert pour correction

        # --- ÉTAPE D'INSERTION (si valide) ---
        result, message = self.produit_service.update_produit(produit_id,produit)
        if not result:
            QMessageBox.warning(dialog, "Erreur", message)
            return   # ❌ la fenêtre reste ouverte
        
        if dialog.photo_path:
            try:
                self.upload_photo(produit_id, dialog.photo_path)
            except RuntimeError as e:
                QMessageBox.warning(dialog, "Erreur", str(e))
                return
        
        dialog.accept()   # ✅ ferme seulement si succès
        self.load_produits(reset_page=True)

    def upload_photo(self, produit_id: int, photo_path: str):
        try:
            dest_folder = utils.Utils.dir_folder_photos_produits()
            filename = f"produit_{str(produit_id).zfill(5)}.jpg"
            dest_path = os.path.join(dest_folder, filename)
            img = Image.open(photo_path)
            # convertir si PNG ou autre
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            # redimensionner max 600x600
            img.thumbnail((600, 600))
            # sauvegarder optimisé
            img.save(dest_path, "JPEG", quality=80, optimize=True)
            self.produit_service.update_photo_produit(produit_id, dest_path)
        except Exception as e:
            raise RuntimeError(f"La photo n'a pas pu être enregistrée: {e}")
        #==
    
    def find_produit(self, produit_id):
        return self.produits.get(produit_id)
    
    def preview_photo(self, file_path):
        if not file_path:
            self.view.photo_preview.clear()
            self.view.photo_preview.setText("Aucune photo.")
            return

        if not os.path.isfile(file_path):
            self.view.photo_preview.clear()
            self.view.photo_preview.setText("Photo supprimée physiquement.")
            return

        if file_path not in self.pixmap_cache:
            self.pixmap_cache[file_path] = QPixmap(file_path)

        pixmap = self.pixmap_cache[file_path]

        pixmap = pixmap.scaled(
            self.view.photo_preview.width(),
            self.view.photo_preview.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.view.photo_preview.setPixmap(pixmap)

    def get_selected_id(self):
        index = self.view.table.currentIndex()
        if not index.isValid():
            return None
        row = index.row()
        produit = self.model.produits[row]
        return produit.id

    def load_produits(self,reset_page=False):
        if reset_page:
            self.page=1

        search_value = self.view.search_input.text()
        categorie =self.view.combo_categorie.currentData()
        stock=self.view.combo_stock.currentData()
        actif=self.view.combo_actif.currentData()
        produits=[]
        result = self.produit_service.get_produits(search_value = search_value,categorie=categorie,actif=actif,stock=stock,order_by=self.order_by,order=self.order,page=self.page,limit=self.limit)
        if result["success"]:
            produits = result["produit"]
            self.page=result["page"]
            self.total_pages=result["total_pages"]
            self.total_rows = result["total_rows"]
            self.produits = {p.id: p for p in produits}
        else:
            self.page=0
            self.total_pages=0
            self.total_rows = 0
            QMessageBox.warning(self.view, "Erreur", result["message"])
        self.view.label_count.setText("Total produits : "+str(self.total_rows)) 
        self.view.label_page.setText("Page" + str(self.page)+"/"+str(self.total_pages))
        self.model.setProduits(produits)
        
        header = self.view.table.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Référence
        header.setSectionResizeMode(2, QHeaderView.Stretch)           # Désignation
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Categorie
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Stock
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Prix vente

        self.update_navigation()
        self.table_changer()

    def load_categories(self):
        self.view.combo_categorie.addItem("Toutes les categories", None)
        if self.categories:
            for cat in self.categories:
                self.view.combo_categorie.addItem(cat["nom"], cat["id"])

        # if produit:
        #         index = self.categorie_produit.findData(produit.categorie_id)
        #         if index >= 0:
        #             self.view.categorie_produit.setCurrentIndex(index)  

    def update_navigation(self):
        has_pages = self.total_pages > 1
        is_not_first = self.page > 1
        is_not_last = self.page < self.total_pages

        self.view.btn_first.setEnabled(has_pages and is_not_first)
        self.view.btn_prev.setEnabled(has_pages and is_not_first)
        self.view.btn_next.setEnabled(has_pages and is_not_last)
        self.view.btn_last.setEnabled(has_pages and is_not_last)

        # if self.page<=1:
        #     if self.total_pages<=1:
        #         self.view.btn_first.setEnabled(False)
        #         self.view.btn_prev.setEnabled(False)
        #         self.view.btn_next.setEnabled(False)
        #         self.view.btn_last.setEnabled(False)
        #     else:
        #         self.view.btn_first.setEnabled(False)
        #         self.view.btn_prev.setEnabled(False)
        #         self.view.btn_next.setEnabled(True)
        #         self.view.btn_last.setEnabled(True)
        # else:
        #     self.view.btn_first.setEnabled(True)
        #     self.view.btn_prev.setEnabled(True)
        #     if self.page==self.total_pages:
        #         self.view.btn_next.setEnabled(False)
        #         self.view.btn_last.setEnabled(False)
        #     else:
        #         self.view.btn_next.setEnabled(True)
        #         self.view.btn_last.setEnabled(True)
    
    def validate_produit_data(self, data):
        # 1. Vérification des champs obligatoires
        if not data.get("reference") or len(data["reference"].strip()) < 3:
            return False,"reference", "La référence doit contenir au moins 3 caractères."
        
        if not data.get("designation") or len(data["designation"].strip()) < 3:
            return False,"designation", "La désignation doit contenir au moins 3 caractères."

        # 2. Vérification de la catégorie
        if data.get("categorie_id") is None:
            return False,"categorie_id", "Veuillez sélectionner une catégorie."

        # 3. Logique métier (ex: seuil d'alerte positif)
        if data.get("seuil_alerte", 0) < 0:
            return False,"seuil_alerte", "Le seuil d'alerte ne peut pas être négatif."

        return True, None, None
    
    @Slot()
    def first_page(self):
        if self.page != 1:
            self.page=1
            self.load_produits()

    @Slot()
    def prev_page(self):
        if self.page>1:
            self.page=self.page-1
            self.load_produits()

    @Slot()
    def next_page(self):
        if self.page<self.total_pages:
            self.page=self.page+1
            self.load_produits()

    @Slot()
    def last_page(self):
        if self.page<self.total_pages:
            self.page=self.total_pages
            self.load_produits()

    @Slot()
    def add_produit(self):        
        dialog = ProduitAddView(categories=self.categories)
        dialog.btn_save.clicked.connect(
            lambda: self.on_save(dialog, self.get_produit_data(dialog))
        )
        dialog.btn_cancel.clicked.connect(dialog.reject)
        dialog.exec()

    @Slot()
    def update_produit(self):
        id = self.get_selected_id()  # Supposons que l'ID est dans la première colonne
        produit= self.find_produit(int(id))
        # categories = self.categorie_service.liste_tout_categories()
        dialog=ProduitAddView(produit,self.categories)
        dialog.btn_save.clicked.connect(
            lambda: self.on_update(dialog, id, self.get_produit_data(dialog))
        )
        dialog.btn_cancel.clicked.connect(dialog.reject)
        dialog.exec()
        self.load_produits(reset_page=True)

    @Slot()
    def detail_produit(self):
        id = self.get_selected_id()  # Supposons que l'ID est dans la première colonne
        produit= self.find_produit(int(id))
        # categories = self.categorie_service.liste_tout_categories()
        dialog=ProduitDetailDialogView(produit)
        dialog.exec()
        
    @Slot()
    def delete_produit(self):
        id = self.get_selected_id() # Supposons que l'ID est dans la première colonne
        confirm = QMessageBox.question(self.view, "Confirmer", f"Êtes-vous sûr de vouloir supprimer le produit ID {id} ?")
        if confirm == QMessageBox.Yes:
            result, message = self.produit_service.delete_produit(int(id))
            if not result:
                QMessageBox.warning(self.view, "Erreur", message)
                return
        self.load_produits(reset_page=True)  

    @Slot()
    def table_changer(self):
        id = self.get_selected_id()
        if id:
            self.view.btn_detail.setEnabled(True)
            self.view.btn_edit.setEnabled(True)
            self.view.btn_delete.setEnabled(True)
            produit= self.find_produit(int(id))
            if produit:
                photo_path=produit.photo_path
                self.preview_photo(photo_path)
            else:
                self.preview_photo(None)
        else:
            self.view.btn_detail.setEnabled(False)
            self.view.btn_edit.setEnabled(False)
            self.view.btn_delete.setEnabled(False)
            self.preview_photo(None)

    @Slot()
    def reset_filters(self):
        # 1. Bloquer les signaux pour éviter le "begaiement" de requêtes SQL
        self.view.search_input.blockSignals(True)
        self.view.combo_stock.blockSignals(True)
        self.view.combo_actif.blockSignals(True)
        self.view.combo_categorie.blockSignals(True)

        # 2. Remettre les valeurs par défaut
        self.view.search_input.clear()
        self.view.combo_stock.setCurrentIndex(0)
        self.view.combo_actif.setCurrentIndex(0)
        self.view.combo_categorie.setCurrentIndex(0)

        # 3. Débloquer les signaux
        self.view.search_input.blockSignals(False)
        self.view.combo_stock.blockSignals(False)
        self.view.combo_actif.blockSignals(False)
        self.view.combo_categorie.blockSignals(False)

        # 4. Lancer une seule charge de données propre
        self.load_produits(reset_page=True)