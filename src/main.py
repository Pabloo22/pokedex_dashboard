import streamlit as st

from plots import pokemon_umap, pokemon_table


def main_page():
    import streamlit as st
    from st_aggrid import AgGrid
    import plotly.express as px

    st.title("Pokedex Dashboard")

    col1, col2 = st.columns(2, gap="large")
    selected_pokemon_id = 1
    df = pokemon_table(pokemon_id=selected_pokemon_id)
    with col1:
        # Select pokemon id
        st.markdown("## Select pokemon id")
        selected_pokemon_id = st.selectbox("", df["id"].values)

    with col2:
        # Plotly plot
        st.markdown("## UMAP plot")
        fig = pokemon_umap()
        st.plotly_chart(fig, use_container_width=True)

        # Table
        st.markdown("## Pokemon table")
        df = pokemon_table(pokemon_id=selected_pokemon_id)
        st.write("Selected pokemon id:", selected_pokemon_id)
        st.dataframe(df, use_container_width=True, hide_index=True)






if __name__ == "__main__":
    main_page()
