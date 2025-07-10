import streamlit as st

def render_signal_summary_section(filtered_data):
    st.subheader("📊 Resumen de Señales Detectadas")

    if filtered_data.empty:
        st.info("No hay señales disponibles con los filtros actuales.")
        return

    signal_counts = filtered_data["Signal"].value_counts()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Señales", len(filtered_data))
    with col2:
        for signal, count in signal_counts.items():
            st.write(f"**{signal}**: {count}")
