import os
import threading
from dotenv import load_dotenv
from bot.strategy_manager import StrategyManager
from webhook_server import run_webhook_server

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
        # Inicializar el gestor de estrategias
        manager = StrategyManager(
            config_path=config_path,
            api_key=api_key,
            api_secret=api_secret
        )

        if not manager.strategies:
            print("No hay estrategias habilitadas en el archivo de configuración. El bot no se iniciará.")
            return


# --- 2. CREACIÓN DE HILOS PARA EJECUCIÓN PARALELA ---
        # Hilo 1: Ejecuta el bucle principal de las estrategias (DCA, Grid, etc.)
        # El 'daemon=True' asegura que el hilo se cierre si el programa principal termina.
        strategy_thread = threading.Thread(target=manager.run_forever, args=(60,), daemon=True)
        
        # Hilo 2: Ejecuta el servidor de webhooks de Flask
        webhook_thread = threading.Thread(target=run_webhook_server, args=(manager,), daemon=True)

        # --- 3. INICIO DE AMBOS HILOS ---
        print("--- Iniciando motor de estrategias ---")
        strategy_thread.start()
        
        print("--- Iniciando servidor de webhooks ---")
        webhook_thread.start()

        # Mantenemos el programa principal vivo esperando que los hilos terminen
        strategy_thread.join()
        webhook_thread.join()

    except KeyboardInterrupt:
        print("\n🛑 Proceso interrumpido por el usuario. Cerrando bot...")
    except Exception as e:
        print(f"Ha ocurrido un error fatal en el runner: {e}")
    finally:
        print("El bot ha finalizado su ejecución.")