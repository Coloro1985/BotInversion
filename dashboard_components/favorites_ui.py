import streamlit as st

def render_favorites_section(favorites_list):
    st.subheader("⭐ Favoritos")
    if not favorites_list:
        st.info("No tienes señales favoritas aún.")
        return

    for signal in favorites_list:
        st.markdown(f"- **{signal['coin']}** - {signal['signal']} ({signal['date']})")