import pandas as pd
import streamlit as st
import plotly
import plotly.express as px


def pokemon_umap() -> plotly.graph_objs._figure.Figure:
    """Display an umap plot of pokemon.

    If you click on a point, it will display the pokemon's data.
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
def get_similarities(pokemon_id: int):
    similarities = {
        1: [0.1, 0.4, 0.35, 0.8, 0.65],
        2: [0.2, 0.3, 0.35, 0.28, 0.5],
        3: [0.3, 0.2, 0.35, 0.18, 0.35],
        4: [0.4, 0.1, 0.35, 0.08, 0.25],
        5: [0.5, 0.0, 0.35, 0.18, 0.15],
    }
    return similarities[pokemon_id]


@st.cache_data
def pokemon_table(sort_by: str = "id", pokemon_id: int = 1) -> pd.DataFrame:
    """Display a table of pokemon. Sort by id or similarity to current pokemon.

    Args:
        sort_by (str, optional): Sort by id or similarity to current pokemon. Defaults to "id".
        pokemon_id (int, optional): Current pokemon id, used to sort by similarity. Defaults to 1.
    """
    # Create a sample dataframe
    data = {'id': [1, 2, 3, 4, 5],
            'similarity': get_similarities(pokemon_id),
            'other_info': ['info1', 'info2', 'info3', 'info4', 'info5']}
    df = pd.DataFrame(data)

    return df
