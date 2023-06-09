import pandas as pd
import numpy as np
import streamlit as st
import plotly
import plotly.express as px
import pathlib
from PIL import Image
import umap
from sklearn.preprocessing import MinMaxScaler


@st.cache_data
def load_pokemon_dataframe():
    """Loads the pokemon dataframe."""
    parent_path = pathlib.Path(__file__).parent
    # Loop until get src folder
    while parent_path.name != "src":
        parent_path = parent_path.parent

    pokemon_path = parent_path.parent.absolute() / "data/pokemon.csv"
    df = pd.read_csv(pokemon_path)
    return df


@st.cache_data
def get_df_with_umap():
    np.random.seed(0)
    df = load_pokemon_dataframe()

    # Select numeric columns
    numeric_cols = df.select_dtypes(include="number").columns
    remove_cols = ["percentage_male", "generation", "pokedex_number", "height_m", "weight_kg"]
    numeric_cols = [col for col in numeric_cols if col not in remove_cols and df[col].isna().sum() == 0]
    df_numeric = df[numeric_cols]

    # Scale data
    scaler = MinMaxScaler()
    df_numeric = pd.DataFrame(scaler.fit_transform(df_numeric), columns=df_numeric.columns)

    # UMAP
    umap_model = umap.UMAP(n_neighbors=5, min_dist=0.3, metric="correlation", random_state=0)
    umap_embeddings = umap_model.fit_transform(df_numeric)
    umap_df = pd.DataFrame(umap_embeddings, columns=["first component", "second component"])

    # Normalize components
    min_first_component = umap_df["first component"].min()
    max_first_component = umap_df["first component"].max()
    min_second_component = umap_df["second component"].min()
    max_second_component = umap_df["second component"].max()
    umap_df["first component"] = (umap_df["first component"] - min_first_component) / (max_first_component - min_first_component)
    umap_df["second component"] = (umap_df["second component"] - min_second_component) / (max_second_component - min_second_component)
    return umap_df


@st.cache_data
def pokemon_umap(color_by: str = "type", pokedex_number: int = 1):
    """Display an umap plot of pokemon.

    Args:
        color_by (str, optional): Color by type or similarity. Defaults to "type". Can be "type" or "pop-out".
        pokedex_number (int, optional): Current pokemon id, used to color by pop-out. Defaults to 1.
    """
    np.random.seed(42)
    df = load_pokemon_dataframe()
    umap_df = get_df_with_umap()

    df["first component"] = umap_df["first component"]
    df["second component"] = umap_df["second component"]

    # Get the hex color of each type
    type_colors = {
        'normal': '#aa9',
        'fire': '#f42',
        'water': '#39f',
        'electric': '#fc3',
        'grass': '#7c5',
        'ice': '#6cf',
        'fighting': '#b54',
        'poison': '#a59',
        'ground': '#db5',
        'flying': '#89f',
        'psychic': '#f59',
        'bug': '#ab2',
        'rock': '#ba6',
        'ghost': '#66b',
        'dragon': '#76e',
        'dark': '#754',
        'steel': '#aab',
        'fairy': '#e9e',
        'curse': '#698'
    }

    if color_by == "type":
        # Plot
        fig = px.scatter(
            df,
            x="first component",
            y="second component",
            # title="Pokemon Embeddings",
            color="type1",
            color_discrete_map=type_colors,
            hover_name="name",
            hover_data=["type1", "type2"],
            width=800,
            height=600,
        )
        # fig.update_traces(marker=dict(size=12, line=dict(width=2, color="DarkSlateGrey")))
        """fig.update_layout(
            plot_bgcolor="#f9f9f9",
            paper_bgcolor="#f9f9f9",
            font_color="#333333",
            margin=dict(l=0, r=0, t=0, b=0),
        )"""
    elif color_by == "pop-out":
        df["pop-out"] = df["pokedex_number"] == pokedex_number
        # Get the name of the current pokemon
        current_pokemon = df[df["pokedex_number"] == pokedex_number]["name"].values[0]
        df['pop-out'] = df['pop-out'].apply(lambda x: current_pokemon if x else f'Not {current_pokemon}')
        popout_colors = {
            current_pokemon: '#ff0000',
            f'Not {current_pokemon}': '#808080'
        }
        # Plot
        fig = px.scatter(
            df,
            x="first component",
            y="second component",
            color="pop-out",
            color_discrete_map=popout_colors,
            hover_name="name",
            hover_data=["type1", "type2"],
            width=800,
            height=600,
        )
        # fig.update_traces(marker=dict(size=12, line=dict(width=2, color="DarkSlateGrey")))
        # Center the plot on the current pokemon
        fig.update_layout(
            #plot_bgcolor="#f9f9f9",
            #paper_bgcolor="#f9f9f9",
            #font_color="#333333",
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(range=[df[df["name"] == current_pokemon]["first component"].values[0] - 0.1,
                              df[df["name"] == current_pokemon]["first component"].values[0] + 0.1]),
            yaxis=dict(range=[df[df["name"] == current_pokemon]["second component"].values[0] - 0.1,
                              df[df["name"] == current_pokemon]["second component"].values[0] + 0.1]),
        )
    else:
        raise ValueError(f"color_by must be 'type' or 'pop-out', got {color_by}")
    return fig


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Returns the cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def _vectorized_cosine_similarity(a: pd.DataFrame, b: pd.DataFrame) -> pd.Series:
    """Returns the cosine similarity between two vectors."""
    return np.dot(a, b.T) / (np.linalg.norm(a) * np.linalg.norm(b, axis=1))


