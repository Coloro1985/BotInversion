# src/strategies/grid_bot.py

from .base_strategy import BaseStrategy
from ..bot.adapters.base_exchange import BaseExchangeAdapter

class GridBotStrategy(BaseStrategy):
    """
    Implementa una estrategia de Grid Trading.
    Coloca una serie de órdenes de compra y venta por encima y por debajo
    del precio actual, creando una "parrilla".
    """

    def __init__(self, exchange_adapter: BaseExchangeAdapter, symbol: str, config: dict):
        super().__init__(exchange_adapter, symbol, config)
        # Configuración específica de Grid
        self.lower_price = self.config.get('lower_price')
        self.upper_price = self.config.get('upper_price')
        self.grid_levels = self.config.get('grid_levels', 10)
        self.investment_per_level_usd = self.config.get('investment_per_level_usd', 20)
        self.grid_lines = []
        self.stop_loss = self.config.get('stop_loss')

    def initialize(self):
        """Calcula los niveles de la parrilla y coloca las órdenes iniciales."""
        print(f"Inicializando estrategia de Grid para {self.symbol}...")
        if self.stop_loss:
            print(f"   - Stop Loss global en: {self.stop_loss}")
        self._calculate_grid_lines()
        self._setup_initial_orders()
        

    def _calculate_grid_lines(self):
        """Calcula los precios para cada nivel de la parrilla."""
        price_range = self.upper_price - self.lower_price
        step = price_range / (self.grid_levels - 1)
        self.grid_lines = [self.lower_price + i * step for i in range(self.grid_levels)]
        print(f"Niveles de la parrilla calculados: {self.grid_lines}")

    def _setup_initial_orders(self):
        """Coloca las órdenes de compra y venta iniciales según la parrilla."""
        current_price = self.exchange.get_price(self.symbol)
        
        for price in self.grid_lines:
            quantity = self.investment_per_level_usd / price
            try:
                if price < current_price:
                    print(f"Colocando orden de compra en {price:.4f} por {quantity:.6f} {self.symbol}")
                    self.exchange.create_order(
                        symbol=self.symbol, order_type='LIMIT', side='BUY',
                        quantity=quantity, price=price
                    )
                elif price > current_price:
                    # Colocar orden de venta (LIMIT SELL)
                    print(f"Colocando orden de venta en {price:.4f} por {quantity:.6f} {self.symbol}")
                    # Nota: Para vender, necesitas tener el activo. Esto asume que ya lo posees.
                    # En una implementación real, se compraría el activo base primero.
                    # self.exchange.create_order(
                    #     symbol=self.symbol, order_type='LIMIT', side='SELL',
                    #     quantity=quantity, price=price
                    # )
            except Exception as e:
                print(f"No se pudo colocar la orden en el nivel {price}: {e}")

    # --- Lógica completa de Stop Loss ---
    def _check_risk_management(self, current_price: float):
        """Verifica si se alcanzó el stop loss y liquida la posición si es necesario."""
        if self.stop_loss and current_price <= self.stop_loss:
            print(f"🛑 STOP LOSS ALCANZADO para la parrilla {self.symbol} a ${current_price:.2f}!")
            
            # 1. Cancelar todas las órdenes abiertas de la parrilla
            open_orders = self.exchange.get_open_orders(self.symbol)
            for order in open_orders:
                print(f"Cancelando orden {order['orderId']}...")
                self.exchange.cancel_order(self.symbol, order['orderId'])
            
            # 2. Vender toda la posición del activo base
            base_currency = self.symbol.replace('USDT', '')
            balance_info = self.exchange.get_account_balance()
            balance = balance_info.get(base_currency, {}).get('free', 0)
            
            if balance > 0:
                print(f"Vendiendo {balance} de {base_currency} por stop loss...")
                self.exchange.create_order(
                    symbol=self.symbol, order_type='MARKET', side='SELL', quantity=balance
                )
            
            self.stop() # Detiene la estrategia para prevenir más acciones

    def run_logic(self):
        """
        Bucle principal de la estrategia:
        1. Verifica el Stop Loss.
        2. Verifica órdenes ejecutadas y repone la parrilla.
        """
        if not self.is_running:
            return
        
        current_price = self.exchange.get_price(self.symbol)
        print(f"Monitoreando parrilla para {self.symbol}. Precio actual: ${current_price:.2f}")

        # --- Lógica principal del bot ---
        # 1. Chequeo de riesgo primero, siempre.
        self._check_risk_management(current_price)
        if not self.is_running: # Si el SL detuvo el bot, no continuar.
            return
        
        # 2. Tu lógica para reponer la parrilla.
        # En una implementación real, este método necesitaría acceder al historial de trades
        # para ver qué órdenes se completaron desde la última revisión.
        # Por ahora, es un placeholder que demuestra cómo se estructuraría.
        # trade_signals = self.get_trade_signals()
        # for signal in trade_signals:
        #     print(f"Nueva señal de trading generada por la parrilla: {signal}")
        #     self.exchange.create_order(
        #         symbol=self.symbol,
        #         order_type='LIMIT',
        #         side=signal['action'].upper(),
        #         quantity=signal['quantity'],_price=signal['price']
        #     )
        pass # La lógica de reposición se desarrollará más adelante

    def get_trade_signals(self):
        """
        Devuelve una lista de señales de trading basadas en órdenes ejecutadas.
        Cada señal es un diccionario con 'action', 'price' y 'quantity'.
        """
        
        # Por ahora se dejara vacía
        return []