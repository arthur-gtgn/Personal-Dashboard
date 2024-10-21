import streamlit as st 
import pandas as pd
from sidebar import write_sidebar

st.set_page_config(page_title="Uber Data", page_icon=":shark:", layout="wide")

st.title("Uber Data - April 2014")

write_sidebar()

data = pd.read_csv("data/Uber2.csv")
st.write(data)


