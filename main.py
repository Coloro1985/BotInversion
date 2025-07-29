# main.py

import sys
import os

# Esta línea es lo PRIMERO que debe ejecutarse.
# Añade la carpeta raíz del proyecto al 'path' de Python para que pueda encontrar 'src'.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Ahora, importamos solo lo que main.py necesita para arrancar.
from src.bot.runner import run_bot
from src.bot.logger import configurar_logger

# El bloque __name__ == "__main__" es el único punto de entrada de la aplicación.
if __name__ == "__main__":
    
    # 1. Configurar el logger al inicio de todo.
    logger = configurar_logger()
    
    try:
        # 2. Iniciar la ejecución del bot.
        logger.info("🚀 Iniciando Bot de Inversión...")
        run_bot()
        logger.info("✅ Ciclo del bot completado exitosamente.")

    except KeyboardInterrupt:
        # Esto permite detener el bot de forma segura con Ctrl+C
        logger.warning("🛑 Ejecución del bot interrumpida por el usuario.")
        
    except Exception as e:
        # Atrapa cualquier otro error inesperado que pueda ocurrir.
        logger.critical(f"💥 Error fatal en la ejecución principal: {e}", exc_info=True)