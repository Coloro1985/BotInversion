import os
import logging
import time
from datetime import datetime
import pandas as pd


from modules.adapters.coingecko_adapter import get_price_data
from modules.logger import configurar_logger

def load_symbol_map(filepath=None):
    """Carga un archivo CSV que mapea coin_id de CoinGecko a símbolos de Binance."""
    if filepath is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = os.path.join(base_dir, "data", "symbol_map.csv")
    try:
        df = pd.read_csv(filepath)
        return dict(zip(df["coin_id"], df["symbol"]))
    except Exception as e:
        print(f"Error al cargar el symbol_map desde {filepath}: {e}")
        return {}

def ensure_directory_exists(path: str) -> None:
    """Crea el directorio si no existe."""
    if not os.path.exists(path):
        os.makedirs(path)

def ensure_directories_exist(directories: list = None) -> None:
    """Crea los directorios si no existen."""
    if directories is None:
        directories = ["data", "logs", "reports"]
    for path in directories:
        os.makedirs(path, exist_ok=True)

def get_current_timestamp() -> str:
    """Devuelve el timestamp actual con formato legible."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def setup_logger(log_file_path: str) -> logging.Logger:
    """Configura y devuelve un logger."""
    logger = logging.getLogger("CryptoBot")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Evitar duplicar handlers
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

def wait_with_feedback(seconds: int) -> None:
    """Muestra una cuenta regresiva en consola mientras espera."""
    for i in range(seconds, 0, -1):
        print(f"Esperando {i} segundos...", end="\r")
        time.sleep(1)
    print(" " * 30, end="\r")  # Limpia la línea

def guardar_historial(coin: str, data: dict, output_dir: str) -> None:
    """Guarda el historial de una criptomoneda en un archivo CSV individual."""
    if not isinstance(data, dict):
        print(f"[ERROR] El dato proporcionado no es un diccionario. No se guardará el historial de {coin}.")
        return

    columnas_esperadas = ['Coin', 'Date', 'Price', 'RSI', 'MACD', 'Signal', 'Trend', 'Golden Triangle']
    if not all(col in data for col in columnas_esperadas):
        print(f"[ADVERTENCIA] Faltan columnas en los datos de {coin}. No se guardará.")
        return

    os.makedirs(output_dir, exist_ok=True)
    coin_filename = coin.replace(" ", "_").lower() + ".csv"
    df = pd.DataFrame([data])
    df.to_csv(os.path.join(output_dir, coin_filename), index=False)

def limpiar_archivos_csv(folder_path: str) -> None:
    """Elimina archivos CSV que estén vacíos o que no puedan ser leídos como DataFrames."""
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            filepath = os.path.join(folder_path, filename)
            try:
                df = pd.read_csv(filepath)
                if df.empty:
                    os.remove(filepath)
            except Exception:
                os.remove(filepath)

def get_today_date() -> str:
    """Devuelve la fecha actual en formato YYYY-MM-DD"""
    return datetime.today().strftime("%Y-%m-%d")

def prepare_dashboard_data():
    logger = configurar_logger()
    logger.info("Generando datos para el dashboard...")
    symbol_map = load_symbol_map()
    results = []

    from .analyzer import analyze_coin

    for name, symbol in symbol_map.items():
        try:
            df = get_price_data(symbol)
            if df is None or df.empty:
                continue
            df = df.copy()
            result = analyze_coin(name, df)
            results.append(result)
        except Exception as e:
            logger.error(f"Error analizando {name}: {e}")
    
    if not results:
        logger.warning("No se generaron resultados.")
        return
    
    df_results = pd.DataFrame(results)
    df_results['Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    os.makedirs("data", exist_ok=True)
    df_results.to_csv("data/analysis_results.csv", index=False)
    logger.info("Archivo generado: data/analysis_results.csv")

def exportar_resultados_csv(top_signals_sorted):
    if not top_signals_sorted:
        print("⚠️ No se exportaron señales ya que no hay datos disponibles.")
        return
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.abspath(os.path.join(os.path.dirname(base_dir), "reports"))
    os.makedirs(output_dir, exist_ok=True)
    df_export = pd.DataFrame(top_signals_sorted)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = os.path.join(output_dir, f"top_signals_{timestamp}.csv")
    df_export.to_csv(output_path, index=False)
    print(f"📁 Resultados exportados a {output_path}")