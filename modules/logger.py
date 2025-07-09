import logging
import os

def configurar_logger(nombre="bot_logger", archivo="logs/execution.log"):
    os.makedirs(os.path.dirname(archivo), exist_ok=True)
    logger = logging.getLogger(nombre)
    logger.setLevel(logging.DEBUG if os.getenv("DEBUG", "false").lower() == "true" else logging.INFO)

    if not logger.handlers:
        fh = logging.FileHandler(archivo)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger