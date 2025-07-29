import pandas as pd
import pandas_ta as ta

def _calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula y añade los indicadores técnicos al DataFrame.
    """
    if df.empty:
        return df
    
    try:
        df.ta.ema(length=50, append=True)
        df.ta.ema(length=200, append=True)
        df.ta.rsi(append=True)
        df.ta.macd(append=True)
        
        df.rename(columns={
            "EMA_50": "ema50", 
            "EMA_200": "ema200", 
            "RSI_14": "RSI", 
            "MACD_12_26_9": "MACD", 
            "MACDh_12_26_9": "macd_histogram", 
            "MACDs_12_26_9": "macd_signal"
        }, inplace=True)
        
        df.dropna(inplace=True)
    except Exception:
        return pd.DataFrame() # Si falla, devuelve un DF vacío
    
    return df

def _check_signals(df: pd.DataFrame) -> str:
    """
    Revisa las señales de trading. Ahora es más seguro.
    """
    # ✅ PASO 1: Verificar que tenemos los datos necesarios
    required_columns = ['ema50', 'ema200']
    if len(df) < 2 or not all(col in df.columns for col in required_columns):
        return "Datos Insuficientes"

    latest = df.iloc[-1]
    previous = df.iloc[-2]
    
    is_golden_cross = latest['ema50'] > latest['ema200'] and previous['ema50'] <= previous['ema200']
    is_death_cross = latest['ema50'] < latest['ema200'] and previous['ema50'] >= previous['ema200']
    
    if is_golden_cross:
        return "🔼 Cruce Dorado"
    if is_death_cross:
        return "🔽 Cruce de la Muerte"
        
    return "Neutral"

def analyze_coin(symbol: str, name: str, df: pd.DataFrame) -> dict:
    """
    Analiza el DataFrame de una criptomoneda.
    """
    if df.empty:
        return {}

    df_with_indicators = _calculate_indicators(df.copy())
    
    if df_with_indicators.empty:
        return {}
        
    latest_data = df_with_indicators.iloc[-1]
    trade_signal = _check_signals(df_with_indicators)

    result = {
        "Symbol": symbol.upper(),
        "Name": name,
        # ✅ PASO 2: Usar .get() por si alguna columna falta
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