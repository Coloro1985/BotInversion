import pandas as pd
import requests

# Importamos el logger de forma relativa
from .logger import configurar_logger

logger = configurar_logger()

def get_top_cryptos(limit=100):
    """
    Obtiene las principales criptomonedas por capitalización de mercado desde CoinGecko.
    """
    logger.info(f"Obteniendo las {limit} criptomonedas principales desde CoinGecko...")
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": False
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return [{'id': coin['id'], 'symbol': coin['symbol'], 'name': coin['name']} for coin in data]
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error de red al obtener criptomonedas principales: {e}")
        return []
    except Exception as e:
        logger.error(f"Error inesperado al obtener criptomonedas principales: {e}")
        return []

def format_klines(klines):
    """
    Convierte los datos de klines (velas) de Binance a un DataFrame de Pandas.
    """
    if not klines:
        return pd.DataFrame()
        
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 
        'close_time', 'quote_asset_volume', 'number_of_trades', 
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    for col in df.columns:
        if col != 'timestamp':
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df