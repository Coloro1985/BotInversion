from binance.client import Client
import os
from dotenv import load_dotenv
import requests
from modules.logger import configurar_logger
from modules.adapters.binance_adapter import get_symbol_price, get_historical_klines
from modules.adapters.coingecko_adapter import get_price_data
logger = configurar_logger()

# Cargar variables de entorno desde .env
load_dotenv()

# Inicializar cliente de Binance
binance_client = Client(
    api_key=os.getenv("BINANCE_API_KEY"),
    api_secret=os.getenv("BINANCE_SECRET_KEY")
)


def get_price_from_coingecko(symbol):
    """Obtiene el precio actual de una criptomoneda desde CoinGecko."""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return data[symbol]["usd"]
    except Exception as e:
        logger.error(f"Error al obtener el precio desde CoinGecko para {symbol}: {e}")
        return None

def get_active_cryptos():
    """Obtiene una lista de criptomonedas activas desde CoinGecko."""
    try:
        url = "https://api.coingecko.com/api/v3/coins/list"
        response = requests.get(url)
        data = response.json()
        return [coin["id"] for coin in data]
    except Exception as e:
        logger.error(f"Error al obtener criptomonedas activas: {e}")
        return []

def get_coin_data(coin_id):
    """Obtiene datos detallados de una criptomoneda desde CoinGecko."""
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        logger.error(f"Error al obtener datos para {coin_id}: {e}")
        return None

import pandas as pd


# Nueva función para obtener las principales criptomonedas por capitalización de mercado desde CoinGecko
def get_top_cryptos(limit=10):
    """
    Devuelve una lista de las principales criptomonedas por capitalización de mercado.
    Cada elemento es un diccionario con 'id', 'symbol', y 'name'.
    """
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": False
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Esto lanzará un error si la petición falla
        data = response.json()
        
        # ✅ CAMBIO: Devolvemos un diccionario con más datos, no solo el ID.
        # Esto permite que el runner use el símbolo ('btc') y el nombre ('Bitcoin').
        return [{'id': coin['id'], 'symbol': coin['symbol'], 'name': coin['name']} for coin in data]
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error de red al obtener criptomonedas principales: {e}")
        return []
    except Exception as e:
        logger.error(f"Error inesperado al obtener criptomonedas principales: {e}")
        return []

def format_klines(klines):
    """Convierte los datos de klines de Binance en un DataFrame con columnas estándar OHLC."""
    if not klines:
        return pd.DataFrame()
    return pd.DataFrame([{
        "timestamp": int(k[0]),
        "open": float(k[1]),
        "high": float(k[2]),
        "low": float(k[3]),
        "close": float(k[4]),
        "volume": float(k[5])
    } for k in klines])