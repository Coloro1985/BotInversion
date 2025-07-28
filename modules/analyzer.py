import pandas as pd
import pandas_ta as ta

def _calculate_indicators(df):
    """
    Función privada para calcular y añadir los indicadores técnicos al DataFrame.
    """
    if df.empty:
        return df
    
    # Calcular indicadores usando pandas_ta
    df.ta.ema(length=50, append=True)
    df.ta.ema(length=200, append=True)
    df.ta.rsi(append=True)
    df.ta.macd(append=True)
    
    # Renombrar columnas para consistencia y eliminar valores nulos
    df.rename(columns={"EMA_50": "ema50", "EMA_200": "ema200", "RSI_14": "RSI", "MACD_12_26_9": "MACD", "MACDh_12_26_9": "macd_histogram", "MACDs_12_26_9": "macd_signal"}, inplace=True)
    df.dropna(inplace=True)
    
    return df

def _check_signals(df):
    """
    Función privada para revisar las señales de trading basadas en los indicadores.
    Devuelve un string con la señal encontrada.
    """
    if df.empty:
        return "Sin Datos"

    latest_row = df.iloc[-1]
    previous_row = df.iloc[-2] if len(df) > 1 else latest_row
    
    signal = "Neutral"

    # 1. Señal de Cruce de Medias Móviles (Golden Cross / Death Cross)
    # Golden Cross: EMA50 cruza por ENCIMA de EMA200
    if latest_row['ema50'] > latest_row['ema200'] and previous_row['ema50'] <= previous_row['ema200']:
        signal = "🔼 Triángulo Dorado (Golden Cross)"
    # Death Cross: EMA50 cruza por DEBAJO de EMA200
    elif latest_row['ema50'] < latest_row['ema200'] and previous_row['ema50'] >= previous_row['ema200']:
        signal = "🔽 Triángulo de Muerte (Death Cross)"
        
    # Aquí se podrían añadir más lógicas de señales en el futuro (ej. MACD, RSI)
    
    return signal

def analyze_coin(symbol, name, df):
    """
    Analiza el DataFrame de una criptomoneda para generar una señal de trading.
    
    Args:
        symbol (str): El símbolo de la moneda (ej. 'BTC').
        name (str): El nombre de la moneda (ej. 'Bitcoin').
        df (pd.DataFrame): DataFrame con los datos históricos (OHLCV).

    Returns:
        dict: Un diccionario con los resultados del análisis.
    """
    # Si no hay datos, devolver un diccionario vacío para evitar errores
    if df.empty or len(df) < 2:
        return {}

    # 1. Calcular todos los indicadores necesarios
    df_with_indicators = _calculate_indicators(df.copy())
    
    if df_with_indicators.empty:
        return {}
        
    # 2. Obtener la última fila con datos y precios
    latest_data = df_with_indicators.iloc[-1]
    
    # 3. Revisar si hay señales de compra/venta
    trade_signal = _check_signals(df_with_indicators)

    # 4. Construir el resultado final
    result = {
        "Symbol": symbol.upper(),
        "Name": name,
        "Price": latest_data.get('close', 0),
        "RSI": latest_data.get('RSI', 0),
        "MACD": latest_data.get('MACD', 0),
        "macd_signal": latest_data.get('macd_signal', 0),
        "ema50": latest_data.get('ema50', 0),
        "ema200": latest_data.get('ema200', 0),
        "volume": latest_data.get('volume', 0),
        "Signal": trade_signal
    }
    
    return result
