from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
import qtawesome as qta
from PySide6.QtCore import Signal

class DashboardView(QWidget):
    view_activated = Signal()
    # Signal qui envoie la "clé" de la carte cliquée (ex: "produits_non_actifs")
    card_clicked = Signal(str)

    def showEvent(self, event):
        """Méthode native de Qt appelée quand le widget devient visible"""
        super().showEvent(event)
        self.view_activated.emit() # On envoie le signal au contrôleur

    def __init__(self):
        super().__init__()
        self.cards = {}
    
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
        self.add_card("produits","Produits", "1", "info", "fa5s.box","#08a1bc")
        self.add_card("actif","Produits actif", "0", "success", "fa5s.box","#00c60b")
        self.add_card("non_actif","Produits non actif", "0", "warning", "fa5s.box","#f6cc00")
        self.add_card("alerte","Actif Inferieur au seuil", "0", "danger", "fa5s.box","#cf002b")
        # self.add_card("Stock bas", "8", "warning", "fa5s.exclamation-triangle")
        # self.add_card("Factures", "56", "success", "fa5s.file-invoice-dollar")
        # self.add_card("Stock epuise", "5", "danger", "fa5s.file-invoice-dollar","red")
        
        # ASTUCE : On ajoute un stretch à la fin du layout horizontal 
        # pour "pousser" les cartes vers la gauche et les garder serrées
        self.layout_cards.addStretch()

        self.main_layout.addWidget(self.cards_container)

        # Pousse tout vers le haut de la fenêtre
        self.main_layout.addStretch()

    def add_card(self,key, title, value, style_class, icon_name,color_icon="blue"):
        card = QWidget()
        card.setObjectName(key) # On utilise l'objectName pour identifier la carte
        card.setFixedSize(180, 110)
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
        
        # ON SAUVEGARDE LA RÉFÉRENCE
        self.cards[key] = lbl_value

        # 3. Titre (Centré horizontalement)
        lbl_title = QLabel(title.upper())
        lbl_title.setProperty("class","card-titre")
        # lbl_title.setStyleSheet("font-size: 12px; font-weight: bold; color: #ddd; border: none;")
        # lbl_title.setAlignment(Qt.AlignCenter) # <--- CRUCIAL
        layout.addWidget(lbl_title)
        
        # --- Centrage vertical ---
        layout.addStretch() 

        # On active la capture des clics de souris
        card.mousePressEvent = lambda event, k=key: self.card_clicked.emit(k)
        card.setCursor(Qt.PointingHandCursor) # Optionnel: change le curseur en main

        # Juste avant le self.layout_cards.addWidget(card)
        card.style().unpolish(card)
        card.style().polish(card)

        self.layout_cards.addWidget(card)

    # MÉTHODE DE MISE À JOUR
    def update_card_value(self, key, new_value):
        if key in self.cards:
            self.cards[key].setText(str(new_value))