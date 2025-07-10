import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def render_technical_chart_section(selected_df: pd.DataFrame, selected_coin: str):
    st.subheader(f"📊 Gráfico Técnico - {selected_coin.upper()}")

    if selected_df.empty:
        st.warning("No hay datos disponibles para mostrar el gráfico.")
        return

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=selected_df['timestamp'],
        y=selected_df['close'],
        mode='lines',
        name='Precio de Cierre',
        line=dict(color='black')
    ))

    if 'ema50' in selected_df.columns:
        fig.add_trace(go.Scatter(
            x=selected_df['timestamp'],
            y=selected_df['ema50'],
            mode='lines',
            name='EMA 50',
            line=dict(color='blue', dash='dash')
        ))

    if 'ema200' in selected_df.columns:
        fig.add_trace(go.Scatter(
            x=selected_df['timestamp'],
            y=selected_df['ema200'],
            mode='lines',
            name='EMA 200',
            line=dict(color='red', dash='dot')
        ))

    if 'rsi' in selected_df.columns:
        fig.add_trace(go.Scatter(
            x=selected_df['timestamp'],
            y=selected_df['rsi'],
            mode='lines',
            name='RSI',
            yaxis='y2',
            line=dict(color='green')
        ))

    fig.update_layout(
        title=f"Indicadores Técnicos de {selected_coin.upper()}",
        xaxis_title='Fecha',
        yaxis=dict(title='Precio', side='left'),
        yaxis2=dict(title='RSI', overlaying='y', side='right'),
        legend=dict(x=0, y=1.2, orientation='h'),
        margin=dict(l=40, r=40, t=60, b=40),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)