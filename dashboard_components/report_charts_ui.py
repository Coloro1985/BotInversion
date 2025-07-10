

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from modules.data_fetcher import fetch_price_data

def render_technical_charts_from_report(df_report: pd.DataFrame):
    st.subheader("📈 Gráficos Técnicos desde Reporte")

    for coin in df_report['Coin'].unique():
        st.markdown(f"### {coin}")
        try:
            df = fetch_price_data(coin)
            if df is None or df.empty or not all(col in df.columns for col in ['close', 'ema_50', 'ema_200']):
                st.warning(f"No hay suficientes datos técnicos disponibles para {coin}.")
                continue

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df['close'], mode='lines', name='Precio de Cierre'))
            fig.add_trace(go.Scatter(x=df.index, y=df['ema_50'], mode='lines', name='Media Móvil (EMA 50)'))
            fig.add_trace(go.Scatter(x=df.index, y=df['ema_200'], mode='lines', name='Media Móvil (EMA 200)'))
            fig.update_layout(
                title=f"{coin} - Gráfico de Precio y Medias Móviles",
                xaxis_title="Fecha",
                yaxis_title="Precio (USD)",
                template="plotly_white",
                xaxis=dict(showgrid=True),
                yaxis=dict(showgrid=True)
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.exception(f"Ocurrió un error al cargar los datos técnicos para {coin}")