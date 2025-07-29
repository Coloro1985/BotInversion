# main.py

from src.bot.runner import run_bot
import warnings

# Ignorar advertencias comunes de librerías para una salida más limpia
warnings.filterwarnings('ignore', category=FutureWarning)

if __name__ == "__main__":
    run_bot()