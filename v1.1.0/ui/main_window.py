from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit,
    QLabel, QMessageBox, QCheckBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import sys
from ui.login_dialog import LoginDialog
from ui.entry_dialog import AddEntryDialog
from core.config import VAULT_PATH
from assets.path import get


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestionnaire de mots de passe")
        self.setGeometry(100, 100, 900, 600)
        self.setWindowIcon(QIcon(get('icon.png')))

        # Login
        self.vault = None
        if not self.show_login():
            sys.exit()

        # Setup UI
        self.setup_ui()
        self.load_entries()

    def show_login(self):
        dialog = LoginDialog()
        result = dialog.exec()

        if result == LoginDialog.Accepted:
            self.vault = dialog.vault
            return True
        else:
            return False

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # --- Barre de recherche ---
        search_widget = QWidget()
        search_main_layout = QVBoxLayout()
        search_widget.setLayout(search_main_layout)

        # Search input
        search_input_layout = QHBoxLayout()
        search_input_layout.addWidget(QLabel("Recherche :"))

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher...")
        self.search_input.textChanged.connect(self.on_search)
        search_input_layout.addWidget(self.search_input)

        search_main_layout.addLayout(search_input_layout)

        # Search filters (checkboxes)
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Rechercher dans :"))

        self.cb_search_service = QCheckBox("Service")
        self.cb_search_service.setChecked(True)  # Default
        self.cb_search_service.stateChanged.connect(self.on_search)
        filter_layout.addWidget(self.cb_search_service)

        self.cb_search_username = QCheckBox("Identifiant")
        self.cb_search_username.setChecked(False)
        self.cb_search_username.stateChanged.connect(self.on_search)
        filter_layout.addWidget(self.cb_search_username)

        self.cb_search_notes = QCheckBox("Notes")
        self.cb_search_notes.setChecked(False)
        self.cb_search_notes.stateChanged.connect(self.on_search)
        filter_layout.addWidget(self.cb_search_notes)

        filter_layout.addStretch()

        search_main_layout.addLayout(filter_layout)

        main_layout.addWidget(search_widget)

        # --- Table des entrées ---
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Service", "Identifiant", "Notes"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Lecture seule

        # Redimensionner les colonnes
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 300)

        main_layout.addWidget(self.table)

        # --- Boutons ---
        button_layout = QHBoxLayout()

        self.add_btn = QPushButton("➕ Ajouter")
        self.delete_btn = QPushButton("🗑️ Supprimer")
        self.copy_btn = QPushButton("📋 Copier mot de passe")

        self.add_btn.clicked.connect(self.on_add)
        self.delete_btn.clicked.connect(self.on_delete)
        self.copy_btn.clicked.connect(self.on_copy_password)

        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.copy_btn)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

    def load_entries(self, query="", fields=None):
        """Charge les entrées dans la table (avec filtre optionnel)"""
        self.table.setRowCount(0)  # Vider la table

        # Filtrer les entrées
        entries = self.vault.search_entries(query, fields)

        # Remplir la table
        for entry in entries:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(entry.service))
            self.table.setItem(row, 1, QTableWidgetItem(entry.username))
            self.table.setItem(row, 2, QTableWidgetItem(entry.notes))

            # Stocker l'ID dans la ligne (pour delete/copy)
            self.table.item(row, 0).setData(Qt.UserRole, entry.id)

    def on_search(self):
        """Appelé quand le texte de recherche change ou les filtres"""
        query = self.search_input.text()

        # Déterminer les champs actifs
        fields = []
        if self.cb_search_service.isChecked():
            fields.append('service')
        if self.cb_search_username.isChecked():
            fields.append('username')
        if self.cb_search_notes.isChecked():
            fields.append('notes')

        # Rechercher
        self.load_entries(query, fields)

    def on_add(self):
        """Ouvre le dialog pour ajouter une entrée"""
        dialog = AddEntryDialog(self)
        result = dialog.exec()

        if result == AddEntryDialog.Accepted:
            # Ajouter l'entrée au vault
            self.vault.add_entry(dialog.entry)
            self.vault.save(VAULT_PATH)

            # Rafraîchir la table
            self.on_search()

    def on_delete(self):
        """Supprime l'entrée sélectionnée"""
        selected_rows = self.table.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(self, "Attention", "Sélectionnez une entrée à supprimer !")
            return

        row = selected_rows[0].row()
        entry_id = self.table.item(row, 0).data(Qt.UserRole)
        service_name = self.table.item(row, 0).text()

        # Confirmation
        reply = QMessageBox.question(
            self, "Confirmation",
            f"Supprimer l'entrée '{service_name}' ?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.vault.remove_entry(entry_id)
            self.vault.save(VAULT_PATH)
            self.on_search()
            QMessageBox.information(self, "Succès", "Entrée supprimée !")

    def on_copy_password(self):
        """Copie le mot de passe dans le presse-papier"""
        selected_rows = self.table.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(self, "Attention", "Sélectionnez une entrée !")
            return

        row = selected_rows[0].row()
        entry_id = self.table.item(row, 0).data(Qt.UserRole)

        # Récupérer l'entrée
        entry = self.vault.get_entry(entry_id)

        if entry:
            # Copier dans le presse-papier
            clipboard = QApplication.clipboard()
            clipboard.setText(entry.password)

            QMessageBox.information(self, "Succès", "Mot de passe copié !")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
