# src/bot/strategy_manager.py

import time
import yaml # Usaremos YAML para una configuración más legible
from typing import Dict, List, Any
from .adapters.base_exchange import BaseExchangeAdapter
from .adapters.binance_adapter import BinanceAdapter # Importamos un adaptador concreto
from ..strategies.base_strategy import BaseStrategy
from ..strategies.dca_bot import DCABotStrategy
from ..strategies.grid_bot import GridBotStrategy

# Mapeo de nombres de estrategia a sus clases correspondientes
STRATEGY_MAPPING = {
    'dca': DCABotStrategy,
    'grid': GridBotStrategy,
}

class StrategyManager:
    """
    Gestiona el ciclo de vida de múltiples estrategias de trading.
    Carga, inicia, y ejecuta periódicamente la lógica de cada estrategia activa.
    """

    def __init__(self, config_path: str, api_key: str, api_secret: str):
        """
        Inicializa el gestor de estrategias.

        :param config_path: Ruta al archivo de configuración de estrategias (strategies.yaml).
        :param api_key: La clave API para el exchange.
        :param api_secret: El secreto de la API para el exchange.
        """
        self.strategies: List[BaseStrategy] = []
        self.config = self._load_config(config_path)
        self.api_key = api_key
        self.api_secret = api_secret
        self._initialize_strategies()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Carga la configuración de estrategias desde un archivo YAML."""
        print(f"Cargando configuración desde: {config_path}")
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _initialize_strategies(self):
        """Crea las instancias de las estrategias basadas en la configuración."""
        print("Inicializando estrategias...")
        
        # Por ahora, creamos un único adaptador. En el futuro, esto podría
        # modificarse para que cada estrategia use un exchange diferente.
        exchange_adapter = BinanceAdapter(self.api_key, self.api_secret)

        for strategy_config in self.config.get('strategies', []):
            if not strategy_config.get('enabled', False):
                continue

            strategy_name = strategy_config.get('type')
            strategy_class = STRATEGY_MAPPING.get(strategy_name)

            if not strategy_class:
                print(f"ADVERTENCIA: Estrategia '{strategy_name}' no reconocida. Omitiendo.")
                continue

            symbol = strategy_config.get('symbol')
            params = strategy_config.get('parameters', {})
            
            # Creamos la instancia de la estrategia
            strategy_instance = strategy_class(exchange_adapter, symbol, params)
            self.strategies.append(strategy_instance)
            print(f"Estrategia '{strategy_name}' para '{symbol}' cargada y lista.")

    def start_all(self):
        """Inicia todas las estrategias cargadas."""
        if not self.strategies:
            print("No hay estrategias activas para iniciar.")
            return
            
        print("\n--- Iniciando todas las estrategias ---")
        for strategy in self.strategies:
            strategy.start()

    def run_forever(self, interval_seconds: int = 3600):
        """
        Bucle principal que ejecuta la lógica de todas las estrategias de forma periódica.
        
        :param interval_seconds: Tiempo de espera en segundos entre cada ejecución.
                                (Ej: 3600 para DCA horario, 60 para Grid más activo).
        """
        self.start_all()
        
        if not self.strategies:
            return

        print(f"\n--- Gestor de Estrategias en funcionamiento. Próxima ejecución en {interval_seconds} segundos. ---")
        while True:
            for strategy in self.strategies:
                if strategy.is_running:
                    strategy.run_logic()
            
            time.sleep(interval_seconds)