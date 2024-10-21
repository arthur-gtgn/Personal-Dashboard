import streamlit as st 
import pandas as pd
import folium
from streamlit_folium import st_folium

from card import write_card
from sidebar import write_sidebar
from getRepo import getRepo

# BUG: Epace non-voulu entre la carte et la partie 'Personal Projects 📁'

st.set_page_config(page_title="Portfolio", page_icon=":briefcase:", layout="wide")

def underlined_subheader(text):
    st.markdown(f"<h3 style='text-decoration: underline;'>{text}</h3>", unsafe_allow_html=True)

write_sidebar()

col1, col2 = st.columns([1, 1])
with col1:
    st.image('./images/efrei.png', width=400)

with col2:
    st.image('./images/BNP.png', width=400)

st.title('Hi! I am Arthur Gatignol 👋')
st.write("""
<p style=font-size:22px>I am a Data Science student at <u>EFREI Paris Panthéon-Assass</u>,
passionate about artificial intelligence and machine learning. I am always looking for new
challenges and opportunities to learn and grow. At the moment, I am working at <u>BNP 
Paribas</u> as a Machine Learning Engineer, exploring the future of AI ⚗️ in the banking 
world!</p  
""", unsafe_allow_html=True)

st.divider()

underlined_subheader('Myself on a map  🌍')

col1, col2 = st.columns([0.5, 1])

with col1:
    school = [48.7889, 2.3638]
    home = [48.8417, 2.3608]
    work = [48.8589, 2.4419]

    center_lat = (school[0] + home[0] + work[0]) / 3
    center_lon = (school[1] + home[1] + work[1]) / 3

    center = [center_lat, center_lon]

    # Create a map centered around Paris
    m = folium.Map(location=center, zoom_start=11, tiles='cartodbpositron')

    def create_emoji_icon(emoji):
        return folium.CustomIcon(
            icon_image=f'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">{emoji}</text></svg>',
            icon_size=(30, 30),
            icon_anchor=(15, 15),
        )
        
    folium.Marker(location=work, icon=create_emoji_icon('🏦')).add_to(m)
    folium.Marker(location=home, icon=create_emoji_icon('🏠')).add_to(m)
    folium.Marker(location=school, icon=create_emoji_icon('🏛️')).add_to(m)

    # Display the map in Streamlit
    st_folium(m, height=500)

with col2:
    st.write("<u><b>Map Legend</b></u>", unsafe_allow_html=True)
    st.write("🏦 - Work: BNP Paribas")
    st.write("🏠 - Home")
    st.write("🏛️ - School: EFREI Paris")
    
    st.write("<u><b>About My Locations</b></u>", unsafe_allow_html=True)
    st.write("""
    This map showcases the key locations in my daily life. 
    From my studies at EFREI Paris to my work at BNP Paribas, 
    and my home in between, it represents my journey in the 
    heart of Paris as a budding Data Scientist and Machine 
    Learning Engineer.
    """)
    
st.divider()

underlined_subheader('Personal Projects 📁')

col1, col2, col3 = st.columns(3)

with col1:
    write_card(
        "🎮 Game Catalog", 
        "A web application allowing interaction with a multi-entities SQL database for different games and their creators.", 
        ['VueJS', 'JavaScript', 'MySQL', 'REST'], 
        "arthur-gtgn/Game-Catalog", 
        "December 2023"
    )

with col2:
    write_card(
        "🤖 Machine Learning for Diabetes",
        "Exploration of different machine learning models for binary classification of the Pima Indians Diabetes dataset",
        ['Python', 'Scikit-learn', 'Pandas', 'Matplotlib'],
        "arthur-gtgn/Machine-Learning-for-Diabetes",
        "October 2024"
    )

with col3:
    write_card(
        "📡 Frequency Bands Allocation",
        "Data visualization and implementation of machine learning models for frequency bands allocation in wireless networks",
        ['Python', 'Pandas', 'Matplotlib', 'Tensorflow'],
        "arthur-gtgn/TRBF",
    "August 2024"
    )
    
st.divider()

underlined_subheader('My Education 🎓')
st.write("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([0.75, 1])

with col1:
    st.write('<br>', unsafe_allow_html=True)
    st.write('<br>', unsafe_allow_html=True)
    st.image('./images/efrei.png', width=300)

with col2:
    st.write("<h4><u><b>EFREI Paris</b></u></h4>", unsafe_allow_html=True)
    st.write("<p style=font-size:21px>🖥️ M1: Data Science & Data Engineering</p>", unsafe_allow_html=True)
    st.write("<p style=font-size:21px>🇭🇺 L3: Common year and international semester</p>", unsafe_allow_html=True)
    st.write("<p style=font-size:21px>📚 L2: Second year of 'classe préparatoire'</p>", unsafe_allow_html=True)
    st.write("<p style=font-size:21px>📚 L1: First year of 'classe préparatoire'</p>", unsafe_allow_html=True)
    
st.write('<br>', unsafe_allow_html=True)
st.write('<br>', unsafe_allow_html=True)

col1, col2 = st.columns([0.75, 1])

with col1:
    st.write('<br>', unsafe_allow_html=True)
    st.write('<br>', unsafe_allow_html=True)
    st.image('./images/MCM.png', width=300)
    
with col2:
    st.write("<h4><u><b>🇲🇾 Marlborough College Malaysia</b></u></h4>", unsafe_allow_html=True)
    st.write("<p style=font-size:21px>👨🏼‍🎓 Upper 6th: Final year of International Baccalaureate</p>", unsafe_allow_html=True)
    st.write("<p style=font-size:21px>👨🏼‍🎓 Lower 6th: First year of International Baccalaureate</p>", unsafe_allow_html=True)
    st.write("<p style=font-size:21px>📚 Hundred: Final year of iGCSE Diploma</p>", unsafe_allow_html=True)
    st.write("<p style=font-size:21px>📚 Remove: Second year preparing the iGCSE Diploma</p>", unsafe_allow_html=True)
    st.write("<p style=font-size:21px>📚 Shell: First year preparing the iGCSE Diploma</p>", unsafe_allow_html=True)