import streamlit as st
from PIL import Image
import base64
import io

# Open the logo image
logo = Image.open('./images/PP_logotyp_ANG_RGB.png')

# Create an in-memory stream
image_stream = io.BytesIO()

# Save the image to the stream in PNG format
logo.save(image_stream, format='PNG')

# Convert the image stream to base64
base64_image = base64.b64encode(image_stream.getvalue()).decode('utf-8')

st.markdown("""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>About</title>
</head>
<body>
  <h1>About</h1>
  <p>
    The Pokémon Dashboard is an interactive web application that provides detailed information and visualizations about 
    the fascinating world of Pokémon. It utilizes an extensive Pokémon dataset to offer a comprehensive examination of 
    individual Pokémon, their evolution trees, and similarities among them using the UMAP algorithm.
  </p>
  <p>
    You can explore in-depth information about specific Pokémon, including their types, 
    abilities, base stats, and more. You can visualize the evolution tree of a Pokémon, allowing you to understand the 
    different stages of its development and how it relates to other Pokémon within its evolutionary line.
  </p>
  <p>
    Additionally, the dashboard employs the UMAP algorithm to identify similar Pokémon based on various attributes such 
    as type, base stats, and abilities. This feature allows you to discover Pokémon that share similar characteristics 
    and may be of interest to you.
  </p>
  <p>
    Whether you are a long-time Pokémon fan or just curious about these creatures, the Pokémon Dashboard offers a wealth
     of information and interactive tools to enhance your understanding and explore the Pokémon universe.
  </p>
</body>
</html>""", unsafe_allow_html=True)

st.markdown(f"""<!DOCTYPE html>
<html>
<head>
    <title>Dashboard Information</title>
    <style>
        body {{
            text-align: center;
        }}
        img {{
            width: 50%;
            height: auto;
        }}
    </style>
    <h1 style='text-align: center;'>Acknowledgements</h1>
</head>
<body>
    <p>This dashboard was created by Pablo Ariño and Álvaro Laguna.</p>
    <p>The data used in this dashboard was obtained from <a href="https://www.kaggle.com/rounakbanik/pokemon">Kaggle</a>
    and scraped from the <a href="https://pokemon.fandom.com/wiki/List_of_Pok%C3%A9mon_by_evolution">Pokémon Wiki</a>.
    </p>
    <p>Part of the code for displaying the main Pokémon data and Type Defenses was adapted from the following 
    tutorial:<br> 
    <a href="https://betterprogramming.pub/build-your-own-pokedex-web-app-with-streamlit-10c550a98e22">Build Your Own 
    Pokedex Web App With Streamlit</a>.</p>
    <p>Pokémon and All Respective Names are Trademark &amp; © of Nintendo 1996-2023.</p>
    <img src="data:image/png;base64,{base64_image}"/>
</body>
</html>
""", unsafe_allow_html=True)


