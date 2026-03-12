from views.produit_add_view import ProduitAddView
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Slot
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

import os
import shutil
import core.utils as utils

class ProduitController():

    def __init__(self, view,container):
        super().__init__()   # obligatoire pour QObject
        self.view = view
        self.produits=[] # stocker les produits affichés dans la table
        self.search_value="" # stocker le terme de recherche actuel
        self.pixmap_cache = {} # cache mémoire

        self.produit_service = container.resolve("produit_service")
        self.categorie_service = container.resolve("categorie_service")

        # Connecter les signaux
        self._connect_signals()

        # Initial load
        self.refresh()

        # Désactiver les boutons de modification et de suppression au démarrage
        self.view.btn_edit.setEnabled(False)
        self.view.btn_delete.setEnabled(False)

    def _connect_signals(self):
        self.view.btn_add.clicked.connect(self.add_produit)
        self.view.btn_edit.clicked.connect(self.update_produit)
        self.view.btn_delete.clicked.connect(self.delete_produit)
        self.view.btn_search.clicked.connect(self.refresh)
        self.view.table.itemSelectionChanged.connect(self.table_changer)
        self.view.table.doubleClicked.connect(self.update_produit)
        self.view.search_input.returnPressed.connect(self.refresh)

    @Slot()
    def refresh(self):
        self.search_value = self.view.search_input.text()
        result = self.produit_service.get_produits(self.search_value)
        if result["success"]:
            if result["produit"]:
                self.view.load_produit(result["produit"])
                _produits = result["produit"]  # stocker les produits pour référence future
                self.produits = {p["id"]: p for p in _produits}
            else:
                self.produits = []  # réinitialiser la liste des produits
                self.view.btn_edit.setEnabled(False)
                self.view.btn_delete.setEnabled(False)
                self.view.load_produit([])
        else:
            QMessageBox.warning(self.view, "Erreur", result["message"])
            self.view.load_produit([])
        self.table_changer()
       
    @Slot()
    def add_produit(self):
        categories = self.categorie_service.liste_tout_categories()
        dialog = ProduitAddView(categories=categories)
        # dialog.save_requested.connect(
        #     lambda produit: self.on_save(dialog, produit)
        # )
        dialog.btn_save.clicked.connect(
            lambda: self.on_save(dialog, self.get_produit_data(dialog))
        )
        dialog.btn_cancel.clicked.connect(dialog.reject)
        dialog.exec()

    @Slot()
    def update_produit(self):
        id = self.get_selected_id()  # Supposons que l'ID est dans la première colonne
        produit= self.find_produit(int(id))
        categories = self.categorie_service.liste_tout_categories()
        dialog=ProduitAddView(produit,categories)
        dialog.btn_save.clicked.connect(
            lambda: self.on_update(dialog, id, self.get_produit_data(dialog))
        )
        dialog.btn_cancel.clicked.connect(dialog.reject)
        dialog.exec()
        self.refresh()

    def get_produit_data(self,dialog):
        produit = {
            "reference": dialog.reference_produit.text(),
            "designation": dialog.designation_produit.text(),
            "categorie_id": dialog.categorie_produit.currentData(),
            "seuil_alerte": dialog.seuil_alerte_produit.value(),
            "photo_path": dialog.photo_path
        }
        return produit
    
    def on_save(self, dialog, produit):
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
                dest_folder = utils.Utils.dir_folder_photos_produits()
                # os.makedirs(dest_folder, exist_ok=True)
                dialog_photo_filename=os.path.basename(dialog.photo_path)
                _,ext = os.path.splitext(dialog_photo_filename)

                # filename = f"produit_{produit_id}_{os.path.basename(dialog.photo_path)}"
                filename = f"produit_{str(produit_id).zfill(5)}{ext}"
                dest_path = os.path.join(dest_folder, filename)
                shutil.copy(dialog.photo_path, dest_path)
                self.produit_service.update_photo_produit(produit_id, dest_path)
                print(f"photo dest : {dest_path}")
            except Exception as e:
                QMessageBox.warning(dialog, "Erreur", f"Produit ajouté mais la photo n'a pas pu être enregistrée: {e}")
                return   # ❌ la fenêtre reste ouverte
        
        dialog.accept()   # ✅ ferme seulement si succès
        self.refresh()

    def on_update(self, dialog, produit_id, produit):
        print("Call updatee")
        pass
        result, message = self.produit_service.update_produit(produit_id,produit)
        if not result:
            QMessageBox.warning(dialog, "Erreur", message)
            return   # ❌ la fenêtre reste ouverte
        
        if dialog.photo_path:
            try:
                dest_folder = utils.Utils.dir_folder_photos_produits()
                # os.makedirs(dest_folder, exist_ok=True)
                dialog_photo_filename=os.path.basename(dialog.photo_path)
                _,ext = os.path.splitext(dialog_photo_filename)

                # filename = f"produit_{produit_id}_{os.path.basename(dialog.photo_path)}"
                filename = f"produit_{str(produit_id).zfill(5)}{ext}"
                dest_path = os.path.join(dest_folder, filename)
                shutil.copy(dialog.photo_path, dest_path)
                self.produit_service.update_photo_produit(produit_id, dest_path)
                print(f"photo dest : {dest_path}")
            except Exception as e:
                QMessageBox.warning(dialog, "Erreur", f"Produit ajouté mais la photo n'a pas pu être enregistrée: {e}")
                return   # ❌ la fenêtre reste ouverte
        
        dialog.accept()   # ✅ ferme seulement si succès
        self.refresh()

    @Slot()
    def delete_produit(self):
        id = self.get_selected_id() # Supposons que l'ID est dans la première colonne
        confirm = QMessageBox.question(self.view, "Confirmer", f"Êtes-vous sûr de vouloir supprimer le produit ID {id} ?")
        if confirm == QMessageBox.Yes:
            result, message = self.produit_service.delete_produit(int(id))
            if not result:
                QMessageBox.warning(self.view, "Erreur", message)
                return
        self.refresh()  

    @Slot()
    def table_changer(self):
        id = self.get_selected_id()
        if id:
            self.view.btn_edit.setEnabled(True)
            self.view.btn_delete.setEnabled(True)
            produit= self.find_produit(int(id))
            if produit:
                photo_path=produit["photo_path"]
                self.preview_photo(photo_path)
            else:
                self.preview_photo(None)
        else:
            # self.refresh()
            self.view.btn_edit.setEnabled(False)
            self.view.btn_delete.setEnabled(False)
            self.preview_photo(None)

    def find_produit(self, produit_id):
        return self.produits.get(produit_id)
        # return next((p for p in self.produits if p["id"] == produit_id), None)
    
    # def preview_photo(self,file_path):
    #     if file_path:
    #         if os.path.isfile(file_path):
    #             pixmap = QPixmap(file_path)

    #             pixmap = pixmap.scaled(
    #                 self.view.photo_preview.width(),
    #                 self.view.photo_preview.height(),
    #                 Qt.KeepAspectRatio,
    #                 Qt.SmoothTransformation
    #             )
    #             self.view.photo_preview.setPixmap(pixmap)
    #             self.photo_path = file_path
    #         else:
    #             self.view.photo_preview.clear()
    #             self.view.photo_preview.setText("Photo supprimer physiquement.")
    #             self.photo_path = None 
    #     else:
    #         self.view.photo_preview.clear()
    #         self.view.photo_preview.setText("Aucune photo.")
    #         self.photo_path = None 

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
        items = self.view.table.selectedItems()
        if items:
            return int(items[0].text())
        return None