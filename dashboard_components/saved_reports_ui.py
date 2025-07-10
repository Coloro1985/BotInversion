import os
import streamlit as st
import pandas as pd

def render_saved_reports_view(df):
    st.header("📁 Reportes Guardados")

    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        st.info("No hay reportes guardados.")
        return

    report_files = [f for f in os.listdir(reports_dir) if f.endswith(".csv")]
    if not report_files:
        st.info("No se encontraron archivos CSV en la carpeta de reportes.")
        return

    selected_report = st.selectbox("Selecciona un reporte para ver:", report_files)
    if selected_report:
        report_path = os.path.join(reports_dir, selected_report)
        try:
            df_report = pd.read_csv(report_path)
            st.write(f"Mostrando datos del archivo: {selected_report}")
            st.dataframe(df_report)

            # Sección de filtros para el reporte cargado
            with st.expander("🔍 Filtros del reporte cargado"):
                columnas = df_report.columns.tolist()
                columna_seleccionada = st.selectbox("Selecciona una columna para filtrar", columnas)
                texto_filtro = st.text_input("Texto a buscar en la columna seleccionada")

                if texto_filtro:
                    df_filtrado = df_report[df_report[columna_seleccionada].astype(str).str.contains(texto_filtro, case=False, na=False)]
                    st.write(f"Mostrando {len(df_filtrado)} resultados que coinciden con el filtro")
                    st.dataframe(df_filtrado)
        except Exception as e:
            st.error(f"No se pudo cargar el archivo: {e}")
