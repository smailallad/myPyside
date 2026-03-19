import core.config as config

class DashboardController:
    def __init__(self, view, container,router):
        self.view = view
        self.router =router
        self.dashboard_service = container.resolve(config.Services.DASHBOARD)
        self.produit_service = container.resolve(config.Services.PRODUIT)

        # Connexion : "Quand la vue s'affiche, rafraîchir les compteurs"
        self.view.view_activated.connect(self.update_dashboard)

        # Connexion du clic sur une carte
        self.view.card_clicked.connect(self.handle_card_click)

    def update_dashboard(self):
        total_produits,total_produits_actif,total_produits_non_actif,total_produits_alerte=self.produit_service.get_count_produits()

        # print(total_produit,total_produit_actif,total_produit_non_actif)
        self.view.update_card_value("produits",total_produits)
        self.view.update_card_value("actif",total_produits_actif)
        self.view.update_card_value("non_actif",total_produits_non_actif)
        self.view.update_card_value("alerte",total_produits_alerte)
        # print("Dashboard mis à jour avec les dernières données !")

    def handle_card_click(self,key):
        self.router.navigate(config.Routes.PRODUIT,status=key)