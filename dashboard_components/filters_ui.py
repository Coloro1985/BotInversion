import streamlit as st


# Filtros individuales extraídos para modularidad y claridad
def filter_by_coin(df):
    if 'Coin' in df.columns:
        unique_coins = sorted(df['Coin'].dropna().unique())
        if unique_coins:
            selected_coins = st.sidebar.multiselect("Criptomonedas:", unique_coins, default=unique_coins)
            return df[df['Coin'].isin(selected_coins)]
    return df

def filter_by_trend(df):
    if 'Trend' in df.columns:
        trend_options = df['Trend'].dropna().unique()
        if trend_options.any():
            selected_trends = st.sidebar.multiselect("Tendencia:", trend_options, default=trend_options)
            return df[df['Trend'].isin(selected_trends)]
    return df

def filter_by_golden_triangle(df):
    if 'Golden Triangle' in df.columns:
        gt_options = df['Golden Triangle'].dropna().unique()
        if gt_options.any():
            selected_gt = st.sidebar.multiselect("Triángulo Dorado:", gt_options, default=gt_options)
            return df[df['Golden Triangle'].isin(selected_gt)]
    return df

def render_filters_section(df):
    st.sidebar.header("🎛️ Filtros de búsqueda")

    if df.empty or not any(col in df.columns for col in ['Coin', 'Trend', 'Golden Triangle']):
        st.sidebar.warning("No hay datos disponibles para filtrar.")
        return df

    df = filter_by_coin(df)
    df = filter_by_trend(df)
    df = filter_by_golden_triangle(df)

    return df