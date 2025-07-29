import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ✅ Se corrige la ruta del import para que apunte a 'src.bot'
from src.bot.data_fetcher import get_historical_klines, format_klines
import config # Importamos config para usar los parámetros

def render_technical_charts_from_report(df_report: pd.DataFrame):
    st.subheader("📈 Gráficos Técnicos desde Reporte")

    # Usamos un slider para no sobrecargar la pantalla con gráficos
    coin_list = df_report['Coin'].unique()
    selected_coin = st.select_slider("Selecciona una moneda para ver su gráfico:", options=coin_list)

    if selected_coin:
        st.markdown(f"### {selected_coin}")
        try:
            # Obtenemos los datos históricos para el gráfico
            klines = get_historical_klines(
                f"{selected_coin}USDT", 
                config.KLINE_INTERVAL, 
                config.KLINE_PERIOD
            )
            df_klines = format_klines(klines)

            if df_klines.empty:
                st.warning(f"No se pudieron obtener datos históricos para {selected_coin}.")
                return

            fig = go.Figure(data=[go.Candlestick(
                x=pd.to_datetime(df_klines['timestamp'], unit='ms'),
                open=df_klines['open'],
                high=df_klines['high'],
                low=df_klines['low'],
                close=df_klines['close'],
                name='Precio'
            )])
            
            fig.update_layout(
                title=f"{selected_coin} - Gráfico de Velas",
                xaxis_title="Fecha",
                yaxis_title="Precio (USD)",
                xaxis_rangeslider_visible=False # Slider más limpio
            )
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Ocurrió un error al cargar los datos técnicos para {selected_coin}: {e}")