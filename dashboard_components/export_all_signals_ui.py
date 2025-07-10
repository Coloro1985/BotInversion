import streamlit as st

def render_export_all_signals_section(df, selected_file):
    with st.expander("📤 Exportar señales mostradas", expanded=False):
        st.subheader("📤 Exportar señales mostradas")
        csv_export = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Descargar archivo CSV",
            data=csv_export,
            file_name=f"export_{selected_file}",
            mime="text/csv"
        )