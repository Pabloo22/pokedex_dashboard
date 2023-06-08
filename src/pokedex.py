import streamlit as st
import pathlib

from utils import (pokemon_umap,
                   pokemon_table,
                   load_pokemon_dataframe,
                   get_pokedex_number,
                   )

from displays import display_basic_info, display_table, display_base_stats_type_defenses


st.set_page_config(page_title="Pokédex", layout="wide")

current_path = pathlib.Path(__file__).parent.absolute()
with open(current_path / "style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialization
if "selected_pokemon" not in st.session_state:
    st.session_state["selected_pokemon"] = "Bulbasaur"


def main_page():
    pokemon_df = load_pokemon_dataframe()

    st.title("Pokédex Dashboard")
    st.sidebar.title("Pokédex Dashboard")
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
    display_base_stats_type_defenses(match)

    st.markdown("## Similar Pokemon")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        fig = pokemon_umap()
        st.plotly_chart(fig, use_container_width=True)

    with col2:

        # Table
        df = pokemon_table(pokemon_df, pokemon_name=st.session_state["selected_pokemon"])
        st.write("Click on a row to select a Pokemon.")
        response = display_table(df)
        try:
            st.session_state["selected_pokemon"] = response.selected_rows[0]["name"]
            st.write(st.session_state["selected_pokemon"])
            st.experimental_rerun()
        except IndexError:
            pass


if __name__ == "__main__":
    main_page()