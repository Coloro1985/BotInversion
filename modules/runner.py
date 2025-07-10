import time
from datetime import datetime
import traceback
import pandas as pd
from modules.utils import guardar_historial, limpiar_archivos_csv, exportar_resultados_csv
from modules.logger import configurar_logger
from modules.analyzer import analyze
from modules.telegram_utils import send_telegram_message
from modules.strategies.momentum import check_price_alerts
from modules.utils import load_symbol_map
from binance.client import Client
import os
from dotenv import load_dotenv

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
    from modules.analyzer import analyze_coin
    top_signals = []
    coins = list(SYMBOL_MAP.keys())

    from modules.data_fetcher import format_klines, get_historical_klines
    for coin in coins:
        if coin not in SYMBOL_MAP:
            logger.warning(f"{coin} no está en SYMBOL_MAP. Saltando.")
            continue
        try:
            time.sleep(0.2)
            klines = get_historical_klines(SYMBOL_MAP[coin], "1d", "30 day ago UTC")
            df = format_klines(klines)
            if 'close' not in df.columns or df.empty:
                logger.warning(f"No hay datos válidos para {coin}. Saltando.")
                continue
            signal = analyze_coin(coin, coin, df)
            signal_entry = {
                "Coin": coin.upper(),
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Price": signal["Price"],
                "RSI": signal["RSI"],
                "MACD": signal["MACD"],
                "Signal": signal["Signal"],
                "Trend": "Bullish" if signal["ema50"] > signal["ema200"] else "Bearish",
                "Golden Triangle": "Yes" if "Triángulo Dorado" in signal["Signal"] else "No",
                "Volume": signal.get("volume", 0),
            }
            required_keys = ["Coin", "Date", "Price", "RSI", "MACD", "Signal", "Trend", "Golden Triangle", "Volume"]
            if all(k in signal_entry for k in required_keys):
                top_signals.append(signal_entry)
            else:
                logger.info(f"⚠️ Entrada incompleta descartada para {coin}: {signal_entry}")

            guardar_historial(coin, signal_entry, "logs/historial")

            if "Triángulo Dorado" in signal["Signal"] or "Triángulo de Muerte" in signal["Signal"]:
                message = f"""📊 {coin.upper()} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
💰 Precio: ${signal["Price"]:.2f}
📉 RSI: {signal["RSI"]:.2f} | MACD: {signal["MACD"]:.4f} | Signal: {signal["macd_signal"]:.4f}
🔔 {signal["Signal"]}
"""
                logger.info(message)
                send_telegram_message(message)
        except Exception as e:
            logger.error(f"❌ Error analizando {coin}: {e}")
            traceback.print_exc()

    top_signals_sorted = sorted([s for s in top_signals if s.get('RSI') is not None], key=lambda x: x['RSI'])[:15]

    if not any("Triángulo Dorado" in entry['Signal'] for entry in top_signals):
        logger.warning("⚠️ No se encontraron señales de Triángulo Dorado en esta ejecución.")

    for entry in top_signals_sorted:
        logger.info(f"""📊 {entry['Coin'].upper()} - {entry['Date']}
💰 Precio: ${entry['Price']:.2f}
📉 RSI: {entry['RSI']:.2f} | MACD: {entry['MACD']:.4f}
🔔 {entry['Signal']}
""")

    exportar_resultados_csv(top_signals_sorted, output_dir="reports")
    limpiar_archivos_csv("logs/historial")
    alerts = check_price_alerts(coins, SYMBOL_MAP, binance_client)
    if alerts:
        for alert in alerts:
            logger.warning(f"🚨 Alerta de Precio: {alert}")