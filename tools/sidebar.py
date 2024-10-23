import streamlit as st
import base64

def write_sidebar():
    image_path = './images/PP.png'
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
        encoded_image = base64.b64encode(image_bytes).decode()

    data_url = f"data:image/png;base64,{encoded_image}"

    # HTML et CSS pour afficher l'image en forme de cercle
    circle_image_html = f"""
    <style>
    .circular-image {{
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        padding: 0px;
        margin: 0px auto; /* Centrer l'image */
        display: block; /* Centrer l'image */
    }}
    </style>
    <img src="{data_url}" class="circular-image" />
    """

    st.sidebar.markdown(circle_image_html, unsafe_allow_html=True)
    st.sidebar.title(' ')

    st.sidebar.write("<p style=font-size:19px>👱🏼‍♂️ <b>|</b> He / Him", unsafe_allow_html=True)
    st.sidebar.write('<p style=font-size:19px>📱 <b>|</b> +33 6 75 82 61 83</p>', unsafe_allow_html=True)
    st.sidebar.write('<p style=font-size:19px>📨 <b>|</b> arthur.gatignol@efrei.net</p>', unsafe_allow_html=True)
    
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    
    st.sidebar.write()
    
    st.sidebar.write("<h1><u>Languages</u></h1>", unsafe_allow_html=True)
    st.sidebar.write("<p style=font-size:19px>🇫🇷 <b>|</b> French: Native</p>", unsafe_allow_html=True)
    st.sidebar.write("<p style=font-size:19px>🇬🇧 <b>|</b> English: Fluent</p>", unsafe_allow_html=True)
    st.sidebar.write('<br>', unsafe_allow_html=True)
    
    # Add a fixed footer
    footer_html = """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px 0;
        background-color: #f1f1f1;
    }
    </style>
    <div class="footer">
        <p>© 2024 Arthur Gatignol. All rights reserved.</p>
    </div>
    """
    
    st.sidebar.markdown(footer_html, unsafe_allow_html=True)