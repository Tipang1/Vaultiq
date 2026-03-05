import os

# Chemin vers %LOCALAPPDATA%\Tipang\Vaultiq\
VAULT_DIR = os.path.join(os.getenv('LOCALAPPDATA'), 'Tipang', 'Vaultiq')
VAULT_PATH = os.path.join(VAULT_DIR, 'vault.dat')

# Créer le dossier si inexistant
os.makedirs(VAULT_DIR, exist_ok=True)
