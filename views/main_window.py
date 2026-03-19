from PySide6.QtWidgets import QCheckBox, QComboBox, QFrame, QLabel, QMainWindow, QMessageBox, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget
from PySide6.QtCore import QSize, Qt, Signal
import qtawesome as qta

class MainWindow(QMainWindow):
    change_theme_signal = Signal(bool)
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestion de Stock - PySide6")
        # self.resize(1000, 600)
        self.setMinimumSize(1200, 600)
        # self.showMaximized()
        # self.showFullScreen()

        # ===== Widget central =====
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setObjectName("main_layout")

        # ===== Sidebar =====
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setObjectName("sidebar")
        sidebar.setAttribute(Qt.WA_StyledBackground, True)
        
        sidebar_layout = QVBoxLayout(sidebar)
        
        self.is_dark_mode = False # ou selon ta config
        self.btn_theme = QPushButton()
        self.btn_theme.setProperty("type","btn-sidebar")
        self.btn_theme.setAttribute(Qt.WA_StyledBackground, True)
        self.btn_theme.setCheckable(True)
        self.btn_theme.setCursor(Qt.PointingHandCursor)
        self.update_theme_icon()

        self.btn_theme.clicked.connect(self.toggle_theme)

        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_dashboard.setProperty("type","btn-sidebar")
        self.btn_dashboard.setAttribute(Qt.WA_StyledBackground, True)
        self.btn_dashboard.setIcon(qta.icon("fa5s.home", color='blue', color_active='blue', color_disabled='gray'))

        self.btn_categories = QPushButton("Categories")
        self.btn_categories.setProperty("type","btn-sidebar")
        self.btn_categories.setAttribute(Qt.WA_StyledBackground, True)
        self.btn_categories.setIcon(qta.icon("fa5s.tags", color='blue',  color_active='blue', color_disabled='gray'))

        self.btn_produits = QPushButton("Produits")
        self.btn_produits.setProperty("type","btn-sidebar")
        self.btn_produits.setAttribute(Qt.WA_StyledBackground, True)
        self.btn_produits.setIcon(qta.icon("fa5s.box", color='blue',  color_active='blue', color_disabled='gray'))

        self.btn_achats = QPushButton("Achats")
        self.btn_achats.setProperty("type","btn-sidebar")
        self.btn_achats.setAttribute(Qt.WA_StyledBackground, True)
        self.btn_achats.setIcon(qta.icon("fa5s.shopping-cart", color='#e67e22',  color_active='blue', color_disabled='gray'))

        self.btn_ventes = QPushButton("Ventes")
        self.btn_ventes.setProperty("type","btn-sidebar")
        self.btn_ventes.setAttribute(Qt.WA_StyledBackground, True)
        self.btn_ventes.setIcon(qta.icon("fa5s.file-invoice-dollar", color='#2ecc71',  color_active='blue', color_disabled='gray'))

        self.btn_clients = QPushButton("Clients")
        self.btn_clients.setProperty("type","btn-sidebar")
        self.btn_clients.setAttribute(Qt.WA_StyledBackground, True)
        self.btn_clients.setIcon(qta.icon("fa5s.users", color='blue',  color_active='blue', color_disabled='gray'))

        self.btn_fournisseurs = QPushButton("Fournisseurs")
        self.btn_fournisseurs.setProperty("type","btn-sidebar")
        self.btn_fournisseurs.setAttribute(Qt.WA_StyledBackground, True)
        self.btn_fournisseurs.setIcon(qta.icon("fa5s.truck", color='blue',  color_active='blue', color_disabled='gray'))

        self.btn_stock = QPushButton("Stock")
        self.btn_stock.setProperty("type","btn-sidebar")
        self.btn_stock.setAttribute(Qt.WA_StyledBackground, True)
        self.btn_stock.setIcon(qta.icon("fa5s.boxes", color='#3498db',  color_active='blue', color_disabled='gray'))

        self.btn_quitter = QPushButton("Quitter")
        self.btn_quitter.setProperty("type", "btn-sidebar-danger")
        self.btn_quitter.setAttribute(Qt.WA_StyledBackground, True)
        self.btn_quitter.setIcon(qta.icon("fa5s.sign-out-alt", color='red',  color_active='blue', color_disabled='gray'))
        self.btn_quitter.clicked.connect(self.close)
        
        sidebar_layout.addWidget(self.btn_theme)
        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_categories)        
        sidebar_layout.addWidget(self.btn_produits)
        sidebar_layout.addWidget(self.btn_achats)
        sidebar_layout.addWidget(self.btn_ventes)
        sidebar_layout.addWidget(self.btn_clients)        
        sidebar_layout.addWidget(self.btn_fournisseurs)
        sidebar_layout.addWidget(self.btn_stock) 

        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.btn_quitter)

        # ===== Zone principale =====
        self.stack = QStackedWidget()  # ✅ le stacked widget est ajouté
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.update_theme_icon()
    
    def update_theme_icon(self):
        if self.is_dark_mode:
            icon = qta.icon("fa5s.moon", color="#f1c40f") # Jaune lune
        else:
            icon = qta.icon("fa5s.sun", color="#f39c12") # Orange soleil
        self.btn_theme.setIcon(icon)
        self.btn_theme.setIconSize(QSize(24, 24))
        self.change_theme_signal.emit(self.is_dark_mode)
    
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Voulez-vous vraiment quitter ?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()