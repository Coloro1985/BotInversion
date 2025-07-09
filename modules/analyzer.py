import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD
from datetime import datetime
from modules.logger import configurar_logger
logger = configurar_logger()


def calculate_rsi(df):
    df = df.copy()
    if 'close' not in df.columns:
        raise ValueError("El DataFrame debe contener la columna 'close'")
    rsi_indicator = RSIIndicator(close=df['close'], window=14)
    df['rsi'] = rsi_indicator.rsi()
    return df

def calculate_macd(df):
    df = df.copy()
    if 'close' not in df.columns:
        raise ValueError("El DataFrame debe contener la columna 'close'")
    macd_indicator = MACD(close=df['close'])
    df['macd'] = macd_indicator.macd()
    df['macd_signal'] = macd_indicator.macd_signal()
    df['macd_diff'] = macd_indicator.macd_diff()
    return df

def calculate_ema(df, period):
    df = df.copy()
    if 'close' not in df.columns:
        raise ValueError("El DataFrame debe contener la columna 'close'")
    df[f'ema{period}'] = df['close'].ewm(span=period, adjust=False).mean()
    return df

def detect_trend(df):
    if 'macd' not in df.columns or 'macd_signal' not in df.columns:
        raise ValueError("El DataFrame debe contener las columnas 'macd' y 'macd_signal'")
    df['trend'] = np.where(df['macd'] > df['macd_signal'], 'bullish', 'bearish')
    return df

def detect_golden_triangle(df):
    required = ['rsi', 'macd', 'macd_signal', 'close', 'bollinger_upper']
    if not all(col in df.columns for col in required):
        raise ValueError(f"El DataFrame debe contener las columnas necesarias: {required}")
    df['golden_triangle'] = np.where(
        (df['rsi'] > 50) & 
        (df['macd'] > df['macd_signal']) & 
        (df['close'] > df['bollinger_upper']),
        True, False)
    return df

def calculate_bollinger_bands(df):
    df = df.copy()
    if 'close' not in df.columns:
        raise ValueError("El DataFrame debe contener la columna 'close'")
    window = 20
    df['bollinger_mid'] = df['close'].rolling(window=window, min_periods=1).mean()
    df['bollinger_std'] = df['close'].rolling(window=window, min_periods=1).std()
    df['bollinger_upper'] = df['bollinger_mid'] + (df['bollinger_std'] * 2)
    df['bollinger_lower'] = df['bollinger_mid'] - (df['bollinger_std'] * 2)
    return df

def detect_signal(df):
    if 'rsi' not in df.columns or 'macd' not in df.columns or 'macd_signal' not in df.columns:
        raise ValueError("El DataFrame debe contener las columnas 'rsi', 'macd' y 'macd_signal'")
    df['signal'] = np.select(
        [
            (df['rsi'] > 70) & (df['macd'] > df['macd_signal']),
            (df['rsi'] < 30) & (df['macd'] < df['macd_signal'])
        ],
        [
            "🔼 Señal de compra",
            "🔽 Señal de venta"
        ],
        default="⏳ Sin señal clara"
    )
    return df

def generate_signal_label(rsi, macd, macd_signal):
    if rsi > 70 and macd > macd_signal:
        return "🔼 Señal fuerte de compra"
    elif 50 < rsi <= 70 and macd > macd_signal:
        return "📈 Tendencia alcista"
    elif rsi < 30 and macd < macd_signal:
        return "🔽 Señal fuerte de venta"
    elif 30 <= rsi < 50 and macd < macd_signal:
        return "📉 Tendencia bajista"
    else:
        return "⏳ Sin señal clara"

def analyze_coin(symbol, name, data):
    if data.empty:
        return {
            'Coin': name,
            'Symbol': symbol,
            'Date': None,
            'Price': None,
            'RSI': None,
            'MACD': None,
            'Signal': None,
            'Trend': None,
            'Golden Triangle': None,
            'ema50': None,
            'ema200': None,
        }
    data = calculate_rsi(data)
    logger.debug(f"{symbol} - Último RSI: {data['rsi'].iloc[-1]}")
    data = calculate_macd(data)
    logger.debug(f"{symbol} - Último MACD: {data['macd'].iloc[-1]}")
    logger.debug(f"{symbol} - Último MACD Signal: {data['macd_signal'].iloc[-1]}")
    data = calculate_ema(data, 50)
    data = calculate_ema(data, 200)
    data = detect_trend(data)
    data = calculate_bollinger_bands(data)
    data = detect_golden_triangle(data)
    data = detect_signal(data)

    signal = generate_signal_label(data['rsi'].iloc[-1], data['macd'].iloc[-1], data['macd_signal'].iloc[-1])
    logger.debug(f"{symbol} - Señal generada: {signal}")

    price = data['close'].iloc[-1] if not data.empty else 0.0
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return {
        'Coin': name,
        'Symbol': symbol,
        'Date': now,
        'Price': price,
        'RSI': data['rsi'].iloc[-1] if 'rsi' in data else None,
        'MACD': data['macd'].iloc[-1] if 'macd' in data else None,
        'Signal': signal,
        'Trend': data['trend'].iloc[-1] if 'trend' in data else None,
        'Golden Triangle': data['golden_triangle'].iloc[-1] if 'golden_triangle' in data else None,
        'ema50': data['ema50'].iloc[-1] if 'ema50' in data else None,
        'ema200': data['ema200'].iloc[-1] if 'ema200' in data else None,
    }

def analyze_dataframe(df_dict):
    results = []
    for symbol, df in df_dict.items():
        name = symbol  # Asumiendo que el nombre es igual al símbolo, puede cambiarse si se dispone de otro dato
        result = analyze_coin(symbol, name, df)
        results.append(result)
    return results

analyze = analyze_coin