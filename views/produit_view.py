import locale

from PySide6.QtWidgets import (
    QAbstractItemView, QLabel, QLineEdit, QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PySide6.QtWidgets import QHeaderView
from PySide6.QtCore import Qt
import qtawesome as qta

class ProduitView(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)
        

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher par ID ou référence ou désignation...")

        self.btn_search=QPushButton("")
        self.btn_search.setIcon(qta.icon("fa5s.search", color='white', color_active='white', color_disabled='gray'))
        self.btn_search.setProperty("type","primary")

        recherche_layout = QHBoxLayout()
        recherche_layout.addWidget(QLabel("Recherche:"))
        recherche_layout.addWidget(self.search_input)
        recherche_layout.addWidget(self.btn_search)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Référence","Designation", "Prix", "Stock"]
        )
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.btn_add = QPushButton("Ajouter")
        self.btn_add.setProperty("type","primary")

        # self.btn_refresh = QPushButton("Actualiser")
        # self.btn_refresh.setProperty("type","primary")

        self.btn_edit = QPushButton("Modifier")
        self.btn_edit.setProperty("type","primary")
        
        self.btn_delete = QPushButton("Supprimer")
        self.btn_delete.setProperty("type", "danger")
        
        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.btn_add)
        # btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addStretch()

        container_layout = QVBoxLayout()
        container_layout.addLayout(recherche_layout)
        container_layout.addWidget(self.table)

        self.layout.addLayout(container_layout)
        self.layout.addLayout(btn_layout)

    def load_produit(self, produit):
        self.table.setRowCount(len(produit))
        # Colonnes numériques (ID, Prix, Stock)
        numeric_columns = [0, 3, 4]  
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')  # Format français pour les milliers et décimales
        for row, item in enumerate(produit):
            produits = [
                item["id"],
                item["reference"],
                item["designation"],
                locale.format_string("%0.2f", item["prix_vente"], grouping=True) + " DA",
                item["stock"]
            ]

            for col, produit in enumerate(produits):
                cell = QTableWidgetItem(str(produit))
                if col in numeric_columns:
                    # Alignement à droite pour les chiffres
                    cell.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                else:
                    # Alignement à gauche pour le texte
                    cell.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

                self.table.setItem(row, col, cell)
            
                # self.table.setItem(row, col, QTableWidgetItem(str(produit)))