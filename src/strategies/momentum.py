import traceback
from ..bot.telegram_utils import send_telegram_message

def check_price_alerts(coins, symbol_map, binance_client):
    try:
        for coin in coins:
            symbol = symbol_map.get(coin.lower())
            if not symbol:
                continue
            klines = binance_client.get_klines(symbol=symbol, interval='1d', limit=2)
            if len(klines) < 2:
                continue
            price_yesterday = float(klines[0][4])
            price_today = float(klines[1][4])
            change = ((price_today - price_yesterday) / price_yesterday) * 100

            if abs(change) >= 5:
                message = f"""📈 ALERTA DE PRECIO ({'🔺' if change > 0 else '🔻'}) - {coin.upper()}
Cambio 24h: {change:.2f}%
Precio actual: ${price_today:.2f}"""
                send_telegram_message(message)
    except Exception as e:
        print(f"❌ Error al verificar alertas de precio: {e}")
        traceback.print_exc()