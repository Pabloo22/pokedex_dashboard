import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from st_aggrid import AgGrid, GridUpdateMode, GridOptionsBuilder, JsCode, AgGridReturn
from utils import get_pokemon_image


def display_basic_info(match):
    """Display basic info of a Pokemon, including name, id, image, type, height, weight, abilities.

    Code adapted from: https://betterprogramming.pub/build-your-own-pokedex-web-app-with-streamlit-10c550a98e22
    """
    # get basic info data
    name = match['name'].iloc[0]
    id = match['pokedex_number'].iloc[0]
    height = str(match['height_m'].iloc[0])
    weight = str(match['weight_kg'].iloc[0])
    type1 = match['type1'].iloc[0]
    type2 = match['type2'].iloc[0]
    type_number = 1 if pd.isnull(type2) else 2
    abilities = match['abilities'].iloc[0].replace(']', '').replace('[', '').replace("'", '').split(', ')
    ability1 = abilities[0] if len(abilities) > 0 else ''
    ability2 = abilities[1] if len(abilities) > 1 else ''
    ability_hidden = abilities[2] if len(abilities) > 2 else ''

    st.title(name + ' #' + str(id).zfill(3))
    col1, col2, col3 = st.columns(3)

    # leftmost column col1 displays pokemon image
    try:
        image = get_pokemon_image(id)
        col1.image(image)
    except Exception:  # output 'Image not available' instead of crashing the program when image not found
        col1.write('Image not available.')

        # middle column col2 displays nicely formatted Pokemon type using css loaded earlier
    with col2.container():
        col2.write('Type')
        # html code that loads the class defined in css, each Pokemon type has a different style color
        type_text = f'<span class="icon type-{type1.lower()}">{type1}</span>'
        if type_number == 2:
            type_text += f'<span class="icon type-{type2.lower()}">{type2}</span>'
        # markdown displays html code directly
        col2.markdown(type_text, unsafe_allow_html=True)
        col2.metric("Height", height + " m")
        col2.metric("Weight", weight + " kg")

    # rightmost column col3 displays Pokemon abilities
    with col3.container():
        # col3.metric("Species", species)
        col3.write('Abilities')
        if ability1 != '':
            col3.subheader(ability1)
        if ability2 != '':
            col3.subheader(ability2)
        if ability_hidden != '':
            col3.subheader(ability_hidden + ' (Hidden)')


def display_table(data) -> AgGridReturn:
    """https://discuss.streamlit.io/t/ag-grid-get-column-index-of-clicked-cell/32576"""
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_columns(list('abc'), editable=True)

    js = JsCode("""
    function(e) {
        let api = e.api;
        let rowIndex = e.rowIndex;
        let col = e.column.colId;

        let rowNode = api.getDisplayedRowAtIndex(rowIndex);

        console.log("column index: " + col + ", row index: " + rowIndex);
    };
    """)

    gb.configure_grid_options(onCellClicked=js)
    gb.configure_selection(selection_mode='single')
    go = gb.build()

    return_ag = AgGrid(data,
                       gridOptions=go,
                       allow_unsafe_jscode=True,
                       reload_data=True,
                       update_mode=GridUpdateMode.SELECTION_CHANGED,
                       fit_columns_on_grid_load=True,
                       height=300,
                       hide_index=False,
                       update_on=['selection_changed'],)
    return return_ag


