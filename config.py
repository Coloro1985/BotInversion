# config.py
# Archivo central de configuración para el Bot de Inversión

# --- CONFIGURACIÓN DE ANÁLISIS ---
# Número de las principales criptomonedas a obtener y analizar
CRYPTO_LIMIT = 100 

# Número de las mejores señales a mostrar en el log y exportar
TOP_SIGNALS_LIMIT = 20

# --- CONFIGURACIÓN DE DATOS DE BINANCE ---
# Intervalo de tiempo para las velas (k-lines). Ej: '1m', '5m', '1h', '4h', '1d', '1w'
KLINE_INTERVAL = "1d"

# Período histórico a obtener. Ej: "30 day ago UTC", "1 year ago UTC"
KLINE_PERIOD = "90 day ago UTC"

# --- CONFIGURACIÓN DE TELEGRAM ---
# Activa o desactiva el envío de notificaciones a Telegram
TELEGRAM_ENABLED = True

# Puedes añadir más configuraciones aquí en el futuro