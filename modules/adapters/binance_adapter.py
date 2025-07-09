import os
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()

# Inicializar cliente de Binance
binance_client = Client(
    api_key=os.getenv("BINANCE_API_KEY"),
    api_secret=os.getenv("BINANCE_SECRET_KEY")
)

def get_symbol_price(symbol):
    """Devuelve el precio actual de un símbolo desde Binance."""
    try:
        ticker = binance_client.get_symbol_ticker(symbol=symbol)
        return float(ticker["price"])
    except Exception as e:
        print(f"Error al obtener el precio para {symbol}: {e}")
        return None

def get_historical_klines(symbol, interval, lookback):
    """Devuelve los datos OHLC desde Binance."""
    try:
        return binance_client.get_historical_klines(symbol, interval, lookback)
    except Exception as e:
        print(f"Error al obtener klines para {symbol}: {e}")
        return []