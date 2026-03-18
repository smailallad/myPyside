from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
import qtawesome as qta

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal de la page
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)

        # 1. Zone des cartes (Conteneur Horizontal)
        self.cards_container = QWidget()
        self.layout_cards = QHBoxLayout(self.cards_container)
        self.layout_cards.setContentsMargins(0, 0, 0, 0)
        self.layout_cards.setSpacing(15)
        
        # Aligner tout à gauche pour que les cartes se suivent
        self.layout_cards.setAlignment(Qt.AlignLeft)

        # Ajout des cartes
        self.add_card("Produits", "120", "info", "fa5s.box")
        self.add_card("Stock bas", "8", "warning", "fa5s.exclamation-triangle")
        self.add_card("Factures", "56", "success", "fa5s.file-invoice-dollar")
        self.add_card("Stock epuise", "5", "danger", "fa5s.file-invoice-dollar","red")
        
        # ASTUCE : On ajoute un stretch à la fin du layout horizontal 
        # pour "pousser" les cartes vers la gauche et les garder serrées
        self.layout_cards.addStretch()

        self.main_layout.addWidget(self.cards_container)

        # Pousse tout vers le haut de la fenêtre
        self.main_layout.addStretch()

    def add_card(self, title, value, style_class, icon_name,color_icon="blue"):
        card = QWidget()
        card.setFixedSize(110, 110)
        card.setProperty("class", "card bordered") # Pas de virgule, espace pour plusieurs classes
        card.setProperty("type", style_class)
        # Layout vertical principal de la carte
        layout = QVBoxLayout(card)
        layout.setSpacing(5) # Espace serré entre icône et texte
        
        # --- Centrage vertical ---
        layout.addStretch() 

        # 1. Icône (Centrée horizontalement)
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon_name, color=color_icon).pixmap(30, 30))
        icon_label.setProperty("class","card-value")
        # icon_label.setAlignment(Qt.AlignCenter) # <--- CRUCIAL
        layout.addWidget(icon_label)

        # 2. Valeur (Centrée horizontalement)
        lbl_value = QLabel(value)
        lbl_value.setProperty("class","card-value")
        # lbl_value.setStyleSheet("font-size: 22px; font-weight: bold; color: white; border: none;")
        # lbl_value.setAlignment(Qt.AlignCenter) # <--- CRUCIAL
        layout.addWidget(lbl_value)

        # 3. Titre (Centré horizontalement)
        lbl_title = QLabel(title.upper())
        lbl_title.setProperty("class","card-titre")
        # lbl_title.setStyleSheet("font-size: 12px; font-weight: bold; color: #ddd; border: none;")
        # lbl_title.setAlignment(Qt.AlignCenter) # <--- CRUCIAL
        layout.addWidget(lbl_title)
        
        # --- Centrage vertical ---
        layout.addStretch() 

        # Juste avant le self.layout_cards.addWidget(card)
        card.style().unpolish(card)
        card.style().polish(card)

        self.layout_cards.addWidget(card)