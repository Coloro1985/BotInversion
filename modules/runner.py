# modules/runner.py
import time
from datetime import datetime
import traceback
import pandas as pd
import os
from dotenv import load_dotenv
from binance.client import Client

# ✅ 1. Importar la configuración
import config 

from modules.utils import guardar_historial, limpiar_archivos_csv, exportar_resultados_csv
from modules.logger import configurar_logger
from modules.analyzer import analyze_coin
from modules.telegram_utils import send_telegram_message
from modules.strategies.momentum import check_price_alerts
from modules.utils import load_symbol_map
from modules.data_fetcher import format_klines, get_historical_klines, get_top_cryptos # Asegúrate de importar get_top_cryptos

load_dotenv()
logger = configurar_logger()

SYMBOL_MAP = load_symbol_map()
binance_client = Client(api_key=os.getenv("BINANCE_API_KEY"), api_secret=os.getenv("BINANCE_SECRET_KEY"))
RUN_ANALYSIS = True

def run_bot():
    global RUN_ANALYSIS
    if not RUN_ANALYSIS:
        logger.info("⏸️ Análisis pausado.")
        return
    logger.info(f"\n🔄 Ejecutando análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    mostrar_balance()

def mostrar_balance():
    top_signals = []
    
    # ✅ 2. Usar la configuración para obtener las monedas
    # La función get_top_cryptos no la tenías en tu runner.py anterior, la añadimos para que sea configurable
    logger.info(f"Obteniendo las {config.CRYPTO_LIMIT} principales criptomonedas...")
    coins_to_analyze = get_top_cryptos(limit=config.CRYPTO_LIMIT)
    
    for crypto in coins_to_analyze:
        symbol = crypto.get('symbol', 'N/A').upper()
        # Adaptar el símbolo al formato que usa Binance (ej. 'BTCUSDT')
        binance_symbol = f"{symbol}USDT"

        try:
            time.sleep(0.5)
            # ✅ 3. Usar la configuración para obtener los datos históricos
            klines = get_historical_klines(binance_symbol, config.KLINE_INTERVAL, config.KLINE_PERIOD)
            
            if not klines:
                logger.warning(f"No se obtuvieron klines para {binance_symbol}. Saltando.")
                continue

            df = format_klines(klines)
            if 'close' not in df.columns or df.empty:
                logger.warning(f"No hay datos válidos para {symbol}. Saltando.")
                continue
                
            signal = analyze_coin(symbol, crypto.get('name'), df)
            
            if not signal: # Si el análisis devuelve un diccionario vacío
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

            # ✅ 4. Usar la configuración para decidir si se envía el mensaje
            if config.TELEGRAM_ENABLED and ("Triángulo Dorado" in signal.get("Signal", "") or "Triángulo de Muerte" in signal.get("Signal", "")):
                message = f"""📊 {symbol} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
💰 Precio: ${signal.get("Price", 0):.2f}
📉 RSI: {signal.get("RSI", 0):.2f} | MACD: {signal.get("MACD", 0):.4f} | Signal: {signal.get("macd_signal", 0):.4f}
🔔 {signal.get("Signal", "")}
"""
                logger.info(message)
                send_telegram_message(message)
        except Exception as e:
            logger.error(f"❌ Error procesando {symbol}: {e}")
            traceback.print_exc()

    # ✅ 5. Usar la configuración para limitar las mejores señales
    top_signals_sorted = sorted([s for s in top_signals if s.get('RSI') is not None and s.get('RSI') > 0], key=lambda x: x['RSI'])[:config.TOP_SIGNALS_LIMIT]

    if not any("Triángulo Dorado" in entry.get('Signal', '') for entry in top_signals):
        logger.warning("⚠️ No se encontraron señales de Triángulo Dorado en esta ejecución.")

    for entry in top_signals_sorted:
        logger.info(f"""📊 {entry['Coin'].upper()} - {entry['Date']}
💰 Precio: ${entry.get('Price', 0):.2f}
📉 RSI: {entry.get('RSI', 0):.2f} | MACD: {entry.get('MACD', 0):.4f}
🔔 {entry.get('Signal', '')}
""")

    df_to_export = pd.DataFrame(top_signals_sorted)
    exportar_resultados_csv(df_to_export, output_dir="reports")
    
    # La limpieza de archivos y la comprobación de alertas se mantienen igual
    limpiar_archivos_csv("logs/historial")
    
    # NOTA: La función check_price_alerts puede necesitar ajustes si no usa símbolos de Binance (ej. BTCUSDT)
    # Por ahora, la dejamos como está.
    # alerts = check_price_alerts(coins, SYMBOL_MAP, binance_client)
    # if alerts:
    #     for alert in alerts:
    #         logger.warning(f"🚨 Alerta de Precio: {alert}")