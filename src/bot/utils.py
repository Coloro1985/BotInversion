import os
import csv
from datetime import datetime
import pandas as pd
from .logger import configurar_logger

# (Si alguna de tus funciones de utilidad necesita get_price_data, esta es la forma correcta)
# from .adapters.coingecko_adapter import get_price_data

logger = configurar_logger()

def ensure_directories_exist():
    """Asegura que los directorios para logs y reportes existan."""
    os.makedirs("logs/historial", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

def guardar_historial(coin, data, directory):
    """Guarda una entrada de señal en el archivo CSV histórico de una moneda."""
    filepath = os.path.join(directory, f"{coin.lower()}.csv")
    file_exists = os.path.isfile(filepath)
    
    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def exportar_resultados_csv(df, output_dir="reports"):
    """Exporta un DataFrame a un archivo CSV con un timestamp."""
    if df.empty:
        logger.warning("El DataFrame para exportar está vacío. No se generó el archivo CSV.")
        return
        
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"top_signals_{timestamp}.csv"
    filepath = os.path.join(output_dir, filename)
    
    try:
        df.to_csv(filepath, index=False)
        logger.info(f"Resultados exportados exitosamente a: {filepath}")
    except Exception as e:
        logger.error(f"Error al exportar resultados a CSV: {e}")

def limpiar_archivos_csv(directory, days_to_keep=7):
    """Elimina archivos CSV más antiguos que un número de días especificado."""
    # Esta función puede ser implementada en el futuro si es necesario.
    pass

# Si no usas load_symbol_map, puedes eliminar esta función.
def load_symbol_map(filepath="data/symbol_map.csv"):
    """Carga el mapeo de símbolos desde un archivo CSV."""
    # Como ya no usamos un mapa de símbolos estático, esta función es obsoleta.
    # La mantenemos aquí por si se usa en algún otro lugar, pero podría ser eliminada.
    logger.warning("La función load_symbol_map está obsoleta y podría ser eliminada en futuras versiones.")
    try:
        df = pd.read_csv(filepath)
        return df.set_index('nombre')['símbolo_binance'].to_dict()
    except FileNotFoundError:
        logger.error(f"Archivo de mapa de símbolos no encontrado en {filepath}. Se devolverá un diccionario vacío.")
        return {}

def get_current_timestamp():
    """Devuelve el timestamp actual en formato legible."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")