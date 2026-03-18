import sys
import core.config as config

from pathlib import Path
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
from views.produit.produit_view import ProduitView

def set_theme(app, theme):
    """
    Applique le thème QSS à l'application.
    theme: "dark" ou "light"
    """
    style_dir = Path(__file__).parent / "resources" / "styles"
    theme_file = "dark.qss" if theme == "dark" else "light.qss"
    structure_file = "style.qss"

    try:
        # Lecture du fichier de couleurs (Dark ou Light)
        with open(style_dir / theme_file, "r", encoding="utf-8") as f:
            theme_content = f.read()
        
        # Lecture du fichier de structure (Dimensions, Radius, etc.)
        with open(style_dir / structure_file, "r", encoding="utf-8") as f:
            structure_content = f.read()

        # Application globale (Fusion des deux)
        app.setStyleSheet(theme_content + "\n" + structure_content)
        
    except FileNotFoundError as e:
        print(f"⚠️ Erreur : Fichier QSS introuvable -> {e}")

def main():
    # création automatique des tables
    create_tables()
    app = QApplication(sys.argv)

    # Initialisation de la fenêtre
    window = MainWindow()

    # --- La fonction de rappel (callback) ---
    def change_theme(is_checked):
        # On détermine le nom du thème
        mode = "dark" if is_checked else "light"
        # On appelle la fonction globale
        set_theme(app, mode)
        # print(f"🎨 Thème changé en : {mode}")

    # Appliquer le thème par défaut au démarrage
    set_theme(app, "light")

    # Connecter le signal du CheckBox / Switch
    window.check_theme.toggled.connect(change_theme)

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

    # 🖥 Main Window
    window = MainWindow()
    window.check_theme.toggled.connect(change_theme)

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