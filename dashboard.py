import os
import glob
import json
import time
import atexit
import asyncio
from datetime import datetime
import platform
import psutil

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
import streamlit_autorefresh
import streamlit_javascript as st_js

from modules.analyzer import analyze, generate_signal_label
from modules.data_fetcher import get_price_data
from modules.telegram_utils import send_telegram_message
from modules.utils import (
    ensure_directories_exist,
    exportar_resultados_csv,
    get_current_timestamp,
    load_symbol_map
)

from dashboard_components.chart_export_ui import render_chart_export_section
from dashboard_components.charts_ui import render_comparative_charts
from dashboard_components.correlation_ui import render_correlation_section
from dashboard_components.export_all_signals_ui import render_export_all_signals_section
from dashboard_components.export_utils import build_filtered_csv_export, render_export_filtered_csv_button
from dashboard_components.favorites_ui import render_favorites_section
from dashboard_components.filters_ui import render_filters_section
from dashboard_components.historical_timeline_ui import render_historical_timeline
from dashboard_components.technical_chart_ui import render_technical_analysis_section
from dashboard_components.report_charts_ui import render_technical_charts_from_report
from dashboard_components.multi_file_comparator import render_multi_file_comparator
from dashboard_components.reporting_ui import render_reporting_tools
from dashboard_components.saved_reports_ui import render_saved_reports_view
from dashboard_components.signal_summary_ui import render_signal_summary_section


# Usar función utilitaria para asegurar directorios
ensure_directories_exist()

# Crear archivos JSON necesarios si no existen
config_filtros_path = "config_filtros.json"
favoritas_path = "favoritas.json"

if not os.path.exists(config_filtros_path):
    with open(config_filtros_path, "w", encoding="utf-8") as f:
        json.dump({}, f, indent=4)

if not os.path.exists(favoritas_path):
    with open(favoritas_path, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)


st.set_page_config(layout="wide")

# --- Cargar estilos CSS según tema ---
def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.sidebar.markdown("🎨 **Tema de la app**")
theme = st.sidebar.radio("Selecciona un tema:", ["Claro", "Oscuro"], horizontal=True)

# --- Detección de tema del sistema operativo ---

def get_system_theme():
    js_code = "window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches"
    result = st_js.st_javascript(js_code)
    return "Oscuro" if result else "Claro"

if 'tema_automatico' not in st.session_state:
    st.session_state.tema_automatico = get_system_theme()

# Opcional: puedes reemplazar el bloque if con la siguiente lógica
css_theme = theme if theme in ["Claro", "Oscuro"] else st.session_state.tema_automatico
load_css("styles/theme.css")  # si ambos temas están en un solo CSS

# --- Modo Autoactualización ---

# --- Autoactualización del dashboard ---
autorefresh = st.checkbox("🔄 Autoactualizar dashboard cada 60 segundos", value=False)
if autorefresh:
    streamlit_autorefresh.st_autorefresh(interval=60 * 1000, key="datarefresh")


# Buscar los archivos CSV generados por el bot
csv_files = sorted(glob.glob(os.path.join("reports", "top_signals_*.csv")), reverse=True)

if not csv_files:
    st.info("ℹ️ No hay archivos de señales disponibles aún.\n\nPara generar reportes, ejecuta primero el bot principal que genera los archivos en la carpeta `reports`.")
    st.stop()

# Seleccionar el archivo más reciente
selected_report_file = st.selectbox("Selecciona un archivo de señales:", csv_files)

# Validar y cargar el archivo CSV seleccionado
df_full = None
if selected_report_file and selected_report_file.endswith(".csv") and os.path.exists(selected_report_file):
    try:
        df_full = pd.read_csv(selected_report_file)

        if df_full.empty or df_full.columns.size == 0:
            st.error("⚠️ El archivo seleccionado está vacío o no contiene columnas válidas.")
            st.stop()

        creation_time = os.path.getctime(selected_report_file)
        formatted_date = datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M:%S")
        st.caption(f"🕒 Fecha de creación del archivo seleccionado: {formatted_date}")

    except Exception as e:
        st.error(f"❌ Error al leer el archivo: {e}")
        st.stop()
else:
    st.error("❌ El archivo seleccionado no es válido o no se encuentra.")
    st.stop()

# Mostrar título y descripción
st.markdown(f"## 📊 Dashboard de Señales - {selected_report_file}")
st.markdown("ℹ️ Usa los filtros y controles para explorar las señales de trading más recientes.")

