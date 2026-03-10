from PySide6.QtCore import QObject, QEvent

class ProduitController(QObject):

    def __init__(self, view,container):
        super().__init__()   # obligatoire pour QObject
        self.view = view
        self.view.table.installEventFilter(self)

        self.produit_service = container.resolve("produit_service")

        # Connecter les signaux
        self._connect_signals()

        # Initial load
        self.refresh()

        # Désactiver les boutons de modification et de suppression au démarrage
        self.view.btn_edit.setEnabled(False)
        self.view.btn_delete.setEnabled(False)

    def eventFilter(self, obj, event):

        if obj == self.view.table:
            if event.type() == QEvent.FocusIn:
                print("Table focus IN")

            if event.type() == QEvent.FocusOut:
                print("Table focus OUT")

        return super().eventFilter(obj, event)

    def _connect_signals(self):
        print("Connexion des signaux dans ProduitController")
        self.view.btn_add.clicked.connect(self.ajouter_produit)
        self.view.btn_edit.clicked.connect(self.update_produit)
        self.view.btn_delete.clicked.connect(self.delete_produit)
        self.view.btn_search.clicked.connect(self.chercher_produit)
        self.view.table.itemSelectionChanged.connect(self.selection_changer)
        
    def refresh(self):
        print("Actualisation des produits dans le controller")
        produits = self.produit_service.get_produits()
        if produits:
            self.view.load_produit(produits)
        else:
            self.view.btn_edit.setEnabled(False)
            self.view.btn_delete.setEnabled(False)
            self.view.load_produit([])
    def ajouter_produit(self):

        print("Ajout d'un produit dans le controller")
        self.refresh()

    def update_produit(self):
        id = self.view.table.selectedItems()[0].text()  # Supposons que l'ID est dans la première colonne
        print(f"Modification du produit {id} dans le controller")
        self.refresh()
    
    def delete_produit(self):
        id = self.view.table.selectedItems()[0].text()  # Supposons que l'ID est dans la première colonne
        print(f"Suppression du produit {id} dans le controller")
        self.refresh()  

    def chercher_produit(self):
        search_term = self.view.search_input.text()
        print(f"Recherche d'un produit dans le controller: {search_term}")
        if len(search_term) == 0:
            self.refresh()
        else:
            self.view.load_produit([])

    def selection_changer(self):
        selected_items = self.view.table.selectedItems()
        if selected_items:
            produit_id = selected_items[0].text()  # Supposons que l'ID est dans la première colonne
            print(f"Produit sélectionné avec ID: {produit_id}")
            self.view.btn_edit.setEnabled(True)
            self.view.btn_delete.setEnabled(True)
            
        else:
            self.refresh()
            self.view.btn_edit.setEnabled(False)
            self.view.btn_delete.setEnabled(False)
            print("Aucun produit sélectionné")

