import streamlit as st
import pathlib

from utils import (pokemon_umap,
                   pokemon_table,
                   get_pokemon_image,
                   get_pokemon_name,
                   load_pokemon_dataframe,
                   get_pokedex_number
                   )


st.set_page_config(page_title="Pokédex", layout="wide")

current_path = pathlib.Path(__file__).parent.absolute()
with open(current_path / "style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def main_page():
    import streamlit as st
    from st_aggrid import AgGrid
    import plotly.express as px

    pokemon_df = load_pokemon_dataframe()

    st.title("Pokédex Dashboard")
    st.sidebar.title("Pokédex Dashboard")
    selected_pokemon_name = st.selectbox("", pokemon_df["name"].values)

    # Add image
    pokedex_number = get_pokedex_number(pokemon_df, selected_pokemon_name)
    st.markdown(f"## {selected_pokemon_name} #{pokedex_number}")
    image = get_pokemon_image(pokedex_number)
    st.image(image, use_column_width=False)

    st.markdown("## Similar Pokemon")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        fig = pokemon_umap()
        st.plotly_chart(fig, use_container_width=True)

    with col2:

        # Table
        df = pokemon_table(pokemon_df, pokemon_name=selected_pokemon_name)
        st.dataframe(df, use_container_width=True, hide_index=False)



if __name__ == "__main__":
    main_page()
