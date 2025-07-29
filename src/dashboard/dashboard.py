import os
import sys
import glob
import json
from datetime import datetime

import pandas as pd
import streamlit as st
import streamlit_autorefresh

# Esta línea es CRUCIAL. Se asegura de que Streamlit encuentre tus módulos en 'src'.
# Debe estar al principio de los imports de tu aplicación.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# =================== BLOQUE DE IMPORTS CORREGIDO ===================
# --- Imports de tu aplicación ---
# Ya no necesitamos la mayoría de los módulos del bot, solo las utilidades si acaso.
from src.bot.utils import ensure_directories_exist

# --- Imports de los componentes del dashboard ---
# Ahora se importan de forma relativa desde la subcarpeta 'components'.
from components.chart_export_ui import render_chart_export_section
from components.charts_ui import render_comparative_charts
from components.correlation_ui import render_correlation_section
from components.export_all_signals_ui import render_export_all_signals_section
from components.favorites_ui import render_favorites_section
from components.filters_ui import render_filters_section
from components.historical_timeline_ui import render_historical_timeline
from components.technical_chart_ui import render_technical_analysis_section
from components.report_charts_ui import render_technical_charts_from_report
from components.multi_file_comparator import render_multi_file_comparator
from components.reporting_ui import render_reporting_tools
from components.saved_reports_ui import render_saved_reports_view
from components.signal_summary_ui import render_signal_summary_section
# =====================================================================

# --- CONFIGURACIÓN INICIAL DE LA PÁGINA ---
st.set_page_config(layout="wide")

# Función para cargar el archivo CSS
def load_css(file_path):
    # Construye la ruta completa desde la ubicación de este archivo
    full_path = os.path.join(os.path.dirname(__file__), file_path)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carga el tema CSS desde la nueva ubicación
load_css("styles/theme.css")


def main_dashboard():
    """
    Función principal que renderiza toda la interfaz del dashboard.
    """
    ensure_directories_exist()

    st.title("📊 Dashboard de Señales de Trading")
    if st.sidebar.checkbox("🔄 Autoactualizar cada 60 segundos"):
        streamlit_autorefresh.st_autorefresh(interval=60 * 1000, key="datarefresh")

    # --- Carga de Datos ---
    # La ruta a los reportes ahora se construye desde la raíz del proyecto
    reports_path = "reports"
    csv_files = sorted(glob.glob(os.path.join(reports_path, "top_signals_*.csv")), reverse=True)

    if not csv_files:
        st.warning("ℹ️ No se encontraron reportes en la carpeta `reports`.")
        st.info("Ejecuta el bot (`python main.py`) para generar los análisis.")
        st.stop()

    selected_report_file = st.sidebar.selectbox("Selecciona un Reporte:", csv_files)

    try:
        df_full = pd.read_csv(selected_report_file)
        if df_full.empty:
            st.error("⚠️ El archivo seleccionado está vacío.")
            st.stop()
    except Exception as e:
        st.error(f"❌ Error al leer el archivo: {e}")
        st.stop()
    
    creation_time = os.path.getctime(selected_report_file)
    formatted_date = datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M:%S")
    st.sidebar.caption(f"Datos del: {formatted_date}")


    # --- Navegación en la Barra Lateral ---
    st.sidebar.title("🧭 Navegación")
    secciones = [
        "Resumen de Señales",
        "Filtros y Reportes",
        "Análisis Técnico Individual",
        # ... (puedes añadir el resto de tus secciones aquí)
    ]
    seccion_seleccionada = st.sidebar.radio("Selecciona una sección:", secciones)

    # --- Renderizado de Secciones ---
    if seccion_seleccionada == "Resumen de Señales":
        render_signal_summary_section(df_full)
    elif seccion_seleccionada == "Filtros y Reportes":
        # Asegúrate de que render_filters_section devuelva solo lo que necesitas
        filtered_df, _, _, _, _, _, _, _, _ = render_filters_section(df_full)
        render_reporting_tools(filtered_df, selected_report_file)
        st.dataframe(filtered_df)
    elif seccion_seleccionada == "Análisis Técnico Individual":
        # Pasamos el dataframe completo para que el componente elija la moneda
        render_technical_analysis_section(df_full)


if __name__ == "__main__":
    main_dashboard()