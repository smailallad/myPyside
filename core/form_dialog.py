import re

from PySide6.QtWidgets import (
    QCheckBox, QDialog, QFormLayout, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit,
    QComboBox, QSpinBox, QDoubleSpinBox,
    QMessageBox
)

class FormDialog(QDialog):

    def __init__(self, title="Formulaire"):
        super().__init__()

        self.fields = {}
        self.validation_rules = {}  # clé = nom du champ, valeur = dict des règles
        
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(420, 0)

        self.layout = QVBoxLayout()

        self.form_dialog = QFormLayout()
        self.layout.addLayout(self.form_dialog)

        # boutons
        btn_layout = QHBoxLayout()

        self.btn_save = QPushButton("Enregistrer")
        self.btn_save.setProperty("type","primary")
        self.btn_cancel = QPushButton("Annuler")
        self.btn_cancel.setProperty("type","default")

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_save)

        self.layout.addStretch()
        self.layout.addLayout(btn_layout)
        
        self.setLayout(self.layout)  # <-- IMPORTANT !
        
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.validate)

    # -------------------------
    # ajouter champ
    # -------------------------

    def add_field(self, name, label, field_type="text",default_value=None, options=None, required=True, min_value=None, max_value=None, regex=None,min_length=None, max_length=None):
            # stocker la validation
        self.validation_rules[name] = {
            "required": required,
            "min": min_value,
            "max": max_value,
            "regex": regex,
            "min_length": min_length,
            "max_length": max_length,
            "label": label
        }

        lbl = QLabel(label)

        if field_type == "text":
            widget = QLineEdit()
            if default_value is not None:
                widget.setText(default_value)

        elif field_type == "int":
            widget = QSpinBox()
            widget.setMaximum(999999)
            if default_value is not None:
                widget.setValue(default_value)

        elif field_type == "float":
            widget = QDoubleSpinBox()
            widget.setMaximum(999999999)
            widget.setDecimals(2)
            if default_value is not None:
                widget.setValue(default_value)
        elif field_type == "checkbox":
            widget = QCheckBox()
            if default_value is not None:
                widget.setChecked(default_value)
        elif field_type == "combo":
            widget = QComboBox()
            if options:
                for opt in options:
                    # si c'est un dict -> id + label
                    if isinstance(opt, dict):
                        widget.addItem(opt["nom"], opt["id"])
                    else:
                        widget.addItem(opt)
            if default_value is not None:
                index = widget.findData(default_value)
                if index >= 0:
                    widget.setCurrentIndex(index)
        else:
            widget = QLineEdit()
            if default_value is not None:
                widget.setText(default_value)

        self.form_dialog.insertRow(self.form_dialog.rowCount(), lbl, widget)

        self.fields[name] = widget

    # -------------------------
    # récupérer données
    # -------------------------
    def get_produit(self):
        produit = {}
        for name, widget in self.fields.items():
            if isinstance(widget, QLineEdit):
                produit[name] = widget.text()
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                produit[name] = widget.value()
            elif isinstance(widget, QComboBox):
                produit[name] = widget.currentData()  # récupère la donnée associée à l'option sélectionnée
            elif isinstance(widget, QCheckBox):
                produit[name] = widget.isChecked()

        return produit

    # -------------------------
    # validation
    # -------------------------

    def validate(self):
        produit = self.get_produit()
        # print("Validation des données dans FormDialog, données : ")  # --- IGNORE ---
        # print(produit)  # --- IGNORE ---
        for name, widget in self.fields.items():
            value = produit[name]
            rules = self.validation_rules.get(name, {})
            label = rules.get("label", name)

            # champ obligatoire
            if rules.get("required", True) and (value is None or value == "" or (isinstance(value, str) and value.strip() == "")):
                QMessageBox.warning(self, "Erreur", f"{label} est obligatoire")
                return

            # minimum / maximum pour int / float
            if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                min_val = rules.get("min")
                max_val = rules.get("max")
                if min_val is not None and value < min_val:
                    QMessageBox.warning(self, "Erreur", f"{label} doit être ≥ {min_val}")
                    return
                if max_val is not None and value > max_val:
                    QMessageBox.warning(self, "Erreur", f"{label} doit être ≤ {max_val}")
                    return
                
            # longueur minimale / maximale pour texte
            if isinstance(widget, QLineEdit):
                min_length = rules.get("min_length")
                max_length = rules.get("max_length")
                if min_length is not None and len(value) < min_length:
                    QMessageBox.warning(self, "Erreur", f"{label} doit contenir au moins {min_length} caractères")
                    return
                if max_length is not None and len(value) > max_length:
                    QMessageBox.warning(self, "Erreur", f"{label} doit contenir au maximum {max_length} caractères")
                    return
                
            # regex pour texte
            if isinstance(widget, QLineEdit):
                pattern = rules.get("regex")
                if pattern and not re.fullmatch(pattern, value):
                    QMessageBox.warning(self, "Erreur", f"{label} n’est pas valide")
                    return

        # si tout est OK
        # émettre un signal au controller
        self.save_requested.emit(produit)