import os
import telegram
from dotenv import load_dotenv
from modules.logger import configurar_logger

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

telegram_bot = telegram.Bot(token=BOT_TOKEN)

def send_telegram_message(message):
    try:
        telegram_bot.send_message(chat_id=CHAT_ID, text=message)
    except telegram.error.TelegramError as e:
        print(f"Error al enviar mensaje a Telegram: {e}")

def formatear_mensaje(entry):
    return f"""📊 {entry['Coin'].upper()} - {entry['Date']}
💰 Precio: ${entry['Price']:.2f}
📉 RSI: {entry['RSI']:.2f} | MACD: {entry['MACD']:.4f}
🔔 {entry['Signal']}
"""

def iniciar_telegram_bot():
    logger = configurar_logger()
    logger.info("📨 Sistema de Telegram inicializado.")