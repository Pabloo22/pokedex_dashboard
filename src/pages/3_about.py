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
    <h1 style='text-align: center;'>About</h1>
</head>
<body>
    <p>This dashboard was created by Pablo Ariño and Álvaro Laguna.</p>
    <p>The data used in this dashboard was obtained from <a href="https://www.kaggle.com/rounakbanik/pokemon">Kaggle</a>
    and scraped from the <a href="https://pokemon.fandom.com/wiki/List_of_Pok%C3%A9mon_by_evolution">Pokémon Wiki</a>.
    </p>    
    <p>Pokémon and All Respective Names are Trademark &amp; © of Nintendo 1996-2023.</p>
    <img src="data:image/png;base64,{base64_image}"/>
</body>
</html>
""", unsafe_allow_html=True)


