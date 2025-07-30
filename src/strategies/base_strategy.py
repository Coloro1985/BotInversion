# src/strategies/base_strategy.py

from abc import ABC, abstractmethod
from logging import Logger
from typing import Dict, Any, List

# ✅ Se corrige la ruta para que apunte a 'src.bot'
from src.bot.adapters.base_exchange import BaseExchangeAdapter

class BaseStrategy(ABC):
    """
    Clase base abstracta para todas las estrategias de trading.
    Define la interfaz común que deben seguir.
    """
    def __init__(self, config: Dict[str, Any], exchange_adapter: BaseExchangeAdapter, logger: Logger):
        self.config = config
        self.exchange = exchange_adapter
        self.logger = logger
        self.symbol = config.get('symbol')
        self.is_running = False

    @abstractmethod
    def run(self):
        """
        El método principal que contiene la lógica de la estrategia.
        Debe ser implementado por cada subclase.
        """
        pass

    def start(self):
        """Inicia la estrategia."""
        self.is_running = True
        self.logger.info(f"Estrategia '{self.__class__.__name__}' para {self.symbol} iniciada.")

    def stop(self):
        """Detiene la estrategia."""
        self.is_running = False
        self.logger.info(f"Estrategia '{self.__class__.__name__}' para {self.symbol} detenida.")