import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def render_correlation_section(df):
    st.subheader("📊 Análisis de Correlación")

    if df is not None and not df.empty:
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        if not numeric_df.empty:
            corr = numeric_df.corr()
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
            st.pyplot(fig)
        else:
            st.warning("No hay columnas numéricas suficientes para analizar la correlación.")
    else:
        st.warning("No se han cargado datos para analizar.")