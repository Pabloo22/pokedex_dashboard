import streamlit as st

from utils import (load_pokemon_dataframe,
                   get_pokedex_number,
                   get_pokemon_image,
                   get_unevolved,
                   get_first_evolved,
                   get_second_evolved,
                   )

# Initialization
if "selected_pokemon" not in st.session_state:
    st.session_state["selected_pokemon"] = "Bulbasaur"

st.markdown("<h1 style='text-align: center;'>Evolution Tree</h1>", unsafe_allow_html=True)

pokemon_df = load_pokemon_dataframe()

with st.sidebar:
    last_selected_pokemon = st.session_state["selected_pokemon"]
    st.session_state["selected_pokemon"] = st.selectbox("Select a Pokemon",
                                                        pokemon_df["name"].values,
                                                        index=int(get_pokedex_number(
                                                            pokemon_df,
                                                            st.session_state["selected_pokemon"])
                                                        ) - 1)
    if last_selected_pokemon != st.session_state["selected_pokemon"]:
        st.experimental_rerun()

col1, col2, col3 = st.columns(3)

try:
    # Write Unevolved in bold and centered
    col1.markdown("<h2 style='text-align: center;'>Unevolved</h2>", unsafe_allow_html=True)
    pokemon = get_unevolved(st.session_state["selected_pokemon"])
    image = get_pokemon_image(get_pokedex_number(pokemon_df, pokemon))
    col1.image(image)
    col1.markdown(f'<p style="text-align: center;">{pokemon}</p>', unsafe_allow_html=True)
except Exception:  # output 'Image not available' instead of crashing the program when image not found
    col1.write('Image not available.')

try:
    col2.markdown("<h2 style='text-align: center;'>First Evolution</h2>", unsafe_allow_html=True)
    first_evolved = get_first_evolved(st.session_state["selected_pokemon"])
    if len(first_evolved) == 0:
        col2.write("This Pokemon does not have a first evolution.")
    else:
        for pokemon in first_evolved:
            try:
                image = get_pokemon_image(get_pokedex_number(pokemon_df, pokemon))
                col2.image(image)
                col2.markdown(f'<p style="text-align: center;">{pokemon}</p>', unsafe_allow_html=True)
            except Exception:
                continue
except Exception:  # output 'Image not available' instead of crashing the program when image not found
    col2.write(f'Image not available.')

try:
    col3.markdown("<h2 style='text-align: center;'>Second Evolution</h2>", unsafe_allow_html=True)
    second_evolved = get_second_evolved(st.session_state["selected_pokemon"])
    if len(second_evolved) == 0:
        col3.write("This Pokemon does not have a second evolution.")
    else:
        for pokemon in second_evolved:
            try:
                image = get_pokemon_image(get_pokedex_number(pokemon_df, pokemon))
                col3.image(image)
                col3.markdown(f'<p style="text-align: center;">{pokemon}</p>', unsafe_allow_html=True)
            except Exception:
                continue
except Exception:  # output 'Image not available' instead of crashing the program when image not found
    col3.write('Image not available.')