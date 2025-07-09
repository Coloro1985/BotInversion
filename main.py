import os
import time
import schedule
from dotenv import load_dotenv
from config import VS_CURRENCY
from binance.client import Client
from modules.utils import load_symbol_map
from modules.logger import configurar_logger
from modules.data_fetcher import get_top_cryptos
from modules.runner import run_bot
from modules.telegram_utils import iniciar_telegram_bot


# Cargar variables de entorno y mapa de símbolos
load_dotenv()
logger = configurar_logger()
logger.info("Bot iniciado.")
SYMBOL_MAP = load_symbol_map() # Usa "data/symbol_map.csv" como fuente

# Inicializar cliente Binance
binance_client = Client(
    api_key=os.getenv("BINANCE_API_KEY"),
    api_secret=os.getenv("BINANCE_SECRET_KEY")
)

# Definir las monedas objetivo
COINS = get_top_cryptos()

def main():
    iniciar_telegram_bot()

    if os.getenv("RUN_ONCE") == "1":
        run_bot()
    else:
        logger.info("🤖 Bot de trading iniciado. Presiona Ctrl+C para detener.")
        run_bot()
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    main()
