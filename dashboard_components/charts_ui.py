import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def render_comparative_charts(df):
    st.subheader("📈 Comparación rápida de precios")

    if 'Coin' in df.columns and 'Price' in df.columns:
        # Filtro por rango de fechas
        min_date = df['Date'].min()
        max_date = df['Date'].max()
        date_range = st.date_input("Selecciona el rango de fechas:", [min_date, max_date])

        if isinstance(date_range, list) and len(date_range) == 2:
            df = df[(df['Date'] >= pd.to_datetime(date_range[0])) & (df['Date'] <= pd.to_datetime(date_range[1]))]

        selected_coins = st.multiselect("Selecciona criptomonedas para comparar precios:", df['Coin'].unique())

        if selected_coins:
            fig = go.Figure()
            for coin in selected_coins:
                coin_df = df[df['Coin'] == coin]
                if coin_df.empty:
                    continue
                fig.add_trace(go.Scatter(
                    x=coin_df['Date'],
                    y=coin_df['Price'],
                    mode='lines+markers',
                    name=coin
                ))

            fig.update_layout(
                title="Comparación de precios por criptomoneda",
                xaxis_title="Fecha",
                yaxis_title="Precio (USD)",
                height=500,
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.markdown("---")
            st.plotly_chart(fig, use_container_width=True)