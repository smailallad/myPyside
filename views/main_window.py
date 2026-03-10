from PySide6.QtWidgets import QFrame, QLabel, QMainWindow, QMessageBox, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget
from PySide6.QtCore import Qt
import qtawesome as qta

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestion de Stock - PySide6")
        # self.resize(1000, 600)
        self.setMinimumSize(900, 600)
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

        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_dashboard.setProperty("type","btn-sidebar")
        self.btn_dashboard.setAttribute(Qt.WA_StyledBackground, True)
        self.btn_dashboard.setIcon(qta.icon("fa5s.home", color='white', color_active='white', color_disabled='gray'))

        self.btn_produits = QPushButton("Produits")
        self.btn_produits.setProperty("type","btn-sidebar")
        self.btn_produits.setAttribute(Qt.WA_StyledBackground, True)
        self.btn_produits.setIcon(qta.icon("fa5s.box", color='white',  color_active='white', color_disabled='gray'))

        self.btn_ventes = QPushButton("Ventes")
        self.btn_ventes.setProperty("type","btn-sidebar")
        self.btn_ventes.setAttribute(Qt.WA_StyledBackground, True)
        self.btn_ventes.setIcon(qta.icon("fa5s.shopping-cart", color='white',  color_active='white', color_disabled='gray'))

        self.btn_quitter = QPushButton("Quitter")
        self.btn_quitter.setProperty("type", "btn-sidebar-danger")
        self.btn_quitter.setAttribute(Qt.WA_StyledBackground, True)
        self.btn_quitter.setIcon(qta.icon("fa5s.sign-out-alt", color='red',  color_active='white', color_disabled='gray'))
        self.btn_quitter.clicked.connect(self.close)
        
        # sidebar_layout.addSpacing(20)
        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_produits)
        sidebar_layout.addWidget(self.btn_ventes)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.btn_quitter)

        # ===== Zone principale =====
        self.stack = QStackedWidget()  # ✅ le stacked widget est ajouté
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

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