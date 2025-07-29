# src/strategies/dca_bot.py

import time
from .base_strategy import BaseStrategy
from ..bot.adapters.base_exchange import BaseExchangeAdapter

class DCABotStrategy(BaseStrategy):
    """
    Implementa una estrategia de Dollar-Cost Averaging (DCA).
    Compra una cantidad fija de un activo a intervalos regulares.
    """

    def __init__(self, exchange_adapter: BaseExchangeAdapter, symbol: str, config: dict):
        super().__init__(exchange_adapter, symbol, config)
        # Configuración específica de DCA
        self.purchase_amount_usd = self.config.get('purchase_amount_usd', 50) # USD a invertir por compra
        self.interval_hours = self.config.get('interval_hours', 24) # Frecuencia de compra

    def initialize(self):
        """No se requiere una inicialización compleja para DCA."""
        print("Estrategia DCA inicializada. Se realizarán compras periódicas.")

    def run_logic(self):
        """
        Ejecuta un ciclo de compra. Esta función sería llamada por un gestor
        de estrategias a intervalos regulares.
        """
        if not self.is_running:
            return

        try:
            print(f"Ejecutando ciclo DCA para {self.symbol}...")
            
            # 1. Obtener el precio actual para calcular la cantidad de cripto a comprar
            current_price = self.exchange.get_price(self.symbol)
            
            # 2. Calcular la cantidad de la criptomoneda a comprar
            quantity_to_buy = self.purchase_amount_usd / current_price
            
            # 3. Crear la orden de compra a mercado
            print(f"Intentando comprar {quantity_to_buy:.6f} de {self.symbol} a un precio de ~${current_price}")
            order = self.exchange.create_order(
                symbol=self.symbol,
                order_type='MARKET',
                side='BUY',
                quantity=quantity_to_buy
            )
            
            print("¡Orden de compra DCA ejecutada exitosamente!")
            print(order)

        except Exception as e:
            print(f"Error durante la ejecución de la estrategia DCA: {e}")