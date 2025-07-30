import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import config
from dotenv import load_dotenv
import os

# --- Imports Corregidos ---
# ✅ Importamos la CLASE, no una función
from src.bot.adapters.binance_adapter import BinanceAdapter
from src.bot.data_fetcher import format_klines

def render_technical_charts_from_report(df_report: pd.DataFrame):
    st.subheader("📈 Gráficos Técnicos desde Reporte")

    if df_report.empty:
        st.warning("No hay datos en el reporte para mostrar gráficos.")
        return

    coin_list = df_report['Coin'].unique()
    selected_coin = st.select_slider(
        "Selecciona una moneda del reporte para ver su gráfico:",
        options=coin_list
    )

    if selected_coin:
        st.markdown(f"### {selected_coin}")
        try:
            # --- ✅ Lógica Correcta ---
            # 1. Cargar las claves de API
            load_dotenv()
            api_key = os.getenv("BINANCE_API_KEY")
            api_secret = os.getenv("BINANCE_SECRET_KEY")

            # 2. Crear una instancia del adaptador
            adapter = BinanceAdapter(api_key, api_secret)

            # 3. Llamar al método get_klines en la instancia
            klines = adapter.get_klines(
                symbol=f"{selected_coin}USDT",
                interval=config.KLINE_INTERVAL,
                limit=200 # Usamos un límite fijo para los gráficos
            )
            df_klines = pd.DataFrame(klines) # El adapter ya lo formatea

            if df_klines.empty:
                st.warning(f"No se pudieron obtener datos históricos para {selected_coin}.")
                return

            # Crear gráfico de velas (candlestick)
            fig = go.Figure(data=[go.Candlestick(
                x=pd.to_datetime(df_klines['open_time'], unit='ms'),
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
                xaxis_rangeslider_visible=False
            )
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Ocurrió un error al cargar los datos para {selected_coin}: {e}")