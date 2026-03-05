import secrets
import string

class Chars:
    SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?/\€°\"'"
    ACCENTED = "àâäéèêëïîôùûüÿæœçÀÂÄÉÈÊËÏÎÔÙÛÜŸÆŒÇýÝ"
    LOWER = string.ascii_lowercase
    UPPER = string.ascii_uppercase
    DIGITS = string.digits
    LETTERS = string.ascii_letters

class PasswordGenerator:

    @staticmethod
    def generate(length=16, use_lower=True, use_upper=True,
                 use_digits=True, use_symbols=True, use_accented=True):
        """
        Génère un mot de passe sécurisé.

        Args:
            length: Longueur du mot de passe (8-64)
            use_lower: Inclure minuscules
            use_upper: Inclure majuscules
            use_digits: Inclure chiffres
            use_symbols: Inclure symboles

        Returns:
            str: Mot de passe généré
        """
        # Construire l'alphabet
        alphabet = ""
        if use_lower:
            alphabet += Chars.LOWER
        if use_upper:
            alphabet += Chars.UPPER
        if use_digits:
            alphabet += Chars.DIGITS
        if use_symbols:
            alphabet += Chars.SYMBOLS
        if use_accented:
            alphabet += Chars.ACCENTED

        # Au moins un type doit être sélectionné
        if not alphabet:
            alphabet = Chars.LETTERS + Chars.DIGITS

        # Générer le mot de passe
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password

    @staticmethod
    def calculate_strength(password):
        """
        Calcule la force d'un mot de passe (0-100).

        Args:
            password: Le mot de passe à évaluer

        Returns:
            tuple: (score, label)
                score: 0-100
                label: "Très faible" / "Faible" / "Moyen" / "Fort" / "Très fort"
        """
        score = 0

        # Longueur
        if len(password) >= 8:
            score += 20
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10

        # Variété de caractères
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in Chars.SYMBOLS for c in password)
        has_accented = any(c in Chars.ACCENTED for c in password)

        if has_lower:
            score += 12
        if has_upper:
            score += 12
        if has_digit:
            score += 12
        if has_symbol:
            score += 12
        if has_accented:
            score += 12

        # Label
        if score < 30:
            label = "Très faible"
        elif score < 50:
            label = "Faible"
        elif score < 70:
            label = "Moyen"
        elif score < 90:
            label = "Fort"
        else:
            label = "Très fort"

        return score, label
