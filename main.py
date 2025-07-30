import sys
import os
import time
import schedule

# Esta línea es CRUCIAL para que Python encuentre tus módulos en la carpeta 'src'.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.bot.strategy_manager import StrategyManager
from src.bot.logger import configurar_logger

# Configurar el logger al inicio de todo.
logger = configurar_logger()

def job():
    """
    Función que será ejecutada por el planificador (scheduler).
    """
    logger.info("🚀 Iniciando ciclo de ejecución de estrategias...")
    try:
        manager = StrategyManager('strategies.yaml')
        manager.run_strategies()
        logger.info("✅ Ciclo de estrategias completado exitosamente.")
    except Exception as e:
        logger.error(f"💥 Ocurrió un error durante la ejecución del job: {e}", exc_info=True)


if __name__ == "__main__":
    logger.info("🤖 Bot de Inversión iniciado. Ejecutando el primer ciclo ahora...")
    
    # Ejecuta el job una vez al iniciar
    job()

    # Configura la ejecución periódica (ej. cada hora)
    # Puedes ajustar el tiempo según tus necesidades en config.py o aquí.
    schedule.every(1).hour.do(job)
    
    logger.info("🕒 El bot está en modo de espera, ejecutará las estrategias periódicamente. Presiona Ctrl+C para detener.")

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logger.warning("🛑 Deteniendo el bot...")
            break
