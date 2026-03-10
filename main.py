from pathlib import Path
import sys
from PySide6.QtWidgets import QApplication

from core.router import Router
from core.container import Container
from core.auth import AuthManager
from core.schema import create_tables

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
from views.produit_view import ProduitView

def main():
    # création automatique des tables
    create_tables()
    
    app = QApplication(sys.argv)

    style_path = Path(__file__).parent / "resources" / "styles" / "style.qss"

    with open(style_path, "r") as f:
        app.setStyleSheet(f.read())

    # with open("myStyle.qss", "r") as f:
    #     app.setStyleSheet(f.read())

    # Set the 'Fusion' system style
    # app.setStyle('Oxygen')

    # 🔐 Auth
    auth = AuthManager()
    auth.login("admin", "ADMIN") # Simuler une connexion
    # auth.login("user", "USER") # Simuler une connexion

    # 🧠 Container
    container = Container()

    # Ajout des services et repositories dans le container
    container.register("dashboard_repository", DashboardRepository())
    container.register(
        "dashboard_service",
        lambda: DashboardService(
            container.resolve("dashboard_repository")
        )
    )

    container.register("categorie_repository", CategorieRepository())
    container.register(
        "categorie_service",
        lambda: CategorieService(
            container.resolve("categorie_repository")
        )
    )

    container.register("produit_repository", ProduitRepository())
    container.register(
        "produit_service",
        lambda: ProduitService(
            container.resolve("produit_repository")
        )
    )

    # 🖥 Main Window
    window = MainWindow()

    # 🚀 Router
    router = Router(window.stack, container, auth)

    router.register(
        "dashboard",
        DashboardView,
        DashboardController,
        roles=["ADMIN", "USER"]
    )

    router.register(
        "produits",
        ProduitView,
        ProduitController,
        roles=["ADMIN"]
    )

    # Signaux de navigation
    window.btn_dashboard.clicked.connect(
        lambda: router.navigate("dashboard")
    )

    window.btn_produits.clicked.connect(
        lambda: router.navigate("produits")
    )

    window.btn_ventes.clicked.connect(
        lambda: router.navigate("ventes")
    )

    # Par défaut, on affiche le dashboard
    router.navigate("dashboard")

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()