import streamlit as st
import json
import os
import pandas as pd

FAVORITES_FILE = "data/favoritas.json"

def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_favorites(favorites):
    os.makedirs(os.path.dirname(FAVORITES_FILE), exist_ok=True)
    with open(FAVORITES_FILE, "w") as f:
        json.dump(list(favorites), f)

def render_favorites_section(df: pd.DataFrame) -> set:
    st.subheader("⭐ Sección de Favoritos")

    coin_list = df["Coin"].unique().tolist()
    selected_favorites = st.multiselect("Selecciona tus criptomonedas favoritas", coin_list)

    if st.button("Guardar Favoritos"):
        save_favorites(set(selected_favorites))
        st.success("Favoritos guardados correctamente ✅")

    current_favorites = load_favorites()
    if current_favorites:
        st.markdown("### Tus Favoritas actuales:")
        for coin in current_favorites:
            st.markdown(f"- **{coin}**")
    else:
        st.info("No tienes favoritas guardadas aún.")

    return current_favorites