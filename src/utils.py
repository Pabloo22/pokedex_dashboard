import pandas as pd
import streamlit as st
import plotly
import plotly.express as px
import pathlib
from PIL import Image


@st.cache_data
def load_pokemon_dataframe():
    """Loads the pokemon dataframe."""
    parent_path = pathlib.Path(__file__).parent.parent.absolute()
    pokemon_path = parent_path / "data/pokemon.csv"
    df = pd.read_csv(pokemon_path)
    return df


def pokemon_umap(color_by: str = "type", pokedex_number: int = 1):
    """Display an umap plot of pokemon.

    Args:
        color_by (str, optional): Color by type or similarity. Defaults to "type". Can be "type" or "pop-out".
        pokedex_number (int, optional): Current pokemon id, used to color by pop-out. Defaults to 1.
    """

    # Create a sample dataframe
    ids = [1, 2, 3, 4, 5]
    x = [0.1, 0.4, 0.35, 0.8, 0.65]
    y = [0.2, 0.3, 0.45, 0.7, 0.55]
    data = {'id': ids,
            'x': x,
            'y': y,
            'other_info': ['info1', 'info2', 'info3', 'info4', 'info5']}
    df = pd.DataFrame(data)

    # Plotly plot
    fig = px.scatter(df, x="x", y="y", hover_data=["id"])

    return fig


@st.cache_data
def get_similarities(pokemon_name: str) -> pd.Series | list[float]:
    """Returns a list of similarities to the current pokemon sorted by pokedex number."""
    import numpy as np

    N_POKEMONS = 801
    np.random.seed(42)
    similarities = np.random.rand(N_POKEMONS)
    return similarities


@st.cache_data
def pokemon_table(pokemon_df: pd.DataFrame, pokemon_name: str) -> pd.DataFrame:
    """Returns a dataframe with basic information about all pokemon.

    It adds a column of similarities to the current pokemon.

    Args:
        pokemon_df (pd.DataFrame): dataframe with pokemon information.
        pokemon_name (int, optional): pokedex number of the current pokemon. Defaults to 1.
    """
    similarities = get_similarities(pokemon_name)
    df = pokemon_df.copy()
    assert len(similarities) == len(df)

    df["similarity"] = similarities
    # Select columns "name", "type1", "type2", "similarity"
    df = df[["name", "type1", "type2", "similarity"]]
    # Sort by similarity
    df = df.sort_values(by="similarity", ascending=False)
    return df


@st.cache_data
def get_pokedex_number(pokemon_df: pd.DataFrame, name: str) -> int:
    return pokemon_df[pokemon_df["name"] == name]["pokedex_number"].values[0]


@st.cache_data
def get_pokemon_image(pokedex_number: int):
    """Returns the image of the pokemon with the given pokedex number."""
    parent_path = pathlib.Path(__file__).parent.parent.absolute()
    pokedex_number = str(pokedex_number).zfill(3)
    image_path = parent_path / f"images/{pokedex_number}.png"

    # Read image
    image = Image.open(image_path)
    return image


@st.cache_data
def get_pokemon_name(pokedex_number: int):
    """Returns the name of the pokemon with the given pokedex number."""
    # Create a sample dataframe
    names = {
        1: "Bulbasaur",
        2: "Ivysaur",
        3: "Venusaur",
        4: "Charmander",
        5: "Charmeleon",
    }
    return names[pokedex_number]
