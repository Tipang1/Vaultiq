# 🔐 Vaultiq

Gestionnaire de mots de passe offline sécurisé pour Windows.

## 📋 Fonctionnalités

- ✅ Stockage local chiffré (AES-128 + HMAC via Fernet)
- ✅ Dérivation de clé sécurisée (PBKDF2-HMAC-SHA256, 200k iterations)
- ✅ Interface graphique moderne (PySide6)
- ✅ Recherche rapide
- ✅ Copie dans le presse-papier
- ✅ 100% offline - aucune connexion internet requise

## 🚀 Installation

### Option 1 : Télécharger l'exécutable (recommandé)
1. Téléchargez `Vaultiq.exe` depuis les [Releases](https://github.com/Tipang1/Vaultiq/releases)
2. Lancez `Vaultiq.exe`
3. Créez votre coffre avec un mot de passe maître

### Option 2 : Depuis le code source
```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python main.py
```

## 🔒 Sécurité

- **Chiffrement** : AES-128-CBC + HMAC-SHA256 (Fernet)
- **Dérivation de clé** : PBKDF2-HMAC-SHA256 (200 000 iterations)
- **Stockage** : `%LOCALAPPDATA%\Tipang\Vaultiq\vault.dat`
- **Pas de crypto maison** : utilise uniquement des librairies reconnues

⚠️ **Important** : Ce projet est un exercice de développement (défi "1 app par mois"). 
Pour un usage critique, privilégiez des solutions établies comme Bitwarden, KeePass, etc.

## 📸 Screenshots

*(À ajouter)*

## 🛠️ Technologies

- Python 3.13.5
- PySide6 (Qt6)
- cryptography

## 📝 Licence

MIT License - Voir [LICENSE](LICENSE)

## 👤 Auteur

**Tipang** - Projet réalisé dans le cadre du défi "1 mois, 1 app" (Janvier 2026)
