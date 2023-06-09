import streamlit as st


st.set_page_config(page_title="Pokemon Dashboard", layout="wide")


import streamlit as st
import pathlib

from utils import (load_pokemon_dataframe,
                   get_pokedex_number,
                   )

from displays import display_basic_info, display_base_stats_type_defenses

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
    compare_match = st.selectbox("Compare with", [None] + pokemon_df["name"].values.tolist())
    compare_match = pokemon_df[pokemon_df["name"] == compare_match] if compare_match is not None else None

st.session_state["selected_pokemon"] = st.selectbox("-",
                                                    pokemon_df["name"].values,
                                                    label_visibility="hidden",
                                                    index=int(get_pokedex_number(
                                                        pokemon_df,
                                                        st.session_state["selected_pokemon"])
                                                    ) - 1)

match = pokemon_df[pokemon_df["name"] == st.session_state["selected_pokemon"]]
display_basic_info(match)

st.markdown("## Base Stats and Type Defenses")

display_base_stats_type_defenses(match, compare_match)

