import core.config as config
class DashboardController:
    def __init__(self, view, container):
        self.view = view
        self.dashboard_service = container.resolve(config.Services.DASHBOARD)
        self.produit_service = container.resolve(config.Services.PRODUIT)
