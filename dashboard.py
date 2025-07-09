import streamlit as st
import pandas as pd
import glob
import os
import plotly.graph_objects as go
import atexit
import asyncio
import time
from modules.data_fetcher import get_price_data
from modules.analyzer import analyze, generate_signal_label
from modules.telegram_utils import send_telegram_message
from modules.utils import ensure_directories_exist, get_current_timestamp, load_symbol_map

# --- Inicialización de carpetas y archivos JSON requeridos ---
import os
import json

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
import platform
import streamlit.components.v1 as components

def get_system_theme():
    import streamlit_javascript as st_js
    js_code = "window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches"
    result = st_js.st_javascript(js_code)
    return "Oscuro" if result else "Claro"

if 'tema_automatico' not in st.session_state:
    st.session_state.tema_automatico = get_system_theme()

# Opcional: puedes reemplazar el bloque if con la siguiente lógica
css_theme = theme if theme in ["Claro", "Oscuro"] else st.session_state.tema_automatico
load_css("styles/theme.css")  # si ambos temas están en un solo CSS

# --- Modo Autoactualización ---
import streamlit_autorefresh

# --- Autoactualización del dashboard ---
autorefresh = st.checkbox("🔄 Autoactualizar dashboard cada 60 segundos", value=False)
if autorefresh:
    streamlit_autorefresh.st_autorefresh(interval=60 * 1000, key="datarefresh")


# Buscar los archivos CSV generados por el bot
csv_files = sorted(glob.glob("top_signals_*.csv"), reverse=True)

if not csv_files:
    st.warning("No se encontraron archivos de señales exportadas.")
    st.stop()

 # Seleccionar el archivo más reciente
selected_file = st.selectbox("Selecciona un archivo de señales:", csv_files)

# Validación del archivo seleccionado
if selected_file and not selected_file.endswith(".csv"):
    st.error("El archivo seleccionado no es un archivo CSV válido.")
    st.stop()

if selected_file not in csv_files:
    st.error("El archivo seleccionado no está en la lista de archivos válidos.")
    st.stop()

# Mostrar la fecha de creación del archivo seleccionado
if os.path.exists(selected_file):
    creation_time = os.path.getctime(selected_file)
    import datetime
    formatted_date = datetime.datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M:%S")
    st.caption(f"🕒 Fecha de creación del archivo seleccionado: {formatted_date}")

import os

# Nuevo bloque para leer el archivo CSV con manejo robusto de errores
try:
    df = pd.read_csv(selected_file)

    if df.empty or df.columns.size == 0:
        st.error("⚠️ El archivo seleccionado está vacío o no contiene columnas válidas.")
        st.stop()

except Exception as e:
    st.error(f"❌ Error al leer el archivo: {e}")
    st.stop()

# Mostrar título y descripción
st.markdown(f"## 📊 Dashboard de Señales - {selected_file}")
st.markdown("ℹ️ Usa los filtros y controles para explorar las señales de trading más recientes.")

# Validar columnas esperadas
expected_columns = ["Coin", "Date", "Price", "RSI", "MACD", "Signal", "Trend", "Golden Triangle", "Volume"]
missing_columns = [col for col in expected_columns if col not in df.columns]
if missing_columns:
    st.warning(f"⚠️ Faltan las siguientes columnas esperadas en el archivo: {', '.join(missing_columns)}")


#
#
# --- Resumen general de señales ---
with st.expander("🔢 Resumen general de señales", expanded=False):
    total_signals = df.shape[0]
    st.metric("📈 Total de señales en el archivo", total_signals)

