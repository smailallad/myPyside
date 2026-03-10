class CategorieController:
    def __init__(self,view,container):
        super().__init__()
        self.view = view

        self.produit_service = container.resolve("produit_service")
        self.categorie_service = container.resolve("categorie_service")

        # Connecter les signaux
        self._connect_signals()

        # Initial load
        self.refresh()

        # Désactiver les boutons de modification et de suppression au démarrage
        # self.view.btn_edit.setEnabled(False)
        # self.view.btn_delete.setEnabled(False)

    def _connect_signals(self):
        pass
        # self.view.btn_add.clicked.connect(self.ajouter_produit)
        # self.view.btn_edit.clicked.connect(self.update_produit)
        # self.view.btn_delete.clicked.connect(self.delete_produit)
        # self.view.btn_search.clicked.connect(self.chercher_produit)
        # self.view.table.itemSelectionChanged.connect(self.selection_changer)
     