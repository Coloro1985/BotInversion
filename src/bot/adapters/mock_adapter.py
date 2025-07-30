# src/bot/adapters/mock_adapter.py

import random
from typing import List, Dict, Any

# Se importa la clase base desde el archivo hermano 'base_exchange.py'
from .base_exchange import BaseExchangeAdapter
# Se importa el logger desde la carpeta 'bot' (subiendo un nivel)
from ..logger import configurar_logger

class MockExchangeAdapter(BaseExchangeAdapter):
    """
    Adaptador de simulación (mock) para pruebas.
    No ejecuta órdenes reales. Simula la interacción con un exchange,
    incluyendo balance, fluctuaciones de precio y ejecución de órdenes.
    """
    def __init__(self, api_key: str = "mock_key", api_secret: str = "mock_secret"):
        """
        Inicializa el adaptador simulado.
        """
        self.logger = configurar_logger()
        self.logger.info("🔌 INICIANDO EN MODO SIMULACIÓN (MOCK) 🔌")
        super().__init__(api_key, api_secret)
        
        # Atributos para la simulación
        self._balances = {'USDT': 10000.0, 'BTC': 1.0, 'ETH': 10.0} # Saldo inicial
        self._current_prices = {'BTCUSDT': 52000.0, 'ETHUSDT': 4500.0, 'SOLUSDT': 180.0}

    def verify_connection(self) -> bool:
        self.logger.info("[MOCK] Verificando conexión... ¡Exitosa!")
        return True

    def _update_mock_price(self, symbol: str):
        """Simula una pequeña fluctuación aleatoria en el precio."""
        price = self._current_prices.get(symbol, 50000)
        change = price * random.uniform(-0.01, 0.01) # Fluctuación de +/- 1%
        self._current_prices[symbol] = price + change

    def get_price(self, symbol: str) -> float:
        self._update_mock_price(symbol)
        price = self._current_prices.get(symbol)
        self.logger.info(f"[MOCK] Precio de {symbol} es ${price:.2f} USDT")
        return price

    def get_balance(self, asset: str) -> float:
        balance = self._balances.get(asset.upper(), 0.0)
        self.logger.info(f"[MOCK] Balance de {asset}: {balance}")
        return balance

    def create_order(self, symbol: str, order_type: str, side: str, quantity: float, price: float = None) -> Dict[str, Any]:
        base_currency = symbol.replace('USDT', '')
        quote_currency = 'USDT'
        
        order_price = price if price is not None else self.get_price(symbol)
        order_cost = quantity * order_price

        self.logger.info("="*50)
        self.logger.info(f"SIMULACIÓN: Recibida orden {side.upper()} {order_type} para {quantity:.6f} {base_currency} a ~${order_price:.2f}")

        if side.upper() == 'BUY':
            if self.get_balance(quote_currency) >= order_cost:
                self._balances[quote_currency] -= order_cost
                self._balances[base_currency] = self.get_balance(base_currency) + quantity
                self.logger.info("✅ ORDEN DE COMPRA SIMULADA EJECUTADA")
            else:
                self.logger.error("❌ FONDOS INSUFICIENTES (SIMULADO)")
                raise Exception("Fondos insuficientes en la simulación")
        
        elif side.upper() == 'SELL':
            if self.get_balance(base_currency) >= quantity:
                self._balances[base_currency] -= quantity
                self._balances[quote_currency] = self.get_balance(quote_currency) + order_cost
                self.logger.info("✅ ORDEN DE VENTA SIMULADA EJECUTADA")
            else:
                self.logger.error(f"❌ NO POSEES SUFICIENTE {base_currency} PARA VENDER (SIMULADO)")
                raise Exception("Activo insuficiente en la simulación")
        
        self.logger.info(f"Nuevo balance simulado: {self._balances}")
        self.logger.info("="*50)
        
        return {'symbol': symbol, 'orderId': random.randint(1000, 9999), 'status': 'FILLED'}