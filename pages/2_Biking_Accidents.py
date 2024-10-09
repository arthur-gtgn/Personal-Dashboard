import streamlit as st
import pandas as pd
import altair as alt

# Import the Altair charts from the provided scripts
# Assuming the scripts contain a function that returns an Altair chart
from visuals.CountDistribution import CountDistribution
from visuals.GravDistributionByAge import GravDistributionByAge
from visuals.GravDistributionByAgeYear import GravDistributionByAgeYear

def select_gravity_df(df):
    out = data.groupby(['age', 'grav']).size().reset_index(name='count')
    out['grav'] = out['grav'].replace({1: 'Indemne', 2: 'Tué', 3: 'Blessé hospitalisé', 4: 'Blessé léger'})
    out = out.sort_values(by='age')
    return out

st.set_page_config(page_title="Biking accidents: insights from the data", page_icon=":shark:", layout="wide")

# Set the title of the Streamlit app
st.title("Biking accidents: insights from the data")

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

st.subheader("Raw Data")
st.code(code, language='python')
st.write(data)

count_df = select_gravity_df(data)

# Display the first chart (count distribution)
st.subheader("Count Distribution Chart")
count_distribution_chart = CountDistribution(data=data)
st.altair_chart(count_distribution_chart, use_container_width=True)

# Display the second chart (gravity distribution by age)
st.subheader("Gravity Distribution by Age Chart")
grav_distribution_chart = GravDistributionByAge(count_df=count_df)
st.altair_chart(grav_distribution_chart, use_container_width=True)

# Add a dropdown menu to select a year
selected_year = st.selectbox("Select Year", data['an'].unique())

count_df1 = select_gravity_df(data[data['an'] == selected_year])

st.write(count_df1)
# Display the third chart (gravity distribution by age for a specific year)
st.subheader(f"Gravity Distribution by Age for {selected_year}")
grav_distribution_year_chart = GravDistributionByAgeYear(df=count_df1, year=selected_year)
st.altair_chart(grav_distribution_year_chart, use_container_width=True)