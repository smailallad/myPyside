from PySide6.QtWidgets import (
    QStyledItemDelegate, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QAbstractItemView, QTableView, QSplitter,
    QComboBox, QMenu
)
from PySide6.QtWidgets import QHeaderView
from PySide6.QtCore import Qt
import qtawesome as qta

class ProduitView(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        
        # ===== CONTENEUR HEADER =====
        header_container = QWidget()
        header_container.setProperty("class","bordered")
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(10,10,10,10)

        # ===== TITRE =====
        title = QLabel("Gestion des Produits")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:18px;font-weight:bold;")
        header_layout.addWidget(title)

        # ===== FILTRE =====
        filter_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Recherche produit...")
        self.search_input.addAction(
            qta.icon("fa5s.search"), QLineEdit.LeadingPosition
        )

        self.combo_stock=QComboBox()
        self.combo_actif=QComboBox()
        self.combo_categorie = QComboBox() 
        
        self.combo_stock.setItemDelegate(QStyledItemDelegate())
        self.combo_actif.setItemDelegate(QStyledItemDelegate())
        self.combo_categorie.setItemDelegate(QStyledItemDelegate())

        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(self.combo_stock)
        filter_layout.addWidget(self.combo_actif)
        filter_layout.addWidget(self.combo_categorie)

        header_layout.addLayout(filter_layout)

        # ===== ACTIONS =====
        actions_layout = QHBoxLayout()

        self.btn_add = QPushButton("Ajouter")
        self.btn_add.setIcon(qta.icon("fa5s.plus",color="white"))
        self.btn_add.setProperty("type","primary")

        self.btn_detail = QPushButton("Detail")
        self.btn_detail.setIcon(qta.icon("fa5s.eye",color="white"))
        self.btn_detail.setProperty("type","success")

        self.btn_edit = QPushButton("Modifier")
        self.btn_edit.setIcon(qta.icon("fa5s.edit",color="white"))
        self.btn_edit.setProperty("type","success")

        self.btn_delete = QPushButton("Supprimer")
        self.btn_delete.setIcon(qta.icon("fa5s.trash",color="white"))
        self.btn_delete.setProperty("type","danger")

        # ===== Btn Navigations ========#
        pagination_layout = QHBoxLayout()

        self.btn_first = QPushButton()
        self.btn_first.setIcon(qta.icon("fa5s.angle-double-left",color="white"))
        self.btn_first.setProperty("type","primary")

        self.btn_prev = QPushButton()
        self.btn_prev.setIcon(qta.icon("fa5s.angle-left",color="white"))
        self.btn_prev.setProperty("type","primary")

        self.label_page = QLabel("Page 1 / 1")

        self.btn_next = QPushButton()
        self.btn_next.setIcon(qta.icon("fa5s.angle-right",color="white"))
        self.btn_next.setProperty("type","primary")

        self.btn_last = QPushButton()
        self.btn_last.setIcon(qta.icon("fa5s.angle-double-right",color="white"))
        self.btn_last.setProperty("type","primary")

        pagination_layout.addStretch()
        pagination_layout.addWidget(self.btn_first)
        pagination_layout.addWidget(self.btn_prev)
        pagination_layout.addWidget(self.label_page)
        pagination_layout.addWidget(self.btn_next)
        pagination_layout.addWidget(self.btn_last)

        actions_layout.addWidget(self.btn_add)
        actions_layout.addWidget(self.btn_edit)
        actions_layout.addWidget(self.btn_detail)
        actions_layout.addWidget(self.btn_delete)
        actions_layout.addLayout(pagination_layout)
        actions_layout.addStretch()
        
        header_layout.addLayout(actions_layout)

        main_layout.addWidget(header_container)

        # ===== TABLE =====
        self.table = QTableView()

        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(44)

        # ===== PHOTO =====
        photo_container = QWidget()
        # photo_container.setStyleSheet("""
        # QWidget{
        #     background:white;
        #     border:1px solid #ddd;
        #     border-radius:6px;
        # }
        # """)
        photo_container.setProperty("class","bordered")

        photo_layout = QVBoxLayout(photo_container)

        self.photo_preview = QLabel("Aucune photo")
        self.photo_preview.setAlignment(Qt.AlignCenter)
        self.photo_preview.setMinimumSize(220,220)

        photo_layout.addWidget(self.photo_preview)
        photo_layout.addStretch()

        # ===== SPLITTER =====
        splitter = QSplitter()

        splitter.addWidget(self.table)
        splitter.addWidget(photo_container)

        splitter.setSizes([800,220])

        main_layout.addWidget(splitter,stretch=1)

        # ===== STATUS BAR =====
        status_container = QWidget()
        # status_container.setStyleSheet("""
        # QWidget{
        #     background:white;
        #     border:1px solid #ddd;
        #     border-radius:6px;
        # }
        # """)
        status_container.setProperty("class","bordered")

        status_layout = QHBoxLayout(status_container)

        self.label_count = QLabel("Total produits : 0")

        status_layout.addWidget(self.label_count)
        status_layout.addStretch()

        main_layout.addWidget(status_container)

        # ===== MENU CONTEXTUEL =====
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self,pos):

        menu = QMenu(self)

        action_edit = menu.addAction("Modifier")
        action_delete = menu.addAction("Supprimer")

        action = menu.exec(self.table.viewport().mapToGlobal(pos))

        if action == action_edit:
            self.btn_edit.click()

        if action == action_delete:
            self.btn_delete.click()