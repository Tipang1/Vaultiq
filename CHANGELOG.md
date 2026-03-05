# Changelog

## [1.1.0] - 2026-03-05

### Nouveautés
- **Générateur de mots de passe sécurisés**
  - Longueur configurable (8-64 caractères)
  - Options : minuscules, majuscules, chiffres, symboles, caractères accentués
  - Indicateur de force du mot de passe
  - Options avancées repliables

- **Filtres de recherche multi-critères**
  - Recherche par service (par défaut)
  - Recherche par identifiant
  - Recherche par notes
  - Combinaison possible de plusieurs critères

- **Bouton afficher/masquer le mot de passe**
  - Toggle visibilité dans le dialog d'ajout

### Améliorations
- Interface du dialog d'ajout améliorée
- Meilleure organisation des champs

### Technique
- Ajout du module `core/password_generator.py`
- `PasswordEntry` maintenant immutable (`frozen=True`)
- Méthode `search_entries()` améliorée avec filtres

---

## [1.0.0] - 2026-02-01

### Version initiale
- Stockage chiffré local (AES-128 + HMAC)
- Dérivation de clé sécurisée (PBKDF2-HMAC-SHA256, 200k iterations)
- Interface graphique (PySide6)
- CRUD complet (Ajouter, Supprimer, Rechercher)
- Copie dans le presse-papier
- 100% offline