with st.expander("🧩 Configuración de Filtros Personalizados", expanded=False):
    st.subheader("🧩 Configuración de Filtros Personalizados")

    filtros_path = "config_filtros.json"
    import json

    # Inicialización segura de variables usando session_state
    if 'signal_filter' not in st.session_state:
        st.session_state.signal_filter = "Todas"
    if 'rsi_min' not in st.session_state:
        st.session_state.rsi_min = 0
    if 'rsi_max' not in st.session_state:
        st.session_state.rsi_max = 100
    if 'macd_min' not in st.session_state:
        st.session_state.macd_min = float(df['MACD'].min()) if 'MACD' in df.columns and not df['MACD'].isna().all() else 0.0
    if 'macd_max' not in st.session_state:
        st.session_state.macd_max = float(df['MACD'].max()) if 'MACD' in df.columns and not df['MACD'].isna().all() else 1.0

    # Convertir la columna 'Signal' a valores numéricos
    df['Signal_num'] = pd.to_numeric(df['Signal'], errors='coerce')

    if 'macd_sig_min' not in st.session_state:
        st.session_state.macd_sig_min = float(df['Signal_num'].min()) if 'Signal_num' in df.columns and not df['Signal_num'].isna().all() else 0.0
    if 'macd_sig_max' not in st.session_state:
        st.session_state.macd_sig_max = float(df['Signal_num'].max()) if 'Signal_num' in df.columns and not df['Signal_num'].isna().all() else 1.0
    if 'search_term' not in st.session_state:
        st.session_state.search_term = ""
    if 'page_size' not in st.session_state:
        st.session_state.page_size = 10

    # Variables ya inicializadas
    signal_filter = st.session_state.signal_filter
    rsi_min = st.session_state.rsi_min
    rsi_max = st.session_state.rsi_max
    macd_min = st.session_state.macd_min
    macd_max = st.session_state.macd_max
    macd_sig_min = st.session_state.macd_sig_min
    macd_sig_max = st.session_state.macd_sig_max
    search_term = st.session_state.search_term
    page_size = st.session_state.page_size

    current_filters = {
        "signal_filter": signal_filter,
        "rsi_min": rsi_min,
        "rsi_max": rsi_max,
        "macd_min": macd_min,
        "macd_max": macd_max,
        "macd_sig_min": macd_sig_min,
        "macd_sig_max": macd_sig_max,
        "search_term": search_term,
        "page_size": page_size
    }

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Guardar configuración actual"):
            try:
                with open(filtros_path, "w") as f:
                    json.dump(current_filters, f)
                st.success("Configuración guardada correctamente.")
            except Exception as e:
                st.error(f"No se pudo guardar la configuración: {e}")

    with col2:
        if os.path.exists(filtros_path):
            if st.button("📥 Cargar configuración guardada"):
                try:
                    with open(filtros_path, "r") as f:
                        saved_filters = json.load(f)
                    signal_filter = saved_filters.get("signal_filter", "Todas")
                    rsi_min = saved_filters.get("rsi_min", 0)
                    rsi_max = saved_filters.get("rsi_max", 100)
                    macd_min = saved_filters.get("macd_min", float(df['macd'].min()))
                    macd_max = saved_filters.get("macd_max", float(df['macd'].max()))
                    macd_sig_min = saved_filters.get("macd_sig_min", float(df['macd_signal'].min()))
                    macd_sig_max = saved_filters.get("macd_sig_max", float(df['macd_signal'].max()))
                    search_term = saved_filters.get("search_term", "")
                    page_size = saved_filters.get("page_size", 10)
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"No se pudo cargar la configuración: {e}")

    # Paginación y búsqueda
    search_term = st.text_input("🔎 Buscar por nombre de criptomoneda:", value=search_term)
    page_size = st.slider("🔢 Resultados por página:", 5, 50, page_size)

    filtered_df = df[df['Coin'].str.contains(search_term, case=False)] if search_term else df


# Filtro por tipo de señal
with st.expander("📍 Filtrar por tipo de señal", expanded=False):
    st.subheader("📍 Filtrar por tipo de señal")
    signal_filter = st.selectbox("Tipo de señal:", ["Todas", "Dorada", "Muerte", "Neutra"], index=["Todas", "Dorada", "Muerte", "Neutra"].index(signal_filter) if signal_filter in ["Todas", "Dorada", "Muerte", "Neutra"] else 0)

    if signal_filter != "Todas":
        if signal_filter == "Dorada":
            filtered_df = filtered_df[filtered_df['Signal'].str.contains("Dorada", case=False, na=False)]
        elif signal_filter == "Muerte":
            filtered_df = filtered_df[filtered_df['Signal'].str.contains("Muerte", case=False, na=False)]
        elif signal_filter == "Neutra":
            filtered_df = filtered_df[~filtered_df['Signal'].str.contains("Dorada|Muerte", case=False, na=False)]

# --- Filtro por umbrales de RSI ---
if 'RSI' in filtered_df.columns:
    with st.expander("📉 Filtrar por RSI", expanded=False):
        st.subheader("📉 Filtrar por RSI")
        rsi_min, rsi_max = st.slider("Selecciona el rango de RSI:", 0, 100, (rsi_min, rsi_max))
        filtered_df = filtered_df[(filtered_df['RSI'] >= rsi_min) & (filtered_df['RSI'] <= rsi_max)]

# --- Filtro por umbrales de MACD ---
if 'MACD' in filtered_df.columns:
    with st.expander("📉 Filtrar por MACD", expanded=False):
        st.subheader("📉 Filtrar por MACD")
        macd_min, macd_max = st.slider(
            "Selecciona el rango de MACD:",
            float(filtered_df['MACD'].min()),
            float(filtered_df['MACD'].max()),
            (macd_min, macd_max)
        )
        filtered_df = filtered_df[(filtered_df['MACD'] >= macd_min) & (filtered_df['MACD'] <= macd_max)]

# --- Filtro por umbrales de MACD Signal ---
if 'Signal_num' in filtered_df.columns:
    with st.expander("📉 Filtrar por MACD Signal", expanded=False):
        st.subheader("📉 Filtrar por MACD Signal")
        macd_sig_min, macd_sig_max = st.slider(
            "Selecciona el rango de MACD Signal:",
            float(filtered_df['Signal_num'].min()),
            float(filtered_df['Signal_num'].max()),
            (macd_sig_min, macd_sig_max)
        )
        filtered_df = filtered_df[(filtered_df['Signal_num'] >= macd_sig_min) & (filtered_df['Signal_num'] <= macd_sig_max)]

# --- Filtro por volumen ---
if 'Volume' in filtered_df.columns or 'volume' in filtered_df.columns:
    with st.expander("📊 Filtrar por Volumen", expanded=False):
        st.subheader("📊 Filtrar por Volumen")
        volumen_col = 'Volume' if 'Volume' in filtered_df.columns else 'volume'
        volumen_min = float(filtered_df[volumen_col].min())
        volumen_max = float(filtered_df[volumen_col].max())
        volumen_slider_min, volumen_slider_max = st.slider(
            "Selecciona el rango de volumen:",
            min_value=volumen_min,
            max_value=volumen_max,
            value=(volumen_min, volumen_max)
        )
        filtered_df = filtered_df[
            (filtered_df[volumen_col] >= volumen_slider_min) &
            (filtered_df[volumen_col] <= volumen_slider_max)
        ]

