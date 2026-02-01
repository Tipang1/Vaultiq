import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


class CryptoManager:
    def __init__(self):
        self._cipher = None

    def generate_salt(self):
        return os.urandom(32)

    def derive_key(self, master_password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=200_000
        )
        key = kdf.derive(master_password.encode('utf-8'))
        return base64.urlsafe_b64encode(key)

    def initialize_cipher(self, master_password, salt):
        key = self.derive_key(master_password, salt)
        self._cipher = Fernet(key)

    def encrypt(self, plaintext):
        if self._cipher is None:
            raise RuntimeError("Cipher not initialized!")
        return self._cipher.encrypt(plaintext.encode('utf-8'))

    def decrypt(self, ciphertext):
        if self._cipher is None:
            raise RuntimeError("Cipher not initialized!")
        return self._cipher.decrypt(ciphertext).decode('utf-8')

    def lock(self):
        self._cipher = None
