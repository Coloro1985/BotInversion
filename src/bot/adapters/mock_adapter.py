

# src/bot/adapters/mock_adapter.py

import random
from typing import List, Dict, Any
from  import BaseExchangeAdapter

class MockExchangeAdapter(BaseExchangeAdapter):
    """
    Adaptador de simulación (mock) para pruebas.
    No ejecuta órdenes reales. Simula la interacción con un exchange.
    """

    def __init__(self, api_key: str, api_secret: str):
        self._balances = {'USDT': 10000.0} # Saldo inicial para simulación
        self._current_prices = {'BTCUSDT': 52000.0, 'ETHUSDT': 4500.0, 'SOLUSDT': 180.0}
        print("🔌 INICIANDO EN MODO SIMULACIÓN (MOCK) 🔌")
        super().__init__(api_key, api_secret)

    def _create_client(self) -> Any:
        """No se necesita cliente para la simulación."""
        return None

    def _update_mock_price(self, symbol: str):
        """Simula una pequeña fluctuación en el precio."""
        price = self._current_prices.get(symbol, 50000)
        change = price * random.uniform(-0.01, 0.01) # Fluctuación de +/- 1%
        self._current_prices[symbol] = price + change

    def get_klines(self, symbol: str, interval: str, limit: int) -> List[Dict[str, Any]]:
        print(f"SIMULACIÓN: Obteniendo klines para {symbol}")
        # En una simulación avanzada, aquí generaríamos datos falsos.
        return []

    def get_price(self, symbol: str) -> float:
        self._update_mock_price(symbol)
        price = self._current_prices.get(symbol)
        print(f"SIMULACIÓN: El precio de {symbol} es {price:.2f} USDT")
        return price

    def get_account_balance(self) -> Dict[str, float]:
        print(f"SIMULACIÓN: Obteniendo balance: {self._balances}")
        return self._balances

    def create_order(self, symbol: str, order_type: str, side: str, quantity: float, price: float = None) -> Dict[str, Any]:
        base_currency = symbol.replace('USDT', '')
        quote_currency = 'USDT'
        
        order_price = price if price is not None else self.get_price(symbol)
        order_cost = quantity * order_price

        print("="*50)
        print(f"SIMULACIÓN: Recibida orden {side} {order_type} para {quantity:.6f} {base_currency} a ~${order_price:.2f}")

        if side.upper() == 'BUY':
            if self._balances.get(quote_currency, 0) >= order_cost:
                self._balances[quote_currency] -= order_cost
                self._balances[base_currency] = self._balances.get(base_currency, 0) + quantity
                print("✅ ORDEN DE COMPRA SIMULADA EJECUTADA")
            else:
                print("❌ FONDOS INSUFICIENTES (SIMULADO)")
                raise Exception("Fondos insuficientes en la simulación")
        
        elif side.upper() == 'SELL':
            if self._balances.get(base_currency, 0) >= quantity:
                self._balances[base_currency] -= quantity
                self._balances[quote_currency] = self._balances.get(quote_currency, 0) + order_cost
                print("✅ ORDEN DE VENTA SIMULADA EJECUTADA")
            else:
                print(f"❌ NO POSEES SUFICIENTE {base_currency} PARA VENDER (SIMULADO)")
                raise Exception("Activo insuficiente en la simulación")
        
        print(f"Nuevo balance simulado: {self._balances}")
        print("="*50)
        
        return {'symbol': symbol, 'orderId': random.randint(1000, 9999), 'status': 'FILLED'}

    def get_open_orders(self, symbol: str = None) -> List[Dict[str, Any]]:
        # En esta simulación simple, todas las órdenes se completan instantáneamente.
        return []

    def cancel_order(self, symbol: str, order_id: str) -> Dict[str, Any]:
        print(f"SIMULACIÓN: Cancelando orden {order_id} para {symbol}")
        return {'status': 'CANCELED'}

    def verify_connection(self) -> bool:
        return True