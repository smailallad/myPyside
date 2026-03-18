from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame

class MyHr(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  # Initialisation obligatoire
        
        # 1. Création de la ligne (On utilise QFrame pour un meilleur rendu de ligne)
        line = QFrame()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #e0e0e0; border: none;")
        
        # 2. Configuration du layout sur 'self'
        # On définit les marges directement ici
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 30, 0, 16)
        layout.setSpacing(0)
        
        # 3. Ajout de la ligne au layout de ce widget
        layout.addWidget(line)

# Utilisation dans ton interface :
# ma_vue_layout.addWidget(MyHr())