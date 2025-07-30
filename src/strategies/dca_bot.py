# src/strategies/dca_bot.py

import time
from strategies.base_strategy import BaseStrategy
from bot.adapters.base_exchange import BaseExchangeAdapter

class DCABotStrategy(BaseStrategy):
    """
    Implementa una estrategia de Dollar-Cost Averaging (DCA) con gestión de riesgo.
    """

    def __init__(self, exchange_adapter: BaseExchangeAdapter, symbol: str, config: dict):
        super().__init__(exchange_adapter, symbol, config)
        # Configuración específica de DCA
        self.purchase_amount_usd = self.config.get('purchase_amount_usd', 50)
        self.interval_hours = self.config.get('interval_hours', 24)
        
        # --- NUEVA LÓGICA DE GESTIÓN DE RIESGO ---
        self.take_profit = self.config.get('take_profit')
        self.stop_loss = self.config.get('stop_loss')
        self.last_purchase_time = 0

    def initialize(self):
        """Inicializa la estrategia DCA."""
        print(f"Estrategia DCA inicializada para {self.symbol}.")
        if self.take_profit:
            print(f"   - Take Profit en: {self.take_profit}")
        if self.stop_loss:
            print(f"   - Stop Loss en: {self.stop_loss}")

    def _check_risk_management(self, current_price: float):
        """Verifica si se deben tomar ganancias o cortar pérdidas."""
        base_currency = self.symbol.replace('USDT', '')
        balance = self.exchange.get_account_balance().get(base_currency, {}).get('free', 0)

        if balance == 0:
            return # No hay nada que vender

        # --- Lógica de Take Profit ---
        if self.take_profit and current_price >= self.take_profit:
            print(f"📈 TAKE PROFIT ALCANZADO para {self.symbol} a ${current_price:.2f}!")
            self.exchange.create_order(
                symbol=self.symbol, order_type='MARKET', side='SELL', quantity=balance
            )
            self.stop() # Detener la estrategia después de tomar ganancias

        # --- Lógica de Stop Loss ---
        elif self.stop_loss and current_price <= self.stop_loss:
            print(f"🛑 STOP LOSS ALCANZADO para {self.symbol} a ${current_price:.2f}!")
            self.exchange.create_order(
                symbol=self.symbol, order_type='MARKET', side='SELL', quantity=balance
            )
            self.stop() # Detener la estrategia después de cortar pérdidas

    def run_logic(self):
        """Ejecuta la lógica principal de la estrategia DCA."""
        if not self.is_running:
            return

        try:
            current_price = self.exchange.get_price(self.symbol)
            
            # 1. Primero, verificar gestión de riesgo
            self._check_risk_management(current_price)
            if not self.is_running: # Si el TP/SL detuvo la estrategia, no continuar
                return

            # 2. Luego, ejecutar la compra periódica si aplica
            now = time.time()
            if (now - self.last_purchase_time) > (self.interval_hours * 3600):
                print(f"Ejecutando ciclo de compra DCA para {self.symbol}...")
                quantity_to_buy = self.purchase_amount_usd / current_price
                
                self.exchange.create_order(
                    symbol=self.symbol, order_type='MARKET', side='BUY', quantity=quantity_to_buy
                )
                self.last_purchase_time = now
                print(f"Compra DCA de {quantity_to_buy:.6f} {self.symbol} ejecutada.")

        except Exception as e:
            print(f"Error durante la ejecución de la estrategia DCA: {e}")