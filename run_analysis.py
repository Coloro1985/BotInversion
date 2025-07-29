# run_analysis.py

import os
from dotenv import load_dotenv
from src.bot.data_fetcher import DataFetcher
from src.bot.analyzer import Analyzer
from src.bot.utils import save_report_to_csv
from src.bot.telegram_utils import send_telegram_message, format_message
from src.bot.adapters.coingecko_adapter import CoinGeckoAdapter
from src.bot.adapters.binance_adapter import BinanceAdapter
import config

def generate_analysis_report():
    """
    Esta función contiene la lógica original de tu bot:
    1. Obtiene las principales criptos.
    2. Descarga sus datos históricos.
    3. Analiza en busca de señales (Cruce Dorado/Muerte).
    4. Guarda el reporte y notifica por Telegram.
    """
    print("🤖 Iniciando análisis de mercado para generar reporte...")
    
    load_dotenv()
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not all([api_key, api_secret, telegram_token, telegram_chat_id]):
        print("🛑 ERROR: Faltan variables de entorno para el análisis (API, Telegram).")
        return

    # Inicializar adaptadores
    coingecko_adapter = CoinGeckoAdapter()
    binance_adapter = BinanceAdapter(api_key, api_secret)
    
    # Inicializar componentes del bot de análisis
    fetcher = DataFetcher(coingecko_adapter=coingecko_adapter, binance_adapter=binance_adapter)
    analyzer = Analyzer()

    try:
        # 1. Obtener monedas y sus datos
        top_coins = fetcher.get_top_coins(limit=config.TOP_N_COINS)
        print(f"Se analizarán las siguientes {len(top_coins)} monedas: {', '.join(top_coins)}")
        all_data = fetcher.get_multiple_klines(top_coins)

        # 2. Analizar datos
        signals = analyzer.analyze_multiple(all_data)

        if not signals:
            print("No se encontraron señales de Cruce Dorado o Cruce de la Muerte en el análisis de hoy.")
            return

        # 3. Guardar y notificar
        report_path = save_report_to_csv(signals)
        print(f"Reporte de señales guardado en: {report_path}")

        # Filtrar y enviar notificaciones importantes
        important_signals = [s for s in signals if s['Signal'] in ["Golden Cross Imminent", "Death Cross Imminent", "Golden Cross Confirmed", "Death Cross Confirmed"]]
        if important_signals:
            message = format_message(important_signals)
            send_telegram_message(telegram_token, telegram_chat_id, f"🔔 ¡Nuevas Alertas de Trading!\n\n{message}")
            print("Notificación de Telegram enviada con las señales más importantes.")

    except Exception as e:
        print(f"Ocurrió un error durante el análisis: {e}")

if __name__ == "__main__":
    generate_analysis_report()