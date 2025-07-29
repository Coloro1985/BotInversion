import os
from binance.client import Client
from dotenv import load_dotenv

# ✅ Se corrige la ruta del logger para que sea relativa
from ..logger import configurar_logger

# Cargar variables de entorno y configurar logger
load_dotenv()
logger = configurar_logger()

# Inicializar cliente de Binance
binance_client = Client(
    api_key=os.getenv("BINANCE_API_KEY"),
    api_secret=os.getenv("BINANCE_SECRET_KEY")
)

def get_symbol_price(symbol):
    """Obtiene el precio actual de un símbolo desde Binance."""
    try:
        ticker = binance_client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])
    except Exception as e:
        logger.error(f"Error al obtener precio para {symbol} desde Binance: {e}")
        return None

def get_historical_klines(symbol, interval, start_str):
    """Obtiene datos históricos (klines/velas) para un símbolo."""
    try:
        klines = binance_client.get_historical_klines(symbol, interval, start_str)
        return klines
    except Exception as e:
        logger.error(f"Error al obtener klines históricos para {symbol}: {e}")
        return []