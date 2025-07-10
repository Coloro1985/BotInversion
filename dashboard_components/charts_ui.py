import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def validar_columnas_esperadas(df, columnas_requeridas):
    """Verifica que el DataFrame contenga todas las columnas requeridas."""
    return columnas_requeridas.issubset(df.columns)

def filtrar_por_fecha(df, rango_fechas):
    """Filtra el DataFrame por el rango de fechas especificado."""
    fecha_inicio, fecha_fin = pd.to_datetime(rango_fechas[0]), pd.to_datetime(rango_fechas[1])
    return df[(df['Date'] >= fecha_inicio) & (df['Date'] <= fecha_fin)]

def render_comparative_charts(df):
    columnas_requeridas = {'Coin', 'Price', 'Date'}
    if not validar_columnas_esperadas(df, columnas_requeridas):
        st.warning("⚠️ El DataFrame debe contener las columnas 'Coin', 'Price' y 'Date'.")
        return

    # Asegura que la columna 'Date' esté en formato datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])

    st.subheader("📈 Comparación rápida de precios")

    # Filtro por rango de fechas
    min_date, max_date = df['Date'].min(), df['Date'].max()
    rango_fechas = st.date_input(
        "Selecciona el rango de fechas:",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # Validación de rango de fechas seleccionado
    if (isinstance(rango_fechas, list) and len(rango_fechas) == 2):
        if rango_fechas[0] > rango_fechas[1]:
            st.error("❌ La fecha de inicio no puede ser mayor que la fecha de fin.")
            return
        if rango_fechas[0] < min_date or rango_fechas[1] > max_date:
            st.error(f"❌ El rango de fechas debe estar entre {min_date.date()} y {max_date.date()}.")
            return
        df = filtrar_por_fecha(df, rango_fechas)

    # Selección de criptomonedas
    monedas_seleccionadas = st.multiselect("Selecciona criptomonedas para comparar precios:", df['Coin'].unique())

    if not monedas_seleccionadas:
        st.warning("⚠️ Debes seleccionar al menos una criptomoneda para comparar.")

    if monedas_seleccionadas:
        fig = go.Figure()
        for moneda in monedas_seleccionadas:
            datos_moneda = df[df['Coin'] == moneda]
            if datos_moneda.empty:
                continue
            fig.add_trace(go.Scatter(
                x=datos_moneda['Date'],
                y=datos_moneda['Price'],
                mode='lines+markers',
                name=moneda
            ))

        # Escala logarítmica opcional
        if st.checkbox("📐 Usar escala logarítmica en eje Y"):
            fig.update_yaxes(type="log")

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
        st.success("✅ Gráfico generado correctamente.")