# src/bot/adapters/binance_adapter.py

import os
from binance.client import Client
from dotenv import load_dotenv
from typing import List, Dict, Any

# ✅ Se corrige la ruta para importar la clase base
from .base_exchange import BaseExchangeAdapter
from ..logger import configurar_logger

load_dotenv()
logger = configurar_logger()

# ✅ Se corrige la herencia de la clase
class BinanceAdapter(BaseExchangeAdapter):
    """
    Adaptador específico para el exchange Binance.
    Hereda de BaseExchangeAdapter e implementa su funcionalidad.
    """

    def _create_client(self) -> Client:
        """Crea el cliente de Binance usando las credenciales."""
        client = Client(self.api_key, self.api_secret)
        return client

    def get_klines(self, symbol: str, interval: str = '1d', limit: int = 300) -> List[Dict[str, Any]]:
        """
        Obtiene datos de velas (k-lines) desde Binance.
        """
        klines = self.client.get_historical_klines(symbol, interval, f"{limit} days ago UTC")
        formatted_klines = []
        for k in klines:
            formatted_klines.append({
                "open_time": k[0],
                "open": float(k[1]),
                "high": float(k[2]),
                "low": float(k[3]),
                "close": float(k[4]),
                "volume": float(k[5]),
                "close_time": k[6],
            })
        return formatted_klines

    def get_price(self, symbol: str) -> float:
        """Obtiene el precio actual de un ticker desde Binance."""
        ticker = self.client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])

    def get_account_balance(self) -> Dict[str, float]:
        """Obtiene el balance de la cuenta de Binance."""
        account_info = self.client.get_account()
        balances = {}
        if 'balances' in account_info:
            for asset in account_info['balances']:
                free = float(asset['free'])
                locked = float(asset['locked'])
                if free > 0 or locked > 0:
                    balances[asset['asset']] = {"free": free, "locked": locked}
        return balances
        
    def create_order(self, symbol: str, order_type: str, side: str, quantity: float, price: float = None) -> Dict[str, Any]:
        """Crea una orden en Binance."""
        if order_type.upper() == 'MARKET':
            order = self.client.create_order(
                symbol=symbol,
                side=side.upper(),
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
        elif order_type.upper() == 'LIMIT':
            if price is None:
                raise ValueError("El precio es obligatorio para órdenes LIMIT.")
            order = self.client.create_order(
                symbol=symbol,
                side=side.upper(),
                type=Client.ORDER_TYPE_LIMIT,
                timeInForce=Client.TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=f'{price:.8f}'
            )
        else:
            raise ValueError(f"Tipo de orden no soportado: {order_type}")
        return order

    def get_open_orders(self, symbol: str = None) -> List[Dict[str, Any]]:
        """Obtiene las órdenes abiertas en Binance."""
        return self.client.get_open_orders(symbol=symbol)

    def cancel_order(self, symbol: str, order_id: str) -> Dict[str, Any]:
        """Cancela una orden en Binance."""
        return self.client.cancel_order(symbol=symbol, orderId=order_id)

    def verify_connection(self) -> bool:
        """Verifica la conexión con la API de Binance."""
        try:
            self.client.ping()
            account_status = self.client.get_account_status()
            return account_status.get('data') == 'Normal'
        except Exception:
            return False