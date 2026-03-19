import sys
import core.config as config

from PySide6.QtWidgets import QApplication

from core.router import Router
from core.container import Container
from core.auth import AuthManager
from core.schema import create_tables

from core.theme_manager import ThemeManager
from repositories.dashboard_repository import DashboardRepository
from repositories.categorie_repository import CategorieRepository
from repositories.produit_repository import ProduitRepository

from services.dashboard_service import DashboardService
from services.categorie_service import CategorieService
from services.produit_service import ProduitService

from controllers.dashboard_controller import DashboardController
from controllers.categorie_controller import CategorieController
from controllers.produit_controller import ProduitController

from views.main_window import MainWindow
from views.dashboard_view import DashboardView
from views.produit.produit_view import ProduitView

def main():
    # création automatique des tables
    create_tables()
    app = QApplication(sys.argv)

    # Initialisation du manager
    theme_manager = ThemeManager(app)
    
    # 🖥 Main Window
    # Initialisation de la fenêtre
    window = MainWindow()

    # Connexion directe à la méthode du manager
    window.change_theme_signal.connect(theme_manager.handle_theme_change)
    
    # Appliquer le thème initial
    theme_manager.apply_theme("light")
    
    # 🔐 Auth
    auth = AuthManager()
    auth.login("admin", "ADMIN") # Simuler une connexion
    # auth.login("user", "USER") # Simuler une connexion

    # 🧠 Container
    container = Container()

    # Ajout des services et repositories dans le container
    container.register(config.Repositories.DASHBOARD, DashboardRepository())
    container.register(
        config.Services.DASHBOARD,
        lambda: DashboardService(
            container.resolve(config.Repositories.DASHBOARD)
        )
    )

    container.register(config.Repositories.CATEGORIE, CategorieRepository())
    container.register(
        config.Services.CATEGORIE,
        lambda: CategorieService(
            container.resolve(config.Repositories.CATEGORIE)
        )
    )

    container.register(config.Repositories.PRODUIT, ProduitRepository())
    container.register(
        config.Services.PRODUIT,
        lambda: ProduitService(
            container.resolve(config.Repositories.PRODUIT)
        )
    )

    # 🚀 Router
    router = Router(window.stack, container, auth)

    router.register(
        config.Routes.DASHBOARD,
        DashboardView,
        DashboardController,
        roles=["ADMIN", "USER"]
    )

    router.register(
        config.Routes.PRODUIT,
        ProduitView,
        ProduitController,
        roles=["ADMIN"]
    )

    # Signaux de navigation
    window.btn_dashboard.clicked.connect(
        lambda: router.navigate(config.Routes.DASHBOARD)
    )

    window.btn_produits.clicked.connect(
        lambda: router.navigate(config.Routes.PRODUIT)
    )

    window.btn_ventes.clicked.connect(
        lambda: router.navigate(config.Routes.DASHBOARD)
    )

    # Par défaut, on affiche le dashboard
    router.navigate(config.Routes.DASHBOARD)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 