# --- Resumen estadístico de indicadores ---
with st.expander("📈 Resumen estadístico de indicadores", expanded=False):
    st.subheader("📈 Resumen estadístico de indicadores")
    expected_cols = ['Price', 'RSI', 'MACD', 'Signal_num', 'Volume']
    existing_cols = [col for col in expected_cols if col in filtered_df.columns]

    if existing_cols:
        stats_df = filtered_df[existing_cols].describe().T
        stats_df = stats_df[['mean', 'std', 'min', 'max']]
        stats_df.columns = ['Promedio', 'Desviación Std', 'Mínimo', 'Máximo']
        st.dataframe(stats_df)
        # Mostrar valores seleccionados de filtros
        st.markdown("### 📌 Valores seleccionados en filtros:")
        st.markdown(f"- RSI: {rsi_min} - {rsi_max}")
        st.markdown(f"- MACD: {macd_min:.4f} - {macd_max:.4f}")
        st.markdown(f"- MACD Signal: {macd_sig_min:.4f} - {macd_sig_max:.4f}")
        if 'volumen_slider_min' in locals() and 'volumen_slider_max' in locals():
            st.markdown(f"- Volumen: {volumen_slider_min:.2f} - {volumen_slider_max:.2f}")

        # Exportar valores seleccionados como CSV
        import io
        resumen_filtros = pd.DataFrame({
            "Indicador": ["RSI", "MACD", "MACD Signal"] + (["Volumen"] if 'volumen_slider_min' in locals() else []),
            "Mínimo": [rsi_min, macd_min, macd_sig_min] + ([volumen_slider_min] if 'volumen_slider_min' in locals() else []),
            "Máximo": [rsi_max, macd_max, macd_sig_max] + ([volumen_slider_max] if 'volumen_slider_max' in locals() else [])
        })

        filtro_csv = resumen_filtros.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="💾 Exportar valores de filtros como CSV",
            data=filtro_csv,
            file_name="resumen_filtros.csv",
            mime="text/csv"
        )
    else:
        st.warning("Ninguna de las columnas esperadas está presente en el DataFrame.")

total_rows = filtered_df.shape[0]
total_pages = (total_rows // page_size) + int(total_rows % page_size > 0)
if total_pages > 0:
    page = st.number_input("📄 Página:", min_value=1, max_value=total_pages, step=1)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    st.dataframe(filtered_df.iloc[start_idx:end_idx])
else:
    st.warning("No hay resultados para mostrar.")

# Exportar datos filtrados como CSV
with st.expander("📤 Exportar búsqueda filtrada", expanded=False):
    st.subheader("📤 Exportar búsqueda filtrada")
    # Asegurar que start_idx y end_idx estén definidos
    if 'start_idx' not in locals():
        start_idx = 0
    if 'end_idx' not in locals():
        end_idx = page_size
    # Añadir bloque de texto con los filtros aplicados antes de generar el CSV exportado
    # Determinar el rango de volumen actual, si existe
    if 'volumen_slider_min' in locals() and 'volumen_slider_max' in locals():
        volume_min = volumen_slider_min
        volume_max = volumen_slider_max
    elif 'Volume' in filtered_df.columns or 'volume' in filtered_df.columns:
        volumen_col = 'Volume' if 'Volume' in filtered_df.columns else 'volume'
        volume_min = float(filtered_df[volumen_col].min())
        volume_max = float(filtered_df[volumen_col].max())
    else:
        volume_min = ""
        volume_max = ""
    filter_metadata = [
        "\n# Filtros aplicados",
        "Indicador,Mínimo,Máximo",
        f"RSI,{rsi_min},{rsi_max}",
        f"MACD,{macd_min},{macd_max}",
        f"MACD Signal,{macd_sig_min},{macd_sig_max}",
        f"Volumen,{volume_min},{volume_max}"
    ]
    filter_metadata_str = "\n".join(filter_metadata)
    csv_data = filtered_df.iloc[start_idx:end_idx].to_csv(index=False)
    full_csv = f"{csv_data}\n{filter_metadata_str}"
    filtered_csv_export = full_csv.encode('utf-8')
    st.download_button(
        label="💾 Descargar búsqueda actual como CSV",
        data=filtered_csv_export,
        file_name=f"busqueda_filtrada_{selected_file}",
        mime="text/csv"
    )

# Guardar búsqueda filtrada como reporte predefinido
with st.expander("📝 Guardar búsqueda como reporte", expanded=False):
    st.subheader("📝 Guardar búsqueda como reporte")
    reporte_nombre = st.text_input("Nombre del reporte:", value=f"reporte_{selected_file.replace('.csv','')}")
    if st.button("📁 Guardar reporte"):
        report_dir = "reportes"
        os.makedirs(report_dir, exist_ok=True)
        
        base_path = os.path.join(report_dir, f"{reporte_nombre}.csv")
        version = 1
        report_path = base_path

        while os.path.exists(report_path):
            version += 1
            report_path = os.path.join(report_dir, f"{reporte_nombre}_v{version}.csv")

        filtered_df.iloc[start_idx:end_idx].to_csv(report_path, index=False)
        st.success(f"Reporte guardado en {report_path}")

# Exportar tabla como CSV
with st.expander("📤 Exportar señales mostradas", expanded=False):
    st.subheader("📤 Exportar señales mostradas")
    csv_export = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="💾 Descargar archivo CSV",
        data=csv_export,
        file_name=f"export_{selected_file}",
        mime="text/csv"
    )