def _vectorized_euclidean_distance(a: pd.DataFrame, b: pd.DataFrame, normalize=True) -> pd.Series:
    """Returns the euclidean distance between two vectors."""
    result = np.linalg.norm(a - b, axis=1)
    # Normalize the result
    if normalize:
        result = (result - result.min()) / (result.max() - result.min())

    return result


@st.cache_data
def get_similarities(pokemon_name: str) -> pd.Series | list[float]:
    """Returns a list of similarities to the current pokemon sorted by pokedex number."""
    np.random.seed(42)
    df = load_pokemon_dataframe()
    umap_df = get_df_with_umap()

    df["first component"] = umap_df["first component"]
    df["second component"] = umap_df["second component"]

    # Get the current pokemon embedding
    current_pokemon = df[df["name"] == pokemon_name][["first component", "second component"]]

    # Use cosine similarity to get the similarity between the current pokemon and all the others
    df["similarity"] = 1 - _vectorized_euclidean_distance(df[["first component", "second component"]].to_numpy(),
                                                          current_pokemon.to_numpy())

    return df["similarity"]


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

    df["similarity"] = np.round(similarities, 4)
    # Select columns "name", "type1", "type2", "similarity"
    df = df[["pokedex_number", "name", "type1", "type2", "similarity"]].rename({"pokedex_number": "#"}, axis=1)
    # Sort by similarity
    df = df.sort_values(by="similarity", ascending=False)
    return df


@st.cache_data
def get_pokedex_number(pokemon_df: pd.DataFrame, name: str) -> int:
    return pokemon_df[pokemon_df["name"] == name]["pokedex_number"].values[0]


@st.cache_data
def get_pokemon_image(pokedex_number: int):
    """Returns the image of the pokemon with the given pokedex number."""
    parent_path = pathlib.Path(__file__).parent
    # Loop until get to src folder
    while parent_path.name != "src":
        parent_path = parent_path.parent
    parent_path = parent_path.parent.absolute()
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

@st.cache_data
def get_pokemon_evolution_line(pokemon_name: str):
    parent_path = pathlib.Path(__file__).parent
    # Loop until get src folder
    while parent_path.name != "src":
        parent_path = parent_path.parent

    evolution_path = parent_path.parent.absolute() / "data/evolutions.csv"
    df = pd.read_csv(evolution_path)

    # Find the row with the pokemon on any of the columns
    # Create an empty list to store matching rows
    matching_rows = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Iterate over each column in the row
        for column in df.columns:
            # Check if the search string is present in the cell value
            if pokemon_name in str(row[column]):
                # Append the matching row to the list
                matching_rows.append(row)
                # Break the inner loop to avoid duplicate rows
                break

    evolution = pd.DataFrame(matching_rows, columns=df.columns)

    # For each column, create a list of all the unique values in the column
    unique_values = [evolution[column].unique() for column in evolution.columns]

    return unique_values

@st.cache_data
def get_unevolved(pokemon_name: str):
    return get_pokemon_evolution_line(pokemon_name)[0][0]

@st.cache_data
def get_first_evolved(pokemon_name: str):
    return get_pokemon_evolution_line(pokemon_name)[1]

@st.cache_data
def get_second_evolved(pokemon_name: str):
    return get_pokemon_evolution_line(pokemon_name)[2]





if __name__ == "__main__":
    df = load_pokemon_dataframe()
    plot = pokemon_umap(color_by="pop-out")
    # Show scatter plot not in streamlit
    plotly.offline.plot(plot, filename="umap_popout.html")

    plot = pokemon_umap(color_by="type")
    # Show scatter plot not in streamlit
    plotly.offline.plot(plot, filename="umap_type.html")
