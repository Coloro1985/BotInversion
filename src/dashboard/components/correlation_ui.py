import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def render_correlation_section(df):
    st.subheader("📊 Análisis de Correlación")

    if df is None or df.empty:
        st.warning("No se han cargado datos para analizar.")
        return

    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.empty:
        st.warning("No hay columnas numéricas suficientes para analizar la correlación.")
        return

    corr = numeric_df.corr()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        cbar=True,
        square=True,
        linewidths=0.5,
        linecolor="white",
        ax=ax
    )
    ax.set_title("Matriz de Correlación", fontsize=14, pad=12)
    st.pyplot(fig)