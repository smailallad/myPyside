import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QFrame
)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont

from produit import Produit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.fenetres=[]

        self.setWindowTitle("Gestion de Stock - PySide6")
        self.resize(1000, 600)

        # ===== Widget central =====
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # ===== Sidebar =====
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setObjectName("sidebar")
        # sidebar.setStyleSheet("background-color: #1e1e2f;")
        # sidebar.setStyleSheet("background-color: #1e1e1e;")

        sidebar_layout = QVBoxLayout(sidebar)

        title = QLabel("GESTION")
        title.setStyleSheet("color: white;")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        btn_dashboard = QPushButton("Dashboard")
        btn_produits = QPushButton("Produits")
        btn_ventes = QPushButton("Ventes")

        btn_produits.clicked.connect(self.show_produits)

        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(20)
        sidebar_layout.addWidget(btn_dashboard)
        sidebar_layout.addWidget(btn_produits)
        sidebar_layout.addWidget(btn_ventes)
        sidebar_layout.addStretch()

        # ===== Zone principale =====
        self.content = QWidget()
        
        # Ajouter au layout principal
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content)

    @Slot()
    def show_produits(self):
        if self.fenetres:
            for fen in self.fenetres:
                fen.deleteLater()
            self.fenetres.clear()
        self.fenetres.append(Produit(self.content))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())
    
    # with open("style.qss", "r") as f:
    #     app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())