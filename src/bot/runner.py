import time
import os
import traceback
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from binance.client import Client

# Importar nuestros módulos usando la nueva estructura 'src'
import config
from src.bot.logger import configurar_logger
from src.bot.analyzer import analyze_coin
from src.bot.data_fetcher import format_klines, get_top_cryptos
from src.bot.adapters.binance_adapter import get_historical_klines
from src.bot.telegram_utils import send_telegram_message
from src.bot.utils import guardar_historial, limpiar_archivos_csv, exportar_resultados_csv
# from src.strategies.momentum import check_price_alerts # Lo dejamos comentado por ahora

# La única variable global que necesitamos es el logger
logger = configurar_logger()

def run_bot():
    """
    Función principal que orquesta la ejecución del bot.
    """
    logger.info(f"\n🔄 Ejecutando análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # --- Inicialización dentro de la función ---
    # Es mejor práctica inicializar aquí que de forma global
    load_dotenv()
    binance_client = Client(api_key=os.getenv("BINANCE_API_KEY"), api_secret=os.getenv("BINANCE_SECRET_KEY"))
    
    # --- Obtener, analizar y guardar señales ---
    top_signals = []
    
    logger.info(f"Obteniendo las {config.CRYPTO_LIMIT} principales criptomonedas...")
    coins_to_analyze = get_top_cryptos(limit=config.CRYPTO_LIMIT)
    
    for crypto in coins_to_analyze:
        symbol = crypto.get('symbol', 'N/A').upper()
        binance_symbol = f"{symbol}USDT"

        try:
            time.sleep(0.5) # Pausa para no saturar la API
            
            klines = get_historical_klines(binance_symbol, config.KLINE_INTERVAL, config.KLINE_PERIOD)
            if not klines:
                logger.warning(f"No se obtuvieron klines para {binance_symbol}. Saltando.")
                continue

            df = format_klines(klines)
            if df.empty or 'close' not in df.columns:
                logger.warning(f"No hay datos válidos para {symbol}. Saltando.")
                continue
                
            signal = analyze_coin(symbol, crypto.get('name'), df)
            if not signal:
                logger.warning(f"Análisis fallido para {symbol}, no se generó señal.")
                continue

            signal_entry = {
                "Coin": symbol,
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Price": signal.get("Price", 0),
                "RSI": signal.get("RSI", 0),
                "MACD": signal.get("MACD", 0),
                "Signal": signal.get("Signal", ""),
                "Trend": "Bullish" if signal.get("ema50", 0) > signal.get("ema200", 0) else "Bearish",
                "Golden Triangle": "Yes" if "Triángulo Dorado" in signal.get("Signal", "") else "No",
                "Volume": signal.get("volume", 0),
            }
            
            top_signals.append(signal_entry)
            guardar_historial(symbol, signal_entry, "logs/historial")

            if config.TELEGRAM_ENABLED and ("Triángulo Dorado" in signal.get("Signal", "") or "Triángulo de Muerte" in signal.get("Signal", "")):
                message = f"""📊 {symbol} - {signal.get("Signal", "")}
💰 Precio: ${signal.get("Price", 0):.2f}
📉 RSI: {signal.get("RSI", 0):.2f}"""
                logger.info(message)
                send_telegram_message(message)

        except Exception as e:
            logger.error(f"❌ Error procesando {symbol}: {e}")
            traceback.print_exc()

    # --- Procesar y exportar los resultados ---
    if not top_signals:
        logger.warning("No se generaron señales válidas en esta ejecución.")
        return

    top_signals_sorted = sorted([s for s in top_signals if s.get('RSI', 0) > 0], key=lambda x: x['RSI'])[:config.TOP_SIGNALS_LIMIT]
    
    logger.info(f"--- Top {len(top_signals_sorted)} Señales Encontradas ---")
    for entry in top_signals_sorted:
        logger.info(f"📊 {entry['Coin']}: Precio=${entry.get('Price', 0):.2f}, RSI={entry.get('RSI', 0):.2f}, Señal='{entry.get('Signal', '')}'")

    df_to_export = pd.DataFrame(top_signals_sorted)
    exportar_resultados_csv(df_to_export, output_dir="reports")
    limpiar_archivos_csv("logs/historial")