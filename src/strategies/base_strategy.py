# src/strategies/base_strategy.py

from abc import ABC, abstractmethod
from bot.adapters.base_exchange import BaseExchangeAdapter

class BaseStrategy(ABC):
    """
    Clase base abstracta para todas las estrategias de trading.
    Define la interfaz común que cada estrategia debe implementar.
    """

    def __init__(self, exchange_adapter: BaseExchangeAdapter, symbol: str, config: dict):
        """
        Inicializa la estrategia.

        :param exchange_adapter: Una instancia de un adaptador de exchange (ej. BinanceAdapter).
        :param symbol: El par de trading (ej. 'BTCUSDT').
        :param config: Un diccionario con la configuración específica de la estrategia.
        """
        self.exchange = exchange_adapter
        self.symbol = symbol
        self.config = config
        self.is_running = False

    def start(self):
        """Inicia la ejecución de la estrategia."""
        self.is_running = True
        print(f"Iniciando estrategia {self.__class__.__name__} para {self.symbol}...")
        self.initialize()

    def stop(self):
        """Detiene la ejecución de la estrategia."""
        self.is_running = False
        print(f"Deteniendo estrategia {self.__class__.__name__} para {self.symbol}...")

    @abstractmethod
    def initialize(self):
        """
        Lógica de inicialización. Se ejecuta una vez al iniciar la estrategia.
        Ej: Crear órdenes iniciales, calcular niveles, etc.
        """
        pass

    @abstractmethod
    def run_logic(self):
        """
        El bucle principal de la estrategia. Se ejecuta periódicamente para tomar decisiones.
        """
        pass