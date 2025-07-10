import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def render_historical_timeline(csv_files):
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

            grouped = hist_df.groupby(['fecha', 'Signal']).size().reset_index(name='conteo')

            fig_timeline = go.Figure()
            for signal_type in grouped['Signal'].unique():
                df_type = grouped[grouped['Signal'] == signal_type]
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