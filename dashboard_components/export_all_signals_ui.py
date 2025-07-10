import streamlit as st
from datetime import datetime

def render_export_all_signals_section(df, selected_file):
    with st.expander("📤 Exportar señales mostradas", expanded=False):
        st.subheader("📤 Exportar señales mostradas")
        if df.empty:
            st.warning("No hay datos disponibles para exportar.")
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"export_{selected_file}_{timestamp}.csv"
        csv_export = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Descargar archivo CSV",
            data=csv_export,
            file_name=file_name,
            mime="text/csv"
        )