st.subheader("⚔️ Comparador Técnico entre Criptomonedas")
coins_to_compare = st.multiselect("Selecciona criptomonedas para comparar sus indicadores técnicos:", df['Coin'].unique())

if coins_to_compare:
    fig_compare_tech = go.Figure()
    for coin in coins_to_compare:
        try:
            # Usar función importada para obtener datos de precios
            data = get_price_data(coin)
            from ta.trend import EMAIndicator
            if not data.empty:
                data['ema50'] = EMAIndicator(close=data['Price'], window=50).ema_indicator()
                fig_compare_tech.add_trace(go.Scatter(
                    x=data.index,
                    y=data['ema50'],
                    mode='lines',
                    name=f"{coin} - EMA50"
                ))
        except Exception as e:
            st.warning(f"No se pudieron cargar los datos técnicos de {coin}: {e}")

    fig_compare_tech.update_layout(
        title="Comparación de EMA50 entre criptomonedas",
        xaxis_title="Fecha",
        yaxis_title="EMA50",
        height=500,
        legend=dict(orientation="h"),
    )
    st.plotly_chart(fig_compare_tech, use_container_width=True)

# Visualizar indicadores por moneda
with st.expander("📌 Comparar múltiples criptomonedas", expanded=False):
    st.subheader("📌 Comparar múltiples criptomonedas")

    selected_coins = st.multiselect("Selecciona criptomonedas para comparar precios:", df['Coin'].unique())

    if selected_coins:
        st.subheader("📊 Comparación de precios entre criptomonedas")
        fig_compare = go.Figure()

        for coin in selected_coins:
            try:
                # Usar función importada para obtener datos de precios
                coin_data = get_price_data(coin)
                if not coin_data.empty:
                    fig_compare.add_trace(go.Scatter(
                        x=coin_data.index,
                        y=coin_data['Price'],
                        mode='lines',
                        name=coin
                    ))
            except Exception as e:
                st.warning(f"No se pudieron cargar los datos de {coin}: {e}")

        fig_compare.update_layout(
            title="Comparación de precios históricos",
            xaxis_title="Fecha",
            yaxis_title="Precio (USD)",
            height=500,
            legend=dict(orientation="h"),
        )

        st.plotly_chart(fig_compare, use_container_width=True)

    # El selectbox y todo lo que sigue debe estar dentro del expander
    selected_coin = st.selectbox("Selecciona una criptomoneda para ver detalles:", df['Coin'].unique())

# Cargar los datos históricos de esa moneda
try:
    # Usar función importada para obtener datos de precios
    data = get_price_data(selected_coin)
    from ta.trend import EMAIndicator
    if data.empty:
        st.error(f"No se encontraron datos históricos para {selected_coin}.")
        st.stop()

    data['ema50'] = EMAIndicator(close=data['Price'], window=50).ema_indicator()
    data['ema200'] = EMAIndicator(close=data['Price'], window=200).ema_indicator()

    # Usar función importada para analizar los datos
    signals, last = analyze(data)

    st.subheader(f"📈 Gráfico técnico para {selected_coin.upper()}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Price'], mode='lines', name='Precio'))
    fig.add_trace(go.Scatter(x=data.index, y=data['ema50'], mode='lines', name='EMA50'))
    fig.add_trace(go.Scatter(x=data.index, y=data['ema200'], mode='lines', name='EMA200'))
    st.plotly_chart(fig, use_container_width=True)

    # Tabla de cambios porcentuales recientes
    st.subheader("📊 Cambios porcentuales recientes")
    try:
        pct_change_7d = data['Price'].pct_change(periods=7).iloc[-1] * 100
        pct_change_30d = data['Price'].pct_change(periods=30).iloc[-1] * 100
        pct_change_90d = data['Price'].pct_change(periods=90).iloc[-1] * 100

        col1, col2, col3 = st.columns(3)
        col1.metric("📅 7 días", f"{pct_change_7d:.2f}%")
        col2.metric("📅 30 días", f"{pct_change_30d:.2f}%")
        col3.metric("📅 90 días", f"{pct_change_90d:.2f}%")
    except Exception as e:
        st.warning(f"No se pudieron calcular los cambios porcentuales: {e}")

    # Gráfico de velas japonesas
    st.subheader("📊 Gráfico de Velas Japonesas (OHLC)")
    try:
        if all(col in data.columns for col in ['open', 'high', 'low', 'close']):
            fig_candlestick = go.Figure(data=[go.Candlestick(
                x=data.index,
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                name=selected_coin.upper()
            )])
            fig_candlestick.update_layout(
                title=f"Gráfico de Velas - {selected_coin.upper()}",
                xaxis_title="Fecha",
                yaxis_title="Precio (USD)",
                height=500
            )
            st.plotly_chart(fig_candlestick, use_container_width=True)
        else:
            st.info("Los datos OHLC (open, high, low, close) no están disponibles para mostrar velas japonesas.")
    except Exception as e:
        st.warning(f"No se pudo generar el gráfico de velas japonesas: {e}")

    # Gráfico de RSI
    st.subheader("📊 RSI a lo largo del tiempo")
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI'))
    fig_rsi.add_hline(y=70, line_dash="dot", line_color="red", annotation_text="Sobrecompra", annotation_position="top left")
    fig_rsi.add_hline(y=30, line_dash="dot", line_color="green", annotation_text="Sobreventa", annotation_position="bottom left")
    st.plotly_chart(fig_rsi, use_container_width=True)

    # Gráfico de MACD
    st.subheader("📊 MACD vs Señal")
    fig_macd = go.Figure()
    fig_macd.add_trace(go.Scatter(x=data.index, y=data['MACD'], mode='lines', name='MACD'))
    fig_macd.add_trace(go.Scatter(x=data.index, y=data['Signal'], mode='lines', name='Signal'))
    st.plotly_chart(fig_macd, use_container_width=True)

    # Gráfico de Volumen (si los datos contienen volumen)
    if 'volume' in data.columns:
        st.subheader("📊 Volumen de trading")
        fig_vol = go.Figure()
        fig_vol.add_trace(go.Bar(x=data.index, y=data['volume'], name='Volumen'))
        st.plotly_chart(fig_vol, use_container_width=True)

    # Gráfico de precio con bandas de Bollinger si existen
    if 'bollinger_h' in data.columns and 'bollinger_l' in data.columns:
        st.subheader("📊 Bandas de Bollinger")
        fig_boll = go.Figure()
        fig_boll.add_trace(go.Scatter(x=data.index, y=data['Price'], mode='lines', name='Precio'))
        fig_boll.add_trace(go.Scatter(x=data.index, y=data['bollinger_h'], mode='lines', name='Bollinger Alta', line=dict(dash='dot')))
        fig_boll.add_trace(go.Scatter(x=data.index, y=data['bollinger_l'], mode='lines', name='Bollinger Baja', line=dict(dash='dot')))
        st.plotly_chart(fig_boll, use_container_width=True)

    # Gráfico combinado RSI + MACD + Precio (+ Volumen si existe)
    st.subheader("📊 Vista combinada: Precio + RSI + MACD" + (" + Volumen" if 'Volume' in data.columns or 'volume' in data.columns else ""))
    fig_combined = go.Figure()

    # Precio
    fig_combined.add_trace(go.Scatter(x=data.index, y=data['Price'], mode='lines', name='Precio', yaxis="y1"))
    
    # RSI
    fig_combined.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI', yaxis="y2"))

    # MACD
    fig_combined.add_trace(go.Scatter(x=data.index, y=data['MACD'], mode='lines', name='MACD', yaxis="y3"))
    fig_combined.add_trace(go.Scatter(x=data.index, y=data['Signal'], mode='lines', name='Signal', yaxis="y3"))

    # Volumen, si existe
    if 'Volume' in data.columns:
        fig_combined.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volumen', yaxis="y4", opacity=0.3))
    elif 'volume' in data.columns:
        fig_combined.add_trace(go.Bar(x=data.index, y=data['volume'], name='Volumen', yaxis="y4", opacity=0.3))

    # Layout con eje de volumen si existe
    layout_dict = dict(
        yaxis=dict(title="Precio", side="left"),
        yaxis2=dict(title="RSI", overlaying="y", side="right"),
        yaxis3=dict(title="MACD", anchor="free", overlaying="y", side="right", position=1.15),
        legend=dict(orientation="h"),
        margin=dict(t=50, b=50),
        height=600
    )
    if 'Volume' in data.columns or 'volume' in data.columns:
        layout_dict['yaxis4'] = dict(title="Volumen", anchor="x", overlaying="y", side="right", position=1.25, showgrid=False)
    fig_combined.update_layout(**layout_dict)

    st.plotly_chart(fig_combined, use_container_width=True)

    import io
    from plotly.io import write_image

    # Exportar fig_combined como imagen (PNG)
    combined_buffer = io.BytesIO()
    fig_combined.write_image(combined_buffer, format="png")
    combined_buffer.seek(0)
    st.download_button(
        label="📥 Descargar gráfico combinado como PNG",
        data=combined_buffer,
        file_name=f"{selected_coin}_grafico_combinado.png",
        mime="image/png"
    )

    # Exportar fig_combined como SVG
    fig_combined.write_image("/tmp/combined_chart.svg", format="svg")
    with open("/tmp/combined_chart.svg", "rb") as svg_file:
        st.download_button(
            label="📄 Descargar gráfico combinado como SVG",
            data=svg_file,
            file_name=f"{selected_coin}_grafico_combinado.svg",
            mime="image/svg+xml"
        )

    # Exportar fig_combined como PDF
    try:
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            write_image(fig_combined, tmpfile.name, format="pdf")
            tmpfile.seek(0)
            st.download_button(
                label="📄 Descargar gráfico combinado como PDF",
                data=tmpfile.read(),
                file_name=f"{selected_coin}_grafico_combinado.pdf",
                mime="application/pdf"
            )
    except Exception as e:
        st.warning(f"No se pudo generar el PDF del gráfico combinado: {e}")

    # Exportar fig_combined como HTML
    html_buffer = io.StringIO()
    fig_combined.write_html(html_buffer)
    html_bytes = html_buffer.getvalue().encode()
    st.download_button(
        label="🌐 Descargar gráfico combinado como HTML",
        data=html_bytes,
        file_name=f"{selected_coin}_grafico_combinado.html",
        mime="text/html"
    )

    # Exportar fig_combined como JSON
    json_buffer = io.StringIO()
    fig_combined.write_json(json_buffer)
    json_bytes = json_buffer.getvalue().encode()
    st.download_button(
        label="📄 Descargar gráfico combinado como JSON",
        data=json_bytes,
        file_name=f"{selected_coin}_grafico_combinado.json",
        mime="application/json"
    )

    # Exportar fig_combined como archivo Plotly .pkl (pickle)
    import pickle
    pkl_buffer = io.BytesIO()
    pickle.dump(fig_combined, pkl_buffer)
    pkl_buffer.seek(0)
    st.download_button(
        label="🧪 Descargar gráfico combinado como PKL",
        data=pkl_buffer,
        file_name=f"{selected_coin}_grafico_combinado.pkl",
        mime="application/octet-stream"
    )

    import io
    from PIL import Image

    buffer = io.BytesIO()
    fig.write_image(buffer, format="png")
    # Exportar también como SVG
    fig.write_image("/tmp/technical_chart.svg", format="svg")
    buffer.seek(0)

    st.download_button(
        label="📥 Descargar gráfico como imagen PNG",
        data=buffer,
        file_name=f"{selected_coin}_grafico.png",
        mime="image/png"
    )

    # Botón para descargar SVG
    with open("/tmp/technical_chart.svg", "rb") as svg_file:
        st.download_button(
            label="📄 Descargar gráfico como SVG",
            data=svg_file,
            file_name=f"{selected_coin}_grafico.svg",
            mime="image/svg+xml"
        )

    # Exportar gráfico como PDF
    import tempfile
    from plotly.io import write_image

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            write_image(fig, tmpfile.name, format="pdf")
            tmpfile.seek(0)
            st.download_button(
                label="📄 Descargar gráfico como PDF",
                data=tmpfile.read(),
                file_name=f"{selected_coin}_grafico.pdf",
                mime="application/pdf"
            )
    except Exception as e:
        st.warning(f"No se pudo generar el PDF del gráfico: {e}")

    st.subheader("📉 Indicadores")
    st.metric("RSI", f"{last['RSI']:.2f}")
    st.metric("MACD", f"{last['MACD']:.4f}")
    st.metric("MACD Signal", f"{last['Signal']:.4f}")
    if "Dorad" in signals[0]:
        st.success(signals[0])
    elif "Muerte" in signals[0]:
        st.error(signals[0])
    else:
        st.warning(signals[0])
except Exception as e:
    st.error(f"No se pudo cargar los datos de {selected_coin}: {e}")

with st.expander("🔗 Correlación entre Criptomonedas", expanded=False):
    st.subheader("🔗 Correlación entre Criptomonedas")

    correlation_df = None

    try:
        selected_corr_coins = st.multiselect("Selecciona criptomonedas para calcular correlación:", df['Coin'].unique())

        if selected_corr_coins:
            price_data = {}
            for coin in selected_corr_coins:
                try:
                    data = get_price_data(coin)
                    if not data.empty:
                        price_data[coin] = data['Price']
                except Exception as e:
                    st.warning(f"No se pudo obtener datos de {coin} para la correlación: {e}")

            if price_data:
                combined_df = pd.DataFrame(price_data)
                correlation_df = combined_df.corr()

                st.subheader("📊 Mapa de calor de correlación")
                fig_corr = go.Figure(data=go.Heatmap(
                    z=correlation_df.values,
                    x=correlation_df.columns,
                    y=correlation_df.index,
                    colorscale='RdBu',
                    zmin=-1,
                    zmax=1,
                    colorbar=dict(title="Correlación")
                ))
                fig_corr.update_layout(
                    title="Correlación de precios entre criptomonedas",
                    height=600
                )
                st.plotly_chart(fig_corr, use_container_width=True)
    except Exception as e:
        st.warning(f"No se pudo calcular la correlación: {e}")

#
# --- Generación de reportes por lotes ---
st.subheader("🧰 Generar reportes por lotes")

st.markdown("Esta herramienta permite generar y guardar automáticamente reportes por tipo de señal para el archivo seleccionado.")

if st.button("🚀 Generar reportes por lotes"):
    lotes_dir = "reportes_lotes"
    os.makedirs(lotes_dir, exist_ok=True)

    timestamp = get_current_timestamp()
    reporte_base = selected_file.replace(".csv", f"_lote_{timestamp}")

    grupos = {
        "Dorada": filtered_df[filtered_df['Signal'].str.contains("Dorada", case=False, na=False)],
        "Muerte": filtered_df[filtered_df['Signal'].str.contains("Muerte", case=False, na=False)],
        "Neutra": filtered_df[~filtered_df['Signal'].str.contains("Dorada|Muerte", case=False, na=False)]
    }

    generados = []
    for tipo, grupo_df in grupos.items():
        if not grupo_df.empty:
            nombre_archivo = f"{reporte_base}_{tipo.lower()}.csv"
            ruta_archivo = os.path.join(lotes_dir, nombre_archivo)
            grupo_df.to_csv(ruta_archivo, index=False)
            generados.append(nombre_archivo)

    if generados:
        st.success("Se generaron los siguientes reportes:")
        for archivo in generados:
            st.write(f"📁 {archivo}")
    else:
        st.warning("No se generó ningún archivo, ya que no había datos disponibles por tipo de señal.")

 # --- Vista cronológica de señales ---
st.subheader("📆 Evolución cronológica de señales")

try:
    historical_data = []
    for file in csv_files:
        try:
            df_temp = pd.read_csv(file)
            if {'Coin', 'Signal'}.issubset(df_temp.columns):
                df_temp['archivo'] = os.path.basename(file)
                df_temp['fecha'] = pd.to_datetime(file.split("_")[-1].replace(".csv", ""), format="%Y-%m-%d_%H-%M-%S", errors='coerce')
                historical_data.append(df_temp[['fecha', 'Coin', 'Signal']])
        except Exception as e:
            st.warning(f"Error leyendo archivo {file}: {e}")

    if historical_data:
        hist_df = pd.concat(historical_data)
        hist_df = hist_df.dropna(subset=['fecha'])

        grouped = hist_df.groupby(['fecha', 'signal']).size().reset_index(name='conteo')

        fig_timeline = go.Figure()
        for signal_type in grouped['signal'].unique():
            df_type = grouped[grouped['signal'] == signal_type]
            fig_timeline.add_trace(go.Bar(
                x=df_type['fecha'],
                y=df_type['conteo'],
                name=signal_type
            ))

        fig_timeline.update_layout(
            title="Cantidad de señales por tipo a lo largo del tiempo",
            xaxis_title="Fecha",
            yaxis_title="Cantidad de señales",
            barmode='stack',
            height=500
        )

        st.plotly_chart(fig_timeline, use_container_width=True)
    else:
        st.info("No se encontraron datos históricos suficientes para mostrar evolución cronológica.")
except Exception as e:
    st.warning(f"No se pudo generar la vista cronológica: {e}")

# Visor de reportes guardados

# --- Sistema de favoritos ---
st.header("⭐ Lista de Criptomonedas Favoritas")
import json

fav_file = "favoritas.json"
if os.path.exists(fav_file):
    with open(fav_file, "r") as f:
        favoritas = json.load(f)
else:
    favoritas = []

favoritas = set(favoritas)  # asegurarse de que sea un conjunto

all_coins = df['Coin'].unique().tolist()
selected_favs = st.multiselect("Selecciona tus criptos favoritas:", all_coins, default=list(favoritas))

if st.button("✅ Guardar favoritas"):
    with open(fav_file, "w") as f:
        json.dump(selected_favs, f)
    st.success("Favoritas guardadas correctamente")

if selected_favs:
    st.subheader("📌 Criptos favoritas seleccionadas")
    st.write(selected_favs)
st.header("📚 Reportes Guardados")
report_dir = "reportes"
if not os.path.exists(report_dir):
    st.info("No hay reportes guardados aún.")
else:
    report_files = sorted(glob.glob(os.path.join(report_dir, "*.csv")))
    if not report_files:
        st.info("No hay reportes guardados aún.")
    else:
        selected_report = st.selectbox("Selecciona un reporte guardado:", report_files)
        import datetime
        creation_time = os.path.getctime(selected_report)
        formatted_date = datetime.datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M:%S")
        st.caption(f"🕒 Fecha de creación: {formatted_date}")
        df_report = pd.read_csv(selected_report)
        st.dataframe(df_report, use_container_width=True)

        # Comparación visual de precios desde reporte guardado
        st.subheader("📌 Comparar criptomonedas del reporte")

        selected_coins_report = st.multiselect("Selecciona criptomonedas del reporte para comparar precios:", df_report['Coin'].unique())

        if selected_coins_report:
            fig_compare_report = go.Figure()
            for coin in selected_coins_report:
                try:
                    # Usar función importada para obtener datos de precios
                    data = get_price_data(coin)
                    if not data.empty:
                        fig_compare_report.add_trace(go.Scatter(
                            x=data.index,
                            y=data['Price'],
                            mode='lines',
                            name=coin
                        ))
                except Exception as e:
                    st.warning(f"No se pudieron cargar los datos de {coin}: {e}")

            fig_compare_report.update_layout(
                title="Comparación de precios históricos (reporte)",
                xaxis_title="Fecha",
                yaxis_title="Precio (USD)",
                height=500,
                legend=dict(orientation="h"),
            )
            st.plotly_chart(fig_compare_report, use_container_width=True)

        # Botón para visualizar el gráfico técnico del reporte
        if st.button("📈 Ver gráfico técnico de monedas en este reporte"):
            st.subheader("📊 Gráficos técnicos desde el reporte guardado")
            from ta.trend import EMAIndicator
            for coin in df_report['Coin'].unique():
                st.markdown(f"### {coin.upper()}")
                try:
                    # Usar función importada para obtener datos de precios
                    data = get_price_data(coin)
                    if data.empty:
                        st.warning(f"No se encontraron datos históricos para {coin}.")
                        continue

                    data['ema50'] = EMAIndicator(close=data['Price'], window=50).ema_indicator()
                    data['ema200'] = EMAIndicator(close=data['Price'], window=200).ema_indicator()

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=data.index, y=data['Price'], mode='lines', name='Precio'))
                    fig.add_trace(go.Scatter(x=data.index, y=data['ema50'], mode='lines', name='EMA50'))
                    fig.add_trace(go.Scatter(x=data.index, y=data['ema200'], mode='lines', name='EMA200'))

                    fig.update_layout(height=400, margin=dict(t=30, b=30))
                    st.plotly_chart(fig, use_container_width=True)

                except Exception as e:
                    st.warning(f"No se pudo cargar {coin}: {e}")

        # Opción para descargar nuevamente
        st.download_button(
            label="💾 Descargar reporte como CSV",
            data=df_report.to_csv(index=False).encode("utf-8"),
            file_name=os.path.basename(selected_report),
            mime="text/csv"
        )

# Confirmar eliminación del reporte
        st.subheader("🗑️ Eliminar reporte")
        if st.checkbox(f"Confirmar eliminación de {os.path.basename(selected_report)}"):
            if st.button("❌ Eliminar reporte"):
                try:
                    os.remove(selected_report)
                    st.success(f"Reporte eliminado correctamente: {selected_report}")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"No se pudo eliminar el archivo: {e}")

# --- Guardar comparación combinada ---
st.subheader("📌 Guardar comparación combinada")
if 'multi_files' in locals() and 'df_combined' in locals() and multi_files and not df_combined.empty:
    nombre_comparacion = st.text_input("📝 Nombre del archivo combinado:", value="comparacion_combined.csv")
    if st.button("💾 Guardar comparación"):
        combinados_dir = "comparaciones"
        os.makedirs(combinados_dir, exist_ok=True)
        ruta_final = os.path.join(combinados_dir, nombre_comparacion)
        version = 1
        while os.path.exists(ruta_final):
            base, ext = os.path.splitext(nombre_comparacion)
            ruta_final = os.path.join(combinados_dir, f"{base}_v{version}{ext}")
            version += 1
        df_combined.to_csv(ruta_final, index=False)
        st.success(f"Comparación guardada en {ruta_final}")
# --- Comparador Multiarchivo ---
st.header("📁 Comparador Multiarchivo")

st.markdown("Selecciona múltiples archivos de señales para comparar la evolución de señales por criptomoneda.")

multi_files = st.multiselect("Selecciona archivos:", csv_files)

if multi_files:
    combined_data = []
    for file in multi_files:
        try:
            df_temp = pd.read_csv(file)
            if {'Coin', 'Signal'}.issubset(df_temp.columns):
                df_temp['archivo'] = os.path.basename(file)
                df_temp['fecha'] = pd.to_datetime(file.split("_")[-1].replace(".csv", ""), format="%Y-%m-%d_%H-%M-%S", errors='coerce')
                combined_data.append(df_temp[['fecha', 'Coin', 'Signal']])
        except Exception as e:
            st.warning(f"No se pudo procesar {file}: {e}")

    if combined_data:
        df_combined = pd.concat(combined_data).dropna(subset=['fecha'])

        st.subheader("📊 Tabla combinada de señales")
        st.dataframe(df_combined, use_container_width=True)

        st.subheader("📈 Tendencia de señales por criptomoneda")
        grouped = df_combined.groupby(['fecha', 'Coin', 'Signal']).size().reset_index(name='conteo')

        fig_multi = go.Figure()
        for coin in grouped['Coin'].unique():
            for sig in grouped['Signal'].unique():
                subset = grouped[(grouped['Coin'] == coin) & (grouped['Signal'] == sig)]
                if not subset.empty:
                    fig_multi.add_trace(go.Scatter(
                        x=subset['fecha'],
                        y=subset['conteo'],
                        mode='lines+markers',
                        name=f"{coin} - {sig}"
                    ))

        fig_multi.update_layout(
            title="Tendencia de señales por criptomoneda",
            xaxis_title="Fecha",
            yaxis_title="Conteo de señales",
            height=600,
            legend=dict(orientation="h")
        )

        st.plotly_chart(fig_multi, use_container_width=True)
    else:
        st.info("No se encontraron datos suficientes para comparar múltiples archivos.")

