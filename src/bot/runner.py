import os
from dotenv import load_dotenv
from .strategy_manager import StrategyManager

def run_bot():
    """
    Punto de entrada principal para ejecutar el bot de trading.
    Carga la configuración, inicializa el gestor de estrategias y lo pone en marcha.
    """
    print("🚀 Iniciando el Bot de Inversión...")

    # Cargar variables de entorno (API_KEY, API_SECRET)
    load_dotenv()
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    if not api_key or not api_secret:
        print("🛑 ERROR: Las variables de entorno API_KEY y API_SECRET no están definidas.")
        print("Por favor, créalas en un archivo .env en la raíz del proyecto.")
        return

    # Ruta al archivo de configuración de estrategias
    config_path = 'strategies.yaml'
    
    # Verificar si el archivo de configuración existe
    if not os.path.exists(config_path):
        print(f"🛑 ERROR: No se encuentra el archivo de configuración '{config_path}'.")
        print("Asegúrate de que el archivo exista en la raíz del proyecto.")
        return

    try:
        # Inicializar y ejecutar el gestor de estrategias
        manager = StrategyManager(
            config_path=config_path,
            api_key=api_key,
            api_secret=api_secret
        )
        manager.run_forever(interval_seconds=60) # Ejecuta la lógica cada 60 segundos

    except Exception as e:
        print(f"Ha ocurrido un error fatal: {e}")
        # Aquí se podría añadir una notificación por Telegram del error
    finally:
        print("El bot ha finalizado su ejecución.")
