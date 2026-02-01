from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTextEdit
)
from PySide6.QtGui import QIcon
from core.models import PasswordEntry
import assets.path


class AddEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Ajouter une entrée")
        self.setWindowIcon(QIcon(assets.path.get("Add Entry.png")))
        self.setFixedSize(400, 350)

        self.entry = None  # Sera rempli si l'utilisateur valide

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

        # Password
        layout.addWidget(QLabel("Mot de passe :"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Notes (optionnel)
        layout.addWidget(QLabel("Notes (optionnel) :"))
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)
        self.notes_input.setPlaceholderText("Informations supplémentaires...")
        layout.addWidget(self.notes_input)

        # Boutons
        self.add_btn = QPushButton("➕ Ajouter")
        self.cancel_btn = QPushButton("❌ Annuler")

        layout.addWidget(self.add_btn)
        layout.addWidget(self.cancel_btn)

        self.add_btn.clicked.connect(self.on_add)
        self.cancel_btn.clicked.connect(self.reject)

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
