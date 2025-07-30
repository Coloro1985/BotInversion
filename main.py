# main.py
import sys
import os
import warnings

# --- LA SOLUCIÓN MÁGICA ---
# Esto añade la carpeta 'src' al path de Python.
# Ahora Python sabrá dónde encontrar el módulo 'bot' y los demás.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
# -------------------------

from bot.runner import run_bot

# Ignorar advertencias comunes
warnings.filterwarnings('ignore', category=FutureWarning)

if __name__ == "__main__":
    run_bot()