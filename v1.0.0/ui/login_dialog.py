from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtGui import QIcon
from core.crypto import CryptoManager
from core.vault import Vault
from core.config import VAULT_PATH
import assets.path
import os


class LoginDialog(QDialog):
    def __init__(self, vault_path="data/vault.dat"):
        super().__init__()
        self.setWindowIcon(QIcon(assets.path.get('login.png')))

        self.vault_path = VAULT_PATH
        self.vault = None  # Sera rempli après login/create
        self.crypto = CryptoManager()

        self.setWindowTitle("Se connecter / s'enregistrer")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Mot de passe maître :"))

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_btn = QPushButton("Ouvrir coffre")
        self.create_btn = QPushButton("Créer nouveau coffre")

        layout.addWidget(self.login_btn)
        layout.addWidget(self.create_btn)

        self.login_btn.clicked.connect(self.on_login)
        self.create_btn.clicked.connect(self.on_create)

    def on_login(self):
        password = self.password_input.text()

        if not password:
            QMessageBox.warning(self, "Erreur", "Le mot de passe est vide !")
            return

        if not os.path.exists(self.vault_path):
            QMessageBox.warning(self, "Erreur", "Aucun coffre trouvé. Créez-en un d'abord !")
            return

        try:
            self.vault = Vault(self.crypto)
            self.vault.load(password, self.vault_path)

            QMessageBox.information(self, "Succès", f"Coffre ouvert ! {len(self.vault.entries)} entrées.")
            self.accept()

        except ValueError as e:
            QMessageBox.critical(self, "Erreur", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur inattendue : {e}")

    def on_create(self):
        password = self.password_input.text()

        if not password:
            QMessageBox.warning(self, "Erreur", "Le mot de passe est vide !")
            return

        if len(password) < 8:
            QMessageBox.warning(self, "Attention", "Le mot de passe devrait faire au moins 8 caractères.")
            return

        if os.path.exists(self.vault_path):
            reply = QMessageBox.question(
                self, "Confirmation",
                "Un coffre existe déjà. Voulez-vous le remplacer ?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        try:
            self.vault = Vault(self.crypto)
            self.vault.create(password)

            # Créer le dossier si besoin
            os.makedirs(os.path.dirname(self.vault_path), exist_ok=True)
            self.vault.save(self.vault_path)

            QMessageBox.information(self, "Succès", "Nouveau coffre créé !")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur : {e}")
