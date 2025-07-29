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
        self.investment_per_level = self.config.get('investment_per_level_usd', 20)
        self.grid_lines = []

    def initialize(self):
        """Calcula los niveles de la parrilla y coloca las órdenes iniciales."""
        print("Inicializando estrategia de Grid...")
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
            quantity = self.investment_per_level / price
            try:
                if price < current_price:
                    # Colocar orden de compra (LIMIT BUY)
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

    def run_logic(self):
        """
        Monitorea las órdenes y las vuelve a colocar cuando se ejecutan.
        Por ejemplo, si una orden de compra se ejecuta, coloca una nueva orden de venta
        en el nivel superior.
        """
        if not self.is_running:
            return
        
        print("Monitoreando estado de la parrilla...")
        # Lógica para verificar órdenes completadas y reemplazarlas
        # (Esta parte es más compleja y se desarrollará en el gestor de estrategias)
        pass