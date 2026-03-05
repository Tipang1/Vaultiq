from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTextEdit, QSpinBox, QCheckBox,
    QWidget, QGroupBox
)
from PySide6.QtGui import QIcon
from core.models import PasswordEntry
from core.password_generator import PasswordGenerator
from assets.path import get


class AddEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Ajouter une entrée")
        self.setFixedSize(450, 500)

        self.entry = None  # Sera rempli si l'utilisateur valide
        self.pw_gen = PasswordGenerator()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Service
        layout.addWidget(QLabel("Service / Site :"))
        self.service_input = QLineEdit()
        self.service_input.setPlaceholderText("Ex: Gmail, Facebook...")
        layout.addWidget(self.service_input)

        # Username
        layout.addWidget(QLabel("Identifiant :"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ex: mon.email@example.com")
        layout.addWidget(self.username_input)

        # Password + Generate button
        # Password + Show/Hide + Generate buttons
        layout.addWidget(QLabel("Mot de passe :"))
        password_layout = QHBoxLayout()

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.textChanged.connect(self.update_strength)
        password_layout.addWidget(self.password_input)

        # Show/Hide button
        self.show_password_btn = QPushButton()
        self.show_password_btn.setIcon(QIcon(get('Show Password.png')))
        self.show_password_btn.setToolTip("Afficher le mot de passe")
        self.show_password_btn.setMaximumWidth(40)
        self.show_password_btn.setCheckable(True)  # Toggle button
        self.show_password_btn.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.show_password_btn)

        # Generate button
        self.generate_btn = QPushButton()
        self.generate_btn.setIcon(QIcon(get('Generate Password.png')))
        self.generate_btn.setToolTip("Générer un mot de passe")
        self.generate_btn.setMaximumWidth(40)
        self.generate_btn.clicked.connect(self.on_generate_password)
        password_layout.addWidget(self.generate_btn)

        layout.addLayout(password_layout)

        # Toggle advanced options
        self.toggle_btn = QPushButton("▼ Options de génération")
        self.toggle_btn.clicked.connect(self.toggle_advanced)
        layout.addWidget(self.toggle_btn)

        # Advanced options (collapsible)
        self.advanced_widget = QWidget()
        advanced_layout = QVBoxLayout()
        self.advanced_widget.setLayout(advanced_layout)
        self.advanced_widget.setVisible(False)

        # Length
        length_layout = QHBoxLayout()
        length_layout.addWidget(QLabel("Longueur :"))
        self.length_spin = QSpinBox()
        self.length_spin.setRange(8, 64)
        self.length_spin.setValue(16)
        length_layout.addWidget(self.length_spin)
        length_layout.addStretch()
        advanced_layout.addLayout(length_layout)

        # Checkboxes
        self.cb_lower = QCheckBox("Minuscules (a-z)")
        self.cb_lower.setChecked(True)
        advanced_layout.addWidget(self.cb_lower)

        self.cb_upper = QCheckBox("Majuscules (A-Z)")
        self.cb_upper.setChecked(True)
        advanced_layout.addWidget(self.cb_upper)

        self.cb_digits = QCheckBox("Chiffres (0-9)")
        self.cb_digits.setChecked(True)
        advanced_layout.addWidget(self.cb_digits)

        self.cb_symbols = QCheckBox("Symboles (!@#$...)")
        self.cb_symbols.setChecked(True)
        advanced_layout.addWidget(self.cb_symbols)

        self.cb_accented = QCheckBox("Caractères accentués (àéè...)")
        self.cb_accented.setChecked(True)
        advanced_layout.addWidget(self.cb_accented)

        # Strength indicator
        self.strength_label = QLabel("Force : -")
        advanced_layout.addWidget(self.strength_label)

        layout.addWidget(self.advanced_widget)

        # Notes (optionnel)
        layout.addWidget(QLabel("Notes (optionnel) :"))
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)
        self.notes_input.setPlaceholderText("Informations supplémentaires...")
        layout.addWidget(self.notes_input)

        # Buttons
        self.add_btn = QPushButton("➕ Ajouter")
        self.cancel_btn = QPushButton("❌ Annuler")

        layout.addWidget(self.add_btn)
        layout.addWidget(self.cancel_btn)

        self.add_btn.clicked.connect(self.on_add)
        self.cancel_btn.clicked.connect(self.reject)

    def toggle_advanced(self):
        """Toggle visibility of advanced options"""
        visible = not self.advanced_widget.isVisible()
        self.advanced_widget.setVisible(visible)
        self.toggle_btn.setText("▲ Masquer les options" if visible else "▼ Options de génération")

        # Adjust dialog size
        if visible:
            self.setFixedSize(450, 700)
        else:
            self.setFixedSize(450, 500)

    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_btn.isChecked():
            # Show password
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.show_password_btn.setIcon(QIcon(get('Hide Password.png')))
            self.show_password_btn.setToolTip("Masquer le mot de passe")
        else:
            # Hide password
            self.password_input.setEchoMode(QLineEdit.Password)
            self.show_password_btn.setIcon(QIcon(get('Show Password.png')))
            self.show_password_btn.setToolTip("Afficher le mot de passe")

    def on_generate_password(self):
        """Generate a secure password"""
        length = self.length_spin.value()

        password = self.pw_gen.generate(
            length=length,
            use_lower=self.cb_lower.isChecked(),
            use_upper=self.cb_upper.isChecked(),
            use_digits=self.cb_digits.isChecked(),
            use_symbols=self.cb_symbols.isChecked(),
            use_accented=self.cb_accented.isChecked()
        )

        self.password_input.setText(password)
        self.update_strength()

    def update_strength(self):
        """Update password strength indicator"""
        password = self.password_input.text()
        if not password:
            self.strength_label.setText("Force : -")
            return

        score, label = self.pw_gen.calculate_strength(password)

        # Color based on strength
        if score < 50:
            color = "red"
        elif score < 70:
            color = "orange"
        else:
            color = "green"

        self.strength_label.setText(f'<b>Force : <span style="color:{color}">{label}</span> ({score}/100)</b>')

    def on_add(self):
        service = self.service_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text()
        notes = self.notes_input.toPlainText().strip()

        # Validation
        if not service:
            QMessageBox.warning(self, "Erreur", "Le nom du service est obligatoire !")
            return

        if not username:
            QMessageBox.warning(self, "Erreur", "L'identifiant est obligatoire !")
            return

        if not password:
            QMessageBox.warning(self, "Erreur", "Le mot de passe est obligatoire !")
            return

        # Créer l'entrée
        self.entry = PasswordEntry(
            service=service,
            username=username,
            password=password,
            notes=notes
        )

        self.accept()  # Ferme le dialog avec succès
