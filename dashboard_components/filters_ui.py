import streamlit as st

def render_filters_section(df):
    st.sidebar.header("🎛️ Filtros de búsqueda")

    # Validación inicial: df vacío o sin columnas esperadas
    if df.empty or not any(col in df.columns for col in ['Coin', 'Trend', 'Golden Triangle']):
        st.sidebar.warning("No hay datos disponibles para filtrar.")
        return df

    if 'Coin' in df.columns:
        unique_coins = sorted(df['Coin'].dropna().unique())
        if len(unique_coins) > 0:
            selected_coins = st.sidebar.multiselect("Criptomonedas:", unique_coins, default=unique_coins)
            df = df[df['Coin'].isin(selected_coins)]

    if 'Trend' in df.columns:
        trend_options = df['Trend'].dropna().unique()
        if len(trend_options) > 0:
            selected_trends = st.sidebar.multiselect("Tendencia:", trend_options, default=trend_options)
            df = df[df['Trend'].isin(selected_trends)]

    if 'Golden Triangle' in df.columns:
        gt_options = df['Golden Triangle'].dropna().unique()
        if len(gt_options) > 0:
            selected_gt = st.sidebar.multiselect("Triángulo Dorado:", gt_options, default=gt_options)
            df = df[df['Golden Triangle'].isin(selected_gt)]

    return df