import streamlit as st
import os
import pandas as pd

def render_reporting_tools(df, selected_file):
    st.markdown("### 💾 Exportar Reporte Filtrado")
    st.markdown("Puedes guardar esta vista como un archivo CSV para su posterior análisis o consulta.")

    if df.empty:
        st.warning("⚠️ No hay datos para guardar.")
        return

    default_name = f"reporte_{selected_file.replace('.csv','')}"
    directorio_reportes = os.path.join(os.getcwd(), "reports")
    os.makedirs(directorio_reportes, exist_ok=True)

    st.markdown("---")
    with st.form("guardar_reporte_form"):
        nombre_archivo = st.text_input("Nombre del archivo:", value=default_name).strip()
        st.markdown("&nbsp;")
        submit_guardar = st.form_submit_button("💾 Guardar como CSV")

        if submit_guardar:
            if not nombre_archivo:
                st.warning("⚠️ El nombre del archivo no puede estar vacío.")
                return

            nombre_archivo = "".join(c for c in nombre_archivo if c.isalnum() or c in ('_', '-')).rstrip()
            nombre_base = os.path.join(directorio_reportes, f"{nombre_archivo}.csv")
            contador = 1
            nombre_final = nombre_base
            while os.path.exists(nombre_final):
                nombre_final = os.path.join(directorio_reportes, f"{nombre_archivo}_v{contador}.csv")
                contador += 1

            df.to_csv(nombre_final, index=False)
            st.markdown("El archivo se almacenará en la carpeta `/reports` del proyecto.")
            st.success(f"✅ Reporte guardado como {os.path.basename(nombre_final)}")
            st.code(nombre_final, language="bash")