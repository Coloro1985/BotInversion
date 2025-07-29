import pandas as pd
import pandas_ta as ta

# Nota: No se necesita importar el 'logger' aquí, ya que este módulo no escribe logs.
# Su única tarea es recibir datos, procesarlos y devolver un resultado.

def _calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Función privada para calcular y añadir los indicadores técnicos al DataFrame.
    Usa la librería pandas_ta para eficiencia.
    """
    if df.empty:
        return df
    
    try:
        # Calcular todos los indicadores en una sola pasada
        df.ta.ema(length=50, append=True)
        df.ta.ema(length=200, append=True)
        df.ta.rsi(append=True)
        df.ta.macd(append=True)
        
        # Renombrar columnas para que sean más consistentes y fáciles de usar
        df.rename(columns={
            "EMA_50": "ema50", 
            "EMA_200": "ema200", 
            "RSI_14": "RSI", 
            "MACD_12_26_9": "MACD", 
            "MACDh_12_26_9": "macd_histogram", 
            "MACDs_12_26_9": "macd_signal"
        }, inplace=True)
        
        # Eliminar filas que no tengan todos los datos después de calcular los indicadores
        df.dropna(inplace=True)
    except Exception:
        # Si hay cualquier error en el cálculo, devuelve un DataFrame vacío
        # para que la función principal lo maneje de forma segura.
        return pd.DataFrame()
    
    return df

def _check_signals(df: pd.DataFrame) -> str:
    """
    Función privada para revisar las señales de trading basadas en los indicadores.
    Devuelve un string con la señal encontrada.
    """
    if len(df) < 2:
        return "Datos Insuficientes"

    # Obtener la última y la penúltima fila para detectar cruces
    latest = df.iloc[-1]
    previous = df.iloc[-2]
    
    # Lógica de Cruce Dorado / Muerte (Golden Cross / Death Cross)
    # Un cruce dorado ocurre cuando la media móvil corta (50) cruza POR ENCIMA de la larga (200)
    is_golden_cross = latest['ema50'] > latest['ema200'] and previous['ema50'] <= previous['ema200']
    
    # Un cruce de la muerte es lo opuesto
    is_death_cross = latest['ema50'] < latest['ema200'] and previous['ema50'] >= previous['ema200']
    
    if is_golden_cross:
        return "🔼 Cruce Dorado"
    if is_death_cross:
        return "🔽 Cruce de la Muerte"
        
    # Si no hay cruces, se devuelve una señal neutral.
    # Aquí podrías añadir más lógica en el futuro (ej. señales de RSI o MACD).
    return "Neutral"

def analyze_coin(symbol: str, name: str, df: pd.DataFrame) -> dict:
    """
    Analiza el DataFrame de una criptomoneda para generar una señal de trading.

    Args:
        symbol (str): El símbolo de la moneda (ej. 'BTC').
        name (str): El nombre de la moneda (ej. 'Bitcoin').
        df (pd.DataFrame): DataFrame con los datos históricos (OHLCV).

    Returns:
        dict: Un diccionario con los resultados del análisis, o un diccionario vacío si falla.
    """
    if df.empty:
        return {}

    # 1. Calcular todos los indicadores necesarios
    df_with_indicators = _calculate_indicators(df.copy())
    
    # Si el cálculo de indicadores falló o no hay datos, no continuar
    if df_with_indicators.empty:
        return {}
        
    # 2. Obtener la última fila con datos completos
    latest_data = df_with_indicators.iloc[-1]
    
    # 3. Revisar si hay señales de trading
    trade_signal = _check_signals(df_with_indicators)

    # 4. Construir el diccionario de resultados final
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