import requests
import pandas as pd
from modules.logger import configurar_logger

logger = configurar_logger()

def get_price_data(symbol, vs_currency="usd", days=30):
    """Devuelve histórico de precios de CoinGecko como DataFrame."""
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"
    params = {"vs_currency": vs_currency, "days": days}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        prices = response.json().get("prices", [])
        if not prices:
            return pd.DataFrame()
        
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        return df
    except Exception as e:
        logger.error(f"Error al obtener datos de CoinGecko para {symbol}: {e}")
        return pd.DataFrame()