# Validar columnas esperadas
expected_columns = ["Coin", "Date", "Price", "RSI", "MACD", "Signal", "Trend", "Golden Triangle", "Volume"]
missing_columns = [col for col in expected_columns if col not in df_full.columns]
if missing_columns:
    st.warning(f"⚠️ Faltan las siguientes columnas esperadas en el archivo: {', '.join(missing_columns)}")

st.sidebar.markdown("🧭 **Navegación**")
secciones = [
    "Resumen de Señales",
    "Filtros y Reportes",
    "Comparativa de Criptomonedas",
    "Análisis Técnico",
    "Correlación",
    "Reportes Guardados",
    "Favoritos",
    "Gráficos del Reporte",
    "Comparación de Archivos",
    "Exportar Señales",
    "Exportar Gráfico Individual"
]
seccion_seleccionada = st.sidebar.radio("Selecciona una sección:", secciones)

page_size = 25  # Número de filas por página

if seccion_seleccionada == "Resumen de Señales":
    render_signal_summary_section(df_full)

if seccion_seleccionada == "Filtros y Reportes":
    filtered_df, rsi_min, rsi_max, macd_min, macd_max, macd_sig_min, macd_sig_max, volumen_slider_min, volumen_slider_max = render_filters_section(df_full)
    selected_coin = st.selectbox("Selecciona una criptomoneda:", sorted(df_full["Coin"].unique()))
    render_reporting_tools(filtered_df, selected_report_file)
    total_rows = filtered_df.shape[0]
    total_pages = (total_rows // page_size) + int(total_rows % page_size > 0)
    if total_pages > 0:
        page = st.number_input("📄 Página:", min_value=1, max_value=total_pages, step=1)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        st.dataframe(filtered_df.iloc[start_idx:end_idx])
    else:
        st.warning("No hay resultados para mostrar.")

    with st.expander("📤 Exportar búsqueda filtrada", expanded=False):
        render_export_filtered_csv_button(filtered_df)

if seccion_seleccionada == "Comparativa de Criptomonedas":
    render_comparative_charts(df_full)

if seccion_seleccionada == "Análisis Técnico":
    selected_coin = st.selectbox("Selecciona una criptomoneda:", sorted(df_full["Coin"].unique()))
    render_technical_analysis_section(selected_coin, df_full)

if seccion_seleccionada == "Correlación":
    selected_coin = st.selectbox("Selecciona una criptomoneda:", sorted(df_full["Coin"].unique()))
    render_correlation_section(df_full, selected_coin)

if seccion_seleccionada == "Reportes Guardados":
    filtered_df, rsi_min, rsi_max, macd_min, macd_max, macd_sig_min, macd_sig_max, volumen_slider_min, volumen_slider_max = render_filters_section(df_full)
    render_saved_reports_view(filtered_df, selected_report_file)

if seccion_seleccionada == "Favoritos":
    render_favorites_section(df_full)

if seccion_seleccionada == "Gráficos del Reporte":
    render_technical_charts_from_report(df_full)

if seccion_seleccionada == "Comparación de Archivos":
    render_multi_file_comparator()

if seccion_seleccionada == "Exportar Señales":
    render_export_all_signals_section(df_full, selected_report_file)

if seccion_seleccionada == "Exportar Gráfico Individual":
    selected_coin = st.selectbox("Selecciona una criptomoneda:", sorted(df_full["Coin"].unique()))
    render_chart_export_section(selected_coin, df_full)

render_historical_timeline(csv_files)

# --- Información de la versión ---
st.markdown("---")
st.caption("🛠️ Versión de la aplicación: 1.1.0")
st.markdown("---")
st.caption("🧠 Asistente de inversión potenciado por IA - Desarrollado por Claudio Esteffan")
st.caption("📬 Para sugerencias o mejoras, contáctame en claudio.esteffan@gmail.com")

# Mostrar tiempo de ejecución
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

end_time = time.time()
elapsed = end_time - st.session_state.start_time
st.caption(f"⏱️ Tiempo de ejecución: {elapsed:.2f} segundos")

# Mostrar consumo estimado de memoria
process = psutil.Process(os.getpid())
mem_info = process.memory_info()
mem_used_mb = mem_info.rss / (1024 * 1024)
st.caption(f"💾 Memoria usada: {mem_used_mb:.2f} MB")

@atexit.register
def close_event_loop():
    try:
        loop = asyncio.get_event_loop()
        if not loop.is_closed():
            loop.close()
    except Exception:
        pass  # ignora cualquier error silenciosamente