def display_base_stats_type_defenses(match, pokemon_df):
    """Displays base stats and type defenses of a Pokemon.

    Code adapted from: https://betterprogramming.pub/build-your-own-pokedex-web-app-with-streamlit-10c550a98e22
    """
    # list to gather all type weaknesses and resistances
    weakness_2_types = []
    weakness_4_types = []
    resistance_half_types = []
    resistance_quarter_types = []

    # dataset only shows damage (x4, x2, x0.25, x0.5) of each type towards the Pokemon
    # manually classify the damages into weaknesses and resistances list
    for i, j in match.iterrows():
        for column, value in j.items():
            if column.startswith('against_'):
                type_ = column.split('_')[1]
                if value == 0.5:
                    resistance_half_types.append(type_)
                elif value == 0.25:
                    resistance_quarter_types.append(type_)
                elif value == 2:
                    weakness_2_types.append(type_)
                elif value == 4:
                    weakness_4_types.append(type_)

    with st.container():
        col1, col2 = st.columns(2)

        # left column col1 displays horizontal bar chart of base stats
        col1.subheader('Base Stats')
        with col1.container():
            compare_match = st.selectbox("Compare with", [None] + pokemon_df["name"].values.tolist())
            compare_match = pokemon_df[pokemon_df["name"] == compare_match] if compare_match is not None else None

        # get base stats of Pokemon and rename columns nicely
        df_stats = match[['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']]
        df_stats = df_stats.rename(
            columns={'hp': 'HP', 'attack': 'Attack', 'defense': 'Defense', 'sp_attack': 'Special Attack',
                     'sp_defense': 'Special Defense', 'speed': 'Speed'}).T
        df_stats.columns = ['stats']

        # plot horizontal bar chart using matplotlib.pyplot
        fig = go.Figure()
        if compare_match is not None:
            df_compare_stats = compare_match[['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']]
            df_compare_stats = df_compare_stats.rename(
                columns={'hp': 'HP', 'attack': 'Attack', 'defense': 'Defense', 'sp_attack': 'Special Attack',
                            'sp_defense': 'Special Defense', 'speed': 'Speed'}).T
            df_compare_stats.columns = ['stats']
            df_stats['compare_stats'] = df_compare_stats['stats']

            # Create a grouped bar chart that compares the stats of match and compare_match

            # set width of bar
            bar_width = 0.4
            # set height of bar
            bars1 = df_stats['stats']
            bars2 = df_stats['compare_stats']
            # Set position of bar on X axis
            r1 = np.arange(len(bars1))
            r2 = [x + bar_width for x in r1]
            # Make the plot
            pokemon_name = match['name'].values[0]
            pokemon_name_compare = compare_match['name'].values[0]
            fig.add_trace(go.Bar(
                y=r2,
                x=bars1,
                orientation='h',
                name=pokemon_name
            ))

            fig.add_trace(go.Bar(
                y=r1,
                x=bars2,
                orientation='h',
                name=pokemon_name_compare,
                marker=dict(color='gray')
            ))

            fig.update_layout(
                yaxis=dict(
                    tickmode='array',
                    tickvals=[r + bar_width / 2 for r in range(len(bars1))],
                    ticktext=df_stats.index
                ),
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1
                )
            )

        else:
            fig.add_trace(go.Bar(
                y=df_stats.index,
                x=df_stats.stats,
                orientation='h'
            ))

            fig.update_layout(
                yaxis=dict(title='Pokemon'),
                xaxis=dict(title='Stats'),
                title='Pokemon Stats'
            )
        fig.update_layout(xaxis_range=[0, 250])
        # plt.xlim([0, 250])
        # col1.pyplot(fig)
        col1.plotly_chart(fig)
        # right column col2 displays the weaknesses and resistances
        # the displayed types are nicely formatted using css (same as earlier)
        col2.subheader('Type Defenses')

        col2.write('Strong Weaknesses (x4)')
        weakness_text = ''
        for type_ in weakness_4_types:
            weakness_text += f' <span class="icon type-{type_}">{type_}</span>'
        col2.markdown(weakness_text, unsafe_allow_html=True)

        col2.write('Weaknesses (x2)')
        weakness_text = ''
        for type_ in weakness_2_types:
            weakness_text += f' <span class="icon type-{type_}">{type_}</span>'
        col2.markdown(weakness_text, unsafe_allow_html=True)

        col2.write('Resistances (x0.5)')
        resistance_half_text = ''
        for type_ in resistance_half_types:
            resistance_half_text += f' <span class="icon type-{type_}">{type_}</span>'
        col2.markdown(resistance_half_text, unsafe_allow_html=True)

        col2.write('Strong Resistances (x0.25)')
        resistance_quarter_text = ''
        for type_ in resistance_quarter_types:
            resistance_quarter_text += f' <span class="icon type-{type_}">{type_}</span>'
        col2.markdown(resistance_quarter_text, unsafe_allow_html=True)
