import json
import base64
from dataclasses import asdict
from cryptography.fernet import InvalidToken
from core.models import PasswordEntry

class Vault:
    def __init__(self, crypto_manager):
        self.crypto = crypto_manager
        self.entries = []  # Liste de PasswordEntry
        self.salt = None

    # Créer un nouveau coffre
    def create(self, master_password):
        self.salt = self.crypto.generate_salt()
        self.crypto.initialize_cipher(master_password, self.salt)

    # Charger un coffre existant
    def load(self, master_password, vault_path):
        with open(vault_path, 'r') as f:
            vault_content = json.load(f)

        salt_b64 = vault_content["salt"]
        encrypted_data_b64 = vault_content["data"]
        encrypted_data = base64.b64decode(encrypted_data_b64)

        self.salt = base64.b64decode(salt_b64)
        self.crypto.initialize_cipher(master_password, self.salt)

        try:
            json_string = self.crypto.decrypt(encrypted_data)
        except InvalidToken:
            raise ValueError("Mauvais mot de passe !")

        entries_as_dicts = json.loads(json_string)
        self.entries = [PasswordEntry(**entry_dict) for entry_dict in entries_as_dicts]


    # Sauvegarder le coffre
    def save(self, vault_path):
        entries_as_dicts = [asdict(entry) for entry in self.entries]
        json_string = json.dumps(entries_as_dicts)
        encrypted_data = self.crypto.encrypt(json_string)

        salt_b64 = base64.b64encode(self.salt).decode('utf-8')
        encrypted_data_b64 = base64.b64encode(encrypted_data).decode('utf-8')

        vault_content = {
            "salt": salt_b64,
            "data": encrypted_data_b64
        }

        with open(vault_path, 'w') as f:
            json.dump(vault_content, f)

    # CRUD operations
    def add_entry(self, entry):
        self.entries.append(entry)

    def remove_entry(self, entry_id):
        # Filtrer pour garder toutes les entries SAUF celle avec cet ID
        self.entries = [e for e in self.entries if e.id != entry_id]

    """def remove_entry(self, entry_id):
    for i, entry in enumerate(self.entries):
        if entry.id == entry_id:
            del self.entries[i]
            return True
    return False  # ID pas trouvé"""

    def get_entry(self, entry_id):
        for entry in self.entries:
            if entry.id == entry_id:
                return entry
        return None  # Pas trouvé

    """def search_entries(self, query):
    query_lower = query.lower()
    results = []
    
    for entry in self.entries:
        if query_lower in entry.service.lower():
            results.append(entry)
    
    return results"""

    def search_entries(self, query):
        q = query.lower()
        return [e for e in self.entries if q in e.service.lower()]
