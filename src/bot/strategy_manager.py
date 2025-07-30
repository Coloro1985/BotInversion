import yaml
import time
import importlib
from typing import Dict, List, Any

# --- Imports de tu aplicación ---
from .logger import configurar_logger
from .adapters.binance_adapter import BinanceAdapter
from .adapters.mock_adapter import MockExchangeAdapter
from ..strategies.base_strategy import BaseStrategy

class StrategyManager:
    """
    Gestiona el ciclo de vida de múltiples estrategias de trading.
    Carga, inicia y ejecuta la lógica de cada estrategia activa de forma robusta.
    """
    def __init__(self, config_path: str, api_key: str, api_secret: str):
        """
        Inicializa el gestor de estrategias.

        :param config_path: Ruta al archivo de configuración de estrategias (strategies.yaml).
        :param api_key: La clave API para el exchange.
        :param api_secret: El secreto de la API para el exchange.
        """
        self.logger = configurar_logger()
        self.strategies: List[BaseStrategy] = []
        self.config = self._load_config(config_path)
        self.api_key = api_key
        self.api_secret = api_secret
        
        # ✅ Inyección de Dependencias: Se crea el adaptador de exchange UNA SOLA VEZ.
        self.exchange_adapter = self._initialize_exchange_adapter()
        
        # Si el adaptador se conecta correctamente, inicializamos las estrategias.
        if self.exchange_adapter:
            self._initialize_strategies()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Carga la configuración de estrategias desde un archivo YAML."""
        self.logger.info(f"Cargando configuración desde: {config_path}")
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.error(f"❌ No se encontró el archivo de configuración en '{config_path}'.")
            return {}
        except yaml.YAMLError as e:
            self.logger.error(f"❌ Error al leer el archivo YAML '{config_path}': {e}")
            return {}

    def _initialize_exchange_adapter(self):
        """Crea y verifica la conexión con el adaptador del exchange."""
        exchange_type = self.config.get('exchange', 'binance').lower()
        self.logger.info(f"Inicializando adaptador para el exchange: {exchange_type}")
        
        adapter = None
        try:
            if exchange_type == 'mock':
                adapter = MockExchangeAdapter()
            elif exchange_type == 'binance':
                adapter = BinanceAdapter(self.api_key, self.api_secret)
            else:
                raise ValueError(f"Tipo de exchange '{exchange_type}' no soportado.")
            
            if not adapter.verify_connection():
                 self.logger.error(f"🛑 No se pudo verificar la conexión con la API de {exchange_type}.")
                 return None
            
            self.logger.info(f"✅ Conexión con {exchange_type} establecida correctamente.")
            return adapter
        except Exception as e:
            self.logger.error(f"❌ Falló la inicialización del adaptador de exchange: {e}")
            return None

    def _initialize_strategies(self):
        """Crea las instancias de las estrategias basadas en la configuración."""
        self.logger.info("Inicializando estrategias...")
        
        for strategy_config in self.config.get('strategies', []):
            if not strategy_config.get('enabled', False):
                continue

            strategy_type = strategy_config.get('type')
            
            # ✅ Manejo de Errores en la Carga: Usamos un bloque try-except.
            # Si una estrategia falla al cargar, el bot no se detiene.
            try:
                # Importación dinámica y más segura
                module_name = strategy_type.lower()
                class_name = strategy_type.capitalize() + "Strategy" # Asume un patrón como DcaStrategy
                
                module = importlib.import_module(f"src.strategies.{module_name}")
                StrategyClass = getattr(module, class_name)

                # ✅ Inyección de Dependencias: Pasamos el adaptador ya creado.
                strategy_instance = StrategyClass(
                    config=strategy_config,
                    exchange_adapter=self.exchange_adapter,
                    logger=self.logger
                )
                self.strategies.append(strategy_instance)
                self.logger.info(f"Estrategia '{strategy_type}' para '{strategy_config.get('symbol')}' cargada y lista.")

            except (ModuleNotFoundError, AttributeError) as e:
                self.logger.error(f"❌ No se pudo cargar la estrategia '{strategy_type}'. Revisa que el nombre en 'strategies.yaml' y el nombre de la clase/archivo sean correctos. Error: {e}")
            except Exception as e:
                self.logger.error(f"❌ Falló la inicialización de la estrategia '{strategy_type}': {e}", exc_info=True)

    def run_all(self):
        """Ejecuta la lógica principal de todas las estrategias cargadas."""
        if not self.strategies:
            self.logger.warning("No hay estrategias activas para ejecutar.")
            return
            
        self.logger.info("\n--- Ejecutando ciclo para todas las estrategias ---")
        for strategy in self.strategies:
            try:
                strategy.run()
            except Exception as e:
                self.logger.error(f"❌ Error al ejecutar la estrategia '{strategy.__class__.__name__}': {e}", exc_info=True)
