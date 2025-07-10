import streamlit as st
import matplotlib.pyplot as plt

def render_signal_summary_section(filtered_data):
    st.subheader("📊 Resumen de Señales Detectadas")

    if filtered_data.empty:
        st.info("No hay señales disponibles con los filtros actuales.")
        return

    signal_counts = filtered_data["Signal"].value_counts()

    st.markdown("### 📈 Distribución de Señales por Tipo")

    fig = plot_signal_distribution(signal_counts)
    st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Señales", len(filtered_data))
    with col2:
        for signal, count in signal_counts.items():
            st.write(f"**{signal}**: {count}")

def plot_signal_distribution(signal_counts):
    fig, ax = plt.subplots()
    signal_counts.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title("Cantidad de Señales por Tipo")
    ax.set_xlabel("Tipo de Señal")
    ax.set_ylabel("Cantidad")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    return fig
