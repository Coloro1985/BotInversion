import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Optional

# ✅ No necesitamos importar nada de 'src.bot' aquí.
# El componente recibe los datos que necesita y solo se encarga de dibujarlos.

def render_technical_analysis_section(df_full: pd.DataFrame) -> None:
    st.subheader("📊 Análisis Técnico Individual")

    if df_full.empty:
        st.warning("No hay datos disponibles para mostrar.")
        return

    # Creamos un selector para que el usuario elija la moneda
    coin_list = sorted(df_full["Coin"].unique())
    selected_coin = st.selectbox("Selecciona una criptomoneda para analizar:", coin_list)

    if not selected_coin:
        st.stop()

    # Filtramos los datos del reporte para la moneda seleccionada
    coin_data = df_full[df_full['Coin'] == selected_coin].iloc[0]

    # Mostramos el gráfico de precio y EMAs
    st.markdown(f"#### Gráfico de Precio para **{selected_coin}**")
    
    # Creamos un DataFrame simple para el gráfico
    # NOTA: Este gráfico es una simplificación. Para un gráfico real de velas, necesitaríamos
    # llamar a 'get_historical_klines' como en el componente anterior.
    # Por ahora, mostramos la tendencia general.
    
    price_df = pd.DataFrame({
        'Fecha': [pd.to_datetime(coin_data['Date'])],
        'Precio': [coin_data['Price']],
        'EMA50': [coin_data.get('ema50')], # Usamos .get por si no existe
        'EMA200': [coin_data.get('ema200')]
    })

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=price_df['Fecha'], y=price_df['Precio'], mode='lines+markers', name='Precio'))
    if 'EMA50' in price_df:
        fig.add_trace(go.Scatter(x=price_df['Fecha'], y=price_df['EMA50'], mode='lines', name='EMA 50'))
    if 'EMA200' in price_df:
        fig.add_trace(go.Scatter(x=price_df['Fecha'], y=price_df['EMA200'], mode='lines', name='EMA 200'))

    st.plotly_chart(fig, use_container_width=True)
    
    # Mostramos los indicadores clave
    st.markdown("#### Indicadores Clave")
    col1, col2, col3 = st.columns(3)
    col1.metric("Precio", f"${coin_data.get('Price', 0):.2f}")
    col2.metric("RSI", f"{coin_data.get('RSI', 0):.2f}")
    col3.metric("Tendencia", coin_data.get('Trend', 'N/A'))