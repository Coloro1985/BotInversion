import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Optional

def render_technical_chart_section(selected_df: pd.DataFrame, selected_coin: Optional[str] = None) -> None:
    st.subheader(f"📊 Gráfico Técnico - {selected_coin.upper()}" if selected_coin else "📊 Gráfico Técnico")

    if selected_df.empty:
        st.warning("No hay datos disponibles para mostrar el gráfico.")
        return

    selected_df = selected_df.sort_values(by='timestamp')

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=selected_df['timestamp'],
        y=selected_df['close'],
        mode='lines',
        name='Precio de Cierre',
        line=dict(color='black')
    ))

    for ema_column, color, dash in [('ema50', 'blue', 'dash'), ('ema200', 'red', 'dot')]:
        if ema_column in selected_df.columns:
            fig.add_trace(go.Scatter(
                x=selected_df['timestamp'],
                y=selected_df[ema_column],
                mode='lines',
                name=ema_column.upper(),
                line=dict(color=color, dash=dash)
            ))

    fig.update_layout(
        title=f"Indicadores Técnicos de {selected_coin.upper() if selected_coin else ''}",
        xaxis_title='Fecha',
        yaxis_title='Precio',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=40, r=40, t=60, b=40),
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    if 'rsi' in selected_df.columns:
        st.subheader("📈 Índice de Fuerza Relativa (RSI)")
        rsi_fig = go.Figure()
        rsi_fig.add_trace(go.Scatter(
            x=selected_df['timestamp'],
            y=selected_df['rsi'],
            mode='lines',
            name='RSI',
            line=dict(color='green')
        ))
        rsi_fig.update_layout(
            xaxis_title='Fecha',
            yaxis_title='RSI',
            height=300,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(rsi_fig, use_container_width=True)

    st.markdown("---")