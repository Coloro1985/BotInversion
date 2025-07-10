import streamlit as st
import pandas as pd
import os

def render_multi_file_comparator(csv_files, reports_dir="reports"):
    st.header("📁 Comparador Multiarchivo")

    if not csv_files:
        st.warning("No hay archivos CSV disponibles para comparar.")
        return

    multi_files = st.multiselect("Selecciona múltiples archivos CSV", options=csv_files)

    if not multi_files:
        st.info("Selecciona al menos un archivo para comparar.")
        return

    data_frames = []
    for file in multi_files:
        file_path = os.path.join(reports_dir, file)
        try:
            df = pd.read_csv(file_path)
            df["source_file"] = file  # Agregar columna de origen
            data_frames.append(df)
        except Exception as e:
            st.error(f"Error al leer {file}: {e}")

    if data_frames:
        df_combined = pd.concat(data_frames, ignore_index=True)
        st.subheader("Vista previa combinada de archivos seleccionados")
        with st.expander("Ver archivos combinados"):
            st.dataframe(df_combined)
            csv = df_combined.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Descargar archivo combinado",
                data=csv,
                file_name="comparacion_archivos.csv",
                mime="text/csv"
            )