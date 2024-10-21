import streamlit as st
import pandas as pd
import base64
import json

# Import the Altair charts from the provided scripts
# Assuming the scripts contain a function that returns an Altair chart
from visuals.CountDistribution import CountDistribution
from visuals.GravDistributionByAge import GravDistributionByAge
from visuals.GravDistributionByAgeYear import GravDistributionByAgeYear
from visuals.GeoHeatmap import GeoHeatmap
from visuals.DateTimeHeatmap import DateTimeHeatmap
from sidebar import write_sidebar
from Portfolio import underlined_subheader

# --------------------------------- Data Loading & Function Declaration -------------------------------------
# Load the GeoJSON data
with open('/Users/arthurgatignol/Developer/Personal-Dashboard/data/france-departments.geojson', 'r') as f:
    geojson_data = json.load(f)

def change_time(x:str) -> str:
    x = x.split(':')
    if int(x[0]) >= 24:
        x[1] = str(x[0][-1] + x[1])
        x[0] = '0' + x[0][0]
        return ':'.join(x)
    elif x[1] == '':
        return x[0] + ':00'
    else:
        return ':'.join(x)

def select_gravity_df(data):
    out = data.groupby(['age', 'grav']).size().reset_index(name='count')
    out['grav'] = out['grav'].replace({1: 'Indemne', 2: 'Tué', 3: 'Blessé hospitalisé', 4: 'Blessé léger'})
    out = out.sort_values(by=['age', 'grav'])
    return out

# --------------------------------------- Page configuration ------------------------------------------------

st.set_page_config(page_title="Biking Accidents: Insights from the data", page_icon=":bar_chart:", layout="wide")

image_path = './images/french_bike.webp'
with open(image_path, "rb") as image_file:
    image_bytes = image_file.read()
    encoded_image = base64.b64encode(image_bytes).decode()


st.sidebar.write(f"""
<div style="text-align: center;">
    <img src="data:image/png;base64,{encoded_image}" width="200" style="border-radius: 50%;">
</div>
</br>
<h2><u>Informations</u></h2>
<div style=font-size:20px>
    <b>Author:</b> Arthur Gatignol</br>
    <b>Dataset:</b> <a href="https://www.data.gouv.fr/fr/datasets/accidents-de-velo/">Biking Dataset</a></br>
    <b>Source code:</b> <a href="https://github.com/arthur-gtgn/Personal-Dashboard">GitHub</a>
</div>
""", unsafe_allow_html=True)

#----------------------------------------- Introduction ---------------------------------------------------

# Set the title of the Streamlit app
st.title("Biking Accidents in France 🇫🇷")
st.write("""
<h3><i>When data tells a story...</i></h3>
""", unsafe_allow_html=True)
st.write("""
<p style=font-size:20px>
We have all seen the ads on TV warning us about the possible dangers of biking, especially in urban areas. We all know
the safety measures that can be taken to prevent accidents. But what do the numbers say? What are the most common reasons
for bike accidents? Who are the most affected? Let's dive into the data and find out!
</p>
""", unsafe_allow_html=True)

data = pd.read_csv("data/AccidentsVeloNum.csv")
data['age'] = data['age'].apply(lambda x: 2022 - x if x > 2000 else x)
data['hrmn'] = data['hrmn'].apply(lambda x: change_time(str(x)))


code = """
data = pd.read_csv("data/AccidentsVeloNum.csv")
data['age'] = data['age'].apply(lambda x: 2022 - x if x > 2000 else x)
data['hrmn'] = data['hrmn'].apply(lambda x: change_time(str(x)))
"""

time_function = """
def change_time(x:str) -> str:

    x = x.split(':') # Split the time into an array where [0] is the hour and [1] is the minute
    
    if int(x[0]) >= 24:
        x[1] = str(x[0][-1] + x[1]) # Add the last digit of the hour to the minute
        x[0] = '0' + x[0][0] # Add a '0' in front of the first digit of the hour
        return ':'.join(x) # Join the array back into a string
        
    elif x[1] == '':
        return x[0] + ':00' # Add ':00' to the time if the minute is missing
        
    else:
        return ':'.join(x) # Join the array back into a string if nothing is wrong
"""

# ------------------------------------------ Data Importation --------------------------------------

st.divider()

underlined_subheader('Raw data')

st.write("""
<p style=font-size:18px>
The code used to load tha data is pretty simple at first. However, an issue appeared with the 'hrmn' column where times 
like '9:30' would be interpreted as '93:0'. To fix this, I created a function that would add a '0' in front of the hour 
if the hour was greater than 24. This way, the time would be correctly interpreted as '09:30'.
</p>
""", unsafe_allow_html=True)

st.code(code, language='python')

st.write("<p style=font-size:18px>Here is the function used to fix the 'hrmn' column:</p>", unsafe_allow_html=True)

st.code(time_function, language='python')

st.write("""
<p style=font-size:18px>
After making the correct pre-processing and cleaning steps, we can finally observe some of the insights.
Here is what the final dataframe used throughout this dashboard looks like:
</p>
""", unsafe_allow_html=True)

st.write(data)

# ------------------------------------------ Data Distribution --------------------------------------

st.divider()

count_df = select_gravity_df(data)

# First chart: Distribution of the number of accidents
underlined_subheader("Overlook of the general trends 📈")

st.write("""
<p style=font-size:18px>
When dealing with time-series, the first question that always comes to mind is: "How has the data evolved over the years?".
To visualize this, we can always plot a line chart of the data. In this case, we are looking at the number of accidents per year.
</p>
""", unsafe_allow_html=True)
st.write('<br>', unsafe_allow_html=True)
st.altair_chart(CountDistribution(data=data), use_container_width=True)

# Second chart: Population distribution by age
st.write("""
<p style=font-size:18px>
Now, one of the advantages of having a dataset produced by the government is that we have access to a lot of information. Especially
population information. In this case, I tried to map the overall distribution of the severity of the accidents based on the victim's
age. This way, we can see if there is a pattern in the age groups most affected by bike accidents.
</p>
""", unsafe_allow_html=True)
st.write('<br>', unsafe_allow_html=True)
st.altair_chart(GravDistributionByAge(count_df=count_df), use_container_width=True)

# ------------------------------------------ Yearly Analysis --------------------------------------

st.divider()

underlined_subheader(f'Yearly Analysis 📊')
st.write("""
<h4><i>Towards safer biking?</i></h4>
<p style=font-size:18px>
The aim of this section is to provide a more detailed analysis of the data. By selecting a specific year, we can explore different
visuals to better unterstand the population affected, the gravity of the accidents, the causes... Through these detailed insights,
we can hope to have a conclusion on the evolution of biking accidents over the years.</br>
</br>
We can first start by selecting the year we want to analyze through the dropdown menu below.
</p>
""", unsafe_allow_html=True)

# Add a dropdown menu to select a year
selected_year = st.selectbox("Select Year", data['an'].unique())
data_per_year = select_gravity_df(data[data['an'] == selected_year])

# Display the third chart (gravity distribution by age for a specific year)

grav_distribution_year_chart = GravDistributionByAgeYear(df=data_per_year, year=selected_year)
st.altair_chart(grav_distribution_year_chart, use_container_width=True)

GeoHeatmap(data, geojson_data, selected_year)

st.altair_chart(DateTimeHeatmap(data), use_container_width=True)