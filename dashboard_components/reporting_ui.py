import streamlit as st
import os
import pandas as pd

def render_reporting_tools(df, selected_file):
    st.subheader("📁 Guardar búsqueda filtrada como reporte")
    
    if df.empty:
        st.warning("⚠️ No hay datos para guardar.")
        return

    default_name = f"reporte_{selected_file.replace('.csv','')}"
    nombre_reporte = st.text_input("Nombre del archivo:", value=default_name).strip()

    if st.button("💾 Guardar búsqueda"):
        if not nombre_reporte:
            st.warning("⚠️ El nombre del archivo no puede estar vacío.")
            return

        # Normalizar el nombre eliminando caracteres no permitidos
        nombre_reporte = "".join(c for c in nombre_reporte if c.isalnum() or c in ('_', '-')).rstrip()

        directorio_reportes = os.path.join(os.getcwd(), "reports")
        os.makedirs(directorio_reportes, exist_ok=True)

        nombre_base = os.path.join(directorio_reportes, f"{nombre_reporte}.csv")
        contador = 1
        nombre_final = nombre_base
        while os.path.exists(nombre_final):
            nombre_final = os.path.join(directorio_reportes, f"{nombre_reporte}_v{contador}.csv")
            contador += 1

        df.to_csv(nombre_final, index=False)
        st.success(f"✅ Reporte guardado como {os.path.basename(nombre_final)}")