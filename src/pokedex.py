import streamlit as st

import pathlib

from utils import (load_pokemon_dataframe,
                   get_pokedex_number,
                   )

from displays import display_basic_info, display_base_stats_type_defenses


st.set_page_config(page_title="Pokemon Dashboard", layout="wide")

current_path = pathlib.Path(__file__).parent.absolute()
with open(current_path / "style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialization
if "selected_pokemon" not in st.session_state:
    st.session_state["selected_pokemon"] = "Bulbasaur"

pokemon_df = load_pokemon_dataframe()

st.markdown("<h1 style='text-align: center;'>Pokédex Dashboard</h1>", unsafe_allow_html=True)
st.sidebar.title("Pokédex Dashboard")

# Add a selectbox to the sidebar:
with st.sidebar:

    st.session_state["selected_pokemon"] = st.selectbox("Select a Pokemon",
                                                        pokemon_df["name"].values,
                                                        index=int(get_pokedex_number(
                                                            pokemon_df,
                                                            st.session_state["selected_pokemon"])
                                                        ) - 1)
    compare_match = st.selectbox("Compare with", [None] + pokemon_df["name"].values.tolist())
    compare_match = pokemon_df[pokemon_df["name"] == compare_match] if compare_match is not None else None


match = pokemon_df[pokemon_df["name"] == st.session_state["selected_pokemon"]]

display_basic_info(match)

display_base_stats_type_defenses(match, compare_match)

