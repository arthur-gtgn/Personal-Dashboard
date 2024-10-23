import streamlit as st
import altair as alt
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
from tools.sidebar import write_sidebar
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

cat_data = pd.read_csv('data/AccidentsVeloCat.csv')
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
st.write(f"""
<p style=font-size:18px>
Now that we are able to select partial amounts of the data, corresponding to a specific year, we can start to analyze the
trends observed through the years simply by selecting the year we want to analyze. In this case, we are looking at the distribution
of the severity of the accidents based on the victim's age for {selected_year}.</br>
</p>

<p style=font-size:18px>
Depending on the year you selected, you can see that the distribution resembles the general trends observed in the previous section.
However, in 2017 and after, we can see a decrease in the number of accidents and a more homogeneous distribution of the severity of the accidents.
</p>
""", unsafe_allow_html=True)
grav_distribution_year_chart = GravDistributionByAgeYear(df=data_per_year, year=selected_year)
st.altair_chart(grav_distribution_year_chart, use_container_width=True)

st.write(f"""
<p style=font-size:18px>
One of the many advantages of having government distributed data is that it usually comes with
geographical data such as department codes or coordinates. For the sake of keeping this dashboard
concise, logical and mainly too avoid breaking it with html content overload, I decided to only
use the department codes provided for each accident. This still allowed to create a heatmap using
statistical observations for scale while preserving the dashboard's fluidity.</br>
</p>

<p style=font-size:18px>
Now again, this map shows the distribution of bike accidents in each department per year. However,
I have provided a more detaied vue of the data in each region next to the overall heatmap. This way,
you can have a more detailed understanding of the distribution of the accidents in each department.
</p>
""", unsafe_allow_html=True)
GeoHeatmap(data, geojson_data, selected_year)

st.write(f"""
<p style=font-size:18px>
Finally, now that we understand the data in each year, in each region, we can also start looking at
the time data that was provided. I have therefore created a heatmap showing when we have 'booms' in
the number of biking accidents.</br>
</p>

<p style=font-size:18px>
From the visual below, and because the peak of accidents doesn't seem to change much over the years,
we can conclude that biking accidents are more likely to happen when people are commuting to work or
when kids come back from school. This is a very interesting insight that could be used to prevent 
more accidents in the future.
</p><br>
""", unsafe_allow_html=True)
st.altair_chart(DateTimeHeatmap(data[data['an'] == selected_year]), use_container_width=True)

cat_data = cat_data[cat_data['an'] == selected_year]
cat_data = cat_data.dropna(subset=['trajet'])

col1, col2 = st.columns([1, 0.75])

with col1:
    pie_chart = alt.Chart(cat_data).mark_arc().encode(
                theta='count()',
                color=alt.Color('trajet:N', title='Type de trajet',),
                tooltip=['trajet', 'count()']
            ).properties(
                width=300,
                height=300
            ).interactive()

    st.altair_chart(pie_chart, use_container_width=True)
    
with col2:
    st.write(f"""
<p style=font-size:18px>
This pie chart allows us to verify our previous hypothesis depending, again on each year. From
what we can see, it counters our previous hypothesis that was suggesting that the accidents were
caused during home-work-home trips.</br>
</p>

<p style=font-size:18px>
We can probably go further in concluding, from all the previous visuals and insights that were given in
this dashboard, that the reason for 'fun' trips to be the most common cause of accidents is because 
victims of these accidents are more likely to be kids or teenagers.
</p><br>
""", unsafe_allow_html=True)
    
st.divider()

underlined_subheader('Contextual analysis of accidents 🚦')
st.write(f"""
<p style=font-size:18px>
The goal of this section is to provide more visuals about the context of each accident.
Pie charts are used as they allow to highlight the most influencial variables. In this 
context, we can observe that most bike accidents happen within town and cities on
two-ways roads.</br>
</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    agglo = alt.Chart(cat_data).mark_arc().encode(
                theta='count()',
                color=alt.Color('agg:N', title="Cadre de l'accident",),
                tooltip=['agg', 'count()']
            ).properties(
                width=300,
                height=300
            ).interactive()

    st.altair_chart(agglo, use_container_width=True)
with col2:
    weather = alt.Chart(cat_data).mark_arc().encode(
                theta='count()',
                color=alt.Color('atm:N', title="Conditions météo",),
                tooltip=['atm', 'count()']
            ).properties(
                width=300,
                height=300
            ).interactive()
            
    st.altair_chart(weather, use_container_width=True)
    
col1, col2 = st.columns([1, 1])
with col1:
    roads = alt.Chart(cat_data).mark_arc().encode(
                    theta='count()',
                    color=alt.Color('catr:N', title="Type de route",),
                    tooltip=['catr', 'count()']
                ).properties(
                    width=300,
                    height=300
                ).interactive()

    st.altair_chart(roads, use_container_width=True)
    
with col2:
    circulation = alt.Chart(cat_data).mark_arc().encode(
                        theta='count()',
                        color=alt.Color('circ:N', title="Sens de circulation",),
                        tooltip=['circ', 'count()']
                    ).properties(
                        width=300,
                        height=300
                    ).interactive()

    st.altair_chart(circulation, use_container_width=True)