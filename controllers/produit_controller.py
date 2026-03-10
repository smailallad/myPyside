from views.produit_add_view import ProduitAddView
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Slot

class ProduitController():

    def __init__(self, view,container):
        super().__init__()   # obligatoire pour QObject
        self.view = view
        self.produits=[] # stocker les produits affichés dans la table
        self.search_value="" # stocker le terme de recherche actuel

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
                self.produits = result["produit"]  # stocker les produits pour référence future
            else:
                self.produits = []  # réinitialiser la liste des produits
                self.view.btn_edit.setEnabled(False)
                self.view.btn_delete.setEnabled(False)
                self.view.load_produit([])
        else:
            QMessageBox.warning(self.view, "Erreur", result["message"])
            self.view.load_produit([])

    @Slot()
    def add_produit(self):
        categories = self.categorie_service.liste_tout_categories()
        dialog = ProduitAddView(categories=categories)
        dialog.save_requested.connect(
            lambda produit: self.on_save(dialog, produit)
        )
        dialog.exec()
       
    def on_save(self, dialog, produit):
        result, message = self.produit_service.add_produit(produit)
        if not result:
            QMessageBox.warning(dialog, "Erreur", message)
            return   # ❌ la fenêtre reste ouverte
        dialog.accept()   # ✅ ferme seulement si succès
        self.refresh()

    def on_update(self, dialog, id, produit):
        pass
        result, message = self.produit_service.update_produit(id,produit)
        if not result:
            QMessageBox.warning(dialog, "Erreur", message)
            return   # ❌ la fenêtre reste ouverte
        dialog.accept()   # ✅ ferme seulement si succès
        self.refresh()

    @Slot()
    def update_produit(self):
        id = self.view.table.selectedItems()[0].text()  # Supposons que l'ID est dans la première colonne
        produit= self.find_produit(int(id))
        categories = self.categorie_service.liste_tout_categories()
        dialog=ProduitAddView(produit=produit,categories=categories)
        dialog.save_requested.connect(
            lambda produit: self.on_update(dialog, id,produit)
        )
        dialog.exec()
        self.refresh()

    @Slot()
    def delete_produit(self):
        id = self.view.table.selectedItems()[0].text()  # Supposons que l'ID est dans la première colonne
        confirm = QMessageBox.question(self.view, "Confirmer", f"Êtes-vous sûr de vouloir supprimer le produit ID {id} ?")
        if confirm == QMessageBox.Yes:
            result, message = self.produit_service.delete_produit(int(id))
            if not result:
                QMessageBox.warning(self.view, "Erreur", message)
                return
        self.refresh()  

    @Slot()
    def table_changer(self):
        selected_items = self.view.table.selectedItems()
        if selected_items:
            self.view.btn_edit.setEnabled(True)
            self.view.btn_delete.setEnabled(True)
            
        else:
            self.refresh()
            self.view.btn_edit.setEnabled(False)
            self.view.btn_delete.setEnabled(False)

    def find_produit(self, produit_id):
        return next((p for p in self.produits if p["id"] == produit_id), None)