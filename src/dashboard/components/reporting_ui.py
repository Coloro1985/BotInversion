import streamlit as st
import os
import pandas as pd

def render_reporting_tools(df_filtered, selected_file_name):
    """
    Renderiza las herramientas para guardar un reporte filtrado.

    Args:
        df_filtered (pd.DataFrame): El DataFrame con los datos ya filtrados.
        selected_file_name (str): El nombre del archivo original para usarlo en el nuevo nombre.
    """
    st.markdown("### 💾 Exportar Reporte Filtrado")
    st.markdown("Puedes guardar esta vista como un archivo CSV para su posterior análisis o consulta.")

    # ✅ Guarda de seguridad: nos aseguramos de que df_filtered sea un DataFrame
    if not isinstance(df_filtered, pd.DataFrame) or df_filtered.empty:
        st.warning("⚠️ No hay datos filtrados para guardar.")
        return

    # Limpiamos el nombre del archivo base
    base_name = os.path.basename(selected_file_name).replace('.csv', '')
    default_name = f"reporte_filtrado_{base_name}"
    
    directorio_reportes = "reports" # Guardamos en la carpeta raíz de reportes
    os.makedirs(directorio_reportes, exist_ok=True)

    with st.form("guardar_reporte_form"):
        nombre_archivo = st.text_input("Nombre del archivo:", value=default_name).strip()
        submit_guardar = st.form_submit_button("💾 Guardar como CSV")

        if submit_guardar:
            if not nombre_archivo:
                st.warning("⚠️ El nombre del archivo no puede estar vacío.")
                return

            # Limpiar el nombre para que sea seguro
            safe_filename = "".join(c for c in nombre_archivo if c.isalnum() or c in ('_', '-')).rstrip()
            final_path = os.path.join(directorio_reportes, f"{safe_filename}.csv")

            try:
                df_filtered.to_csv(final_path, index=False)
                st.success(f"✅ Reporte guardado como `{safe_filename}.csv` en la carpeta `reports/`.")
            except Exception as e:
                st.error(f"❌ No se pudo guardar el archivo: {e}")