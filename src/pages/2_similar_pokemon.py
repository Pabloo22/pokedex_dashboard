import streamlit as st

from utils import (load_pokemon_dataframe,
                   get_pokedex_number,
                   pokemon_umap,
                   pokemon_table,
                   )

from displays import display_basic_info, display_table
st.markdown("<h1 style='text-align: center;'>Similar Pokemon</h1>", unsafe_allow_html=True)

# Initialization
if "selected_pokemon" not in st.session_state:
    st.session_state["selected_pokemon"] = "Bulbasaur"

with st.sidebar:
    mode = st.radio("Mode", ["type", "pop-out"], index=0)

pokemon_df = load_pokemon_dataframe()
st.session_state["selected_pokemon"] = st.selectbox("-",
                                                    pokemon_df["name"].values,
                                                    label_visibility="hidden",
                                                    index=int(get_pokedex_number(
                                                        pokemon_df,
                                                        st.session_state["selected_pokemon"])
                                                    ) - 1)
display_basic_info(pokemon_df[pokemon_df["name"] == st.session_state["selected_pokemon"]])

col1, col2 = st.columns(2, gap="large")
with col1:
    # Choose between "type" and "pop-out"

    fig = pokemon_umap(color_by=mode, pokedex_number=get_pokedex_number(pokemon_df,
                                                                        st.session_state["selected_pokemon"]))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Table
    df = pokemon_table(pokemon_df, pokemon_name=st.session_state["selected_pokemon"])
    st.write("Click on a row to select a Pokemon.")
    response = display_table(df)
    try:
        last_selected_pokemon = st.session_state["selected_pokemon"]
        st.session_state["selected_pokemon"] = response.selected_rows[0]["name"]
        if last_selected_pokemon != st.session_state["selected_pokemon"]:
            st.experimental_rerun()
    except IndexError:
        pass