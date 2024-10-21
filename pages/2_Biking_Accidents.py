import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import geopandas as gpd # type: ignore
print(gpd.__version__)
from sidebar import write_sidebar
import json

# Import the Altair charts from the provided scripts
# Assuming the scripts contain a function that returns an Altair chart
from visuals.CountDistribution import CountDistribution
from visuals.GravDistributionByAge import GravDistributionByAge
from visuals.GravDistributionByAgeYear import GravDistributionByAgeYear
from visuals.GeoHeatmap import GeoHeatmap

# Load the GeoJSON data
with open('/Users/arthurgatignol/Developer/Personal-Dashboard/data/france-departments.geojson', 'r') as f:
    geojson_data = json.load(f)


def select_gravity_df(data):
    out = data.groupby(['age', 'grav']).size().reset_index(name='count')
    out['grav'] = out['grav'].replace({1: 'Indemne', 2: 'Tué', 3: 'Blessé hospitalisé', 4: 'Blessé léger'})
    out = out.sort_values(by=['age', 'grav'])
    return out

st.set_page_config(page_title="Biking Accidents: Insights from the data", page_icon=":bar_chart:", layout="wide")

write_sidebar()

# Set the title of the Streamlit app
st.title("Biking accidents: Insights from the data")

# Add some description or instructions
st.write("""
This dashboard displays two different Altair visualizations. 
One shows the count distribution and the other shows the distribution of gravity by age.
""")

data = pd.read_csv("data/AccidentsVeloNum.csv")
data['age'] = data['age'].apply(lambda x: 2022 - x if x > 2000 else x)

code = """
data = pd.read_csv("data/AccidentsVeloNum.csv")
data['age'] = data['age'].apply(lambda x: 2022 - x if x > 2000 else x)
"""

st.divider()

st.subheader("Raw Data")
st.code(code, language='python')
st.write(data)

count_df = select_gravity_df(data)

st.divider()

# Display the first chart (count distribution)
st.subheader("Distribution of the number of accidents")
count_distribution_chart = CountDistribution(data=data)
st.altair_chart(count_distribution_chart, use_container_width=True)

# Display the second chart (gravity distribution by age)
st.subheader("Gravity Distribution by Age")
grav_distribution_chart = GravDistributionByAge(count_df=count_df)
st.altair_chart(grav_distribution_chart, use_container_width=True)

# Add a dropdown menu to select a year
selected_year = st.selectbox("Select Year", data['an'].unique())
count_df1 = select_gravity_df(data[data['an'] == selected_year])

# Display the third chart (gravity distribution by age for a specific year)
st.subheader(f"Gravity Distribution by Age for {selected_year}")
grav_distribution_year_chart = GravDistributionByAgeYear(df=count_df1, year=selected_year)
st.altair_chart(grav_distribution_year_chart, use_container_width=True)


st.divider()

st.subheader("Geographical heatmap of the number of accidents per department")
m = GeoHeatmap(data, geojson_data)
st.components.v1.html(m._repr_html_(), width=700, height=500)