# --- Resumen total de señales por criptomoneda ---
st.subheader("📊 Resumen total de señales por criptomoneda")

if multi_files and 'df_combined' in locals() and not df_combined.empty:
    resumen = df_combined.groupby(['Coin', 'Signal']).size().unstack(fill_value=0)
    resumen['Total'] = resumen.sum(axis=1)
    resumen = resumen.sort_values('Total', ascending=False)
    st.dataframe(resumen)

# --- Visualización de señales por criptomoneda seleccionada ---
if multi_files and 'df_combined' in locals() and not df_combined.empty:
    st.subheader("🔍 Evolución de señales por criptomoneda seleccionada")

    coin_selected_for_signal = st.selectbox("Selecciona una criptomoneda:", sorted(df_combined['Coin'].unique()))

    if coin_selected_for_signal:
        df_coin = df_combined[df_combined['Coin'] == coin_selected_for_signal]
        trend_df = df_coin.groupby(['fecha', 'Signal']).size().reset_index(name='conteo')

        fig = go.Figure()
        for signal in trend_df['Signal'].unique():
            df_signal = trend_df[trend_df['Signal'] == signal]
            fig.add_trace(go.Scatter(
                x=df_signal['fecha'],
                y=df_signal['conteo'],
                mode='lines+markers',
                name=signal
            ))

        fig.update_layout(
            title=f"Evolución de señales para {coin_selected_for_signal}",
            xaxis_title="Fecha",
            yaxis_title="Cantidad de señales",
            height=500,
            legend=dict(orientation="h")
        )
        st.plotly_chart(fig, use_container_width=True)

# --- Información de la versión ---
st.markdown("---")
st.caption("🛠️ Versión de la aplicación: 1.0.0")
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
import psutil
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