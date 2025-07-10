import streamlit as st
import pandas as pd
import io

def render_chart_export_section(df_filtered, selected_coin):
    st.subheader("📤 Exportar datos de la criptomoneda seleccionada")

    if df_filtered.empty:
        st.warning("⚠️ No hay datos disponibles para exportar.")
        return

    st.markdown("Puedes descargar los datos filtrados de la criptomoneda seleccionada en formato CSV.")

    buffer = io.StringIO()
    df_filtered.to_csv(buffer, index=False)
    buffer.seek(0)

    filename = f"{selected_coin}_filtered_data.csv"

    st.download_button(
        label="📥 Descargar CSV",
        data=buffer,
        file_name=filename,
        mime="text/csv",
    )