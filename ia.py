

from PySide6.QtWidgets import QLabel, QGridLayout
from PySide6.QtCore import Qt

# Dummy produit object for demonstration; replace with your actual object
class Produit:
    seuil_alerte = 10

produit = Produit()

# Dummy grid for demonstration; replace with your actual grid layout
grid = QGridLayout()

label_seuil = QLabel(str(produit.seuil_alerte))
label_seuil.setProperty("class", "fields")
label_seuil.setProperty("class", "right")
label_seuil.setAlignment(Qt.AlignRight)
grid.addWidget(label_seuil, 4, 1)
        # En PySide6, setProperty("class", ...) écrase la valeur précédente.
        # Pour appliquer plusieurs classes CSS, utilisez setProperty("class", "fields right")
        label_seuil.setProperty("class", "fields right")