import streamlit as st
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Restaurant Reservation System",
    page_icon="🍽️",
    layout="wide"
)

# Page styling
st.markdown(
"""
<style>
    .title {
        text-align: center;
        font-size: 48px;
        color: #ff4500;
        padding-bottom: 30px;
    }
    .description {
        text-align: center;
        font-size: 20px;
        color: #808080;
        padding-bottom: 30px;
    }
</style>
""",
unsafe_allow_html=True)

# Title and description
st.markdown("<h1 class='title'>Restaurant Reservation System</h1>", unsafe_allow_html=True)
st.markdown("<p class='description'>Welcome to our restaurant reservation system. Reserve your table now!</p>", unsafe_allow_html=True)

# Image
image = Image.open("restaurant_image.jpeg")
st.image(image, caption="Photo by Daria Shevtsova from Pexels", use_column_width=True)
