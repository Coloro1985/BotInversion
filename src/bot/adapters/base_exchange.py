# src/bot/adapters/base_exchange.py

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseExchangeAdapter(ABC):
    """
    Clase base abstracta para los adaptadores de exchanges.
    Define la interfaz común que todos los adaptadores deben implementar.
    """

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = self._create_client()

    @abstractmethod
    def _create_client(self) -> Any:
        """
        Crea y configura el cliente específico del exchange.
        Debe ser implementado por cada subclase.
        """
        pass

    @abstractmethod
    def get_klines(self, symbol: str, interval: str, limit: int) -> List[Dict[str, Any]]:
        """
        Obtiene datos de velas (k-lines) para un símbolo.
        """
        pass

    @abstractmethod
    def get_price(self, symbol: str) -> float:
        """
        Obtiene el precio actual de un símbolo.
        """
        pass
    
    @abstractmethod
    def get_account_balance(self) -> Dict[str, float]:
        """
        Obtiene el balance de los activos en la cuenta.
        """
        pass

    @abstractmethod
    def create_order(self, symbol: str, order_type: str, side: str, quantity: float, price: float = None) -> Dict[str, Any]:
        """
        Crea una nueva orden en el exchange.
        """
        pass

    @abstractmethod
    def get_open_orders(self, symbol: str = None) -> List[Dict[str, Any]]:
        """
        Obtiene todas las órdenes abiertas, opcionalmente filtrando por símbolo.
        """
        pass

    @abstractmethod
    def cancel_order(self, symbol: str, order_id: str) -> Dict[str, Any]:
        """
        Cancela una orden existente.
        """
        pass

    @abstractmethod
    def verify_connection(self) -> bool:
        """
        Verifica que la conexión con la API del exchange es exitosa.
        """
        pass

    @abstractmethod
    def get_executed_orders(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Obtiene las órdenes que fueron ejecutadas recientemente para un símbolo.
        """
        pass