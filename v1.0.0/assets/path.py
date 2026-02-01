import sys
import os


def get(relative_path):
    """
    Retourne le chemin absolu d'une ressource.
    Fonctionne en dev (Python) ET en prod (PyInstaller .exe)
    """
    if getattr(sys, 'frozen', False):
        # Mode .exe (PyInstaller)
        base_path = sys._MEIPASS
    else:
        # Mode dev (Python)
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, 'assets', relative_path)
