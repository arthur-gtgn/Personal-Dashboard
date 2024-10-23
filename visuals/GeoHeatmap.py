import streamlit as st
import folium
import pandas as pd
from folium import Choropleth, GeoJsonPopup
import altair as alt

attr = (
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
    'contributors, &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'
)
tiles = "https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png"

def GeoHeatmap(data, geojson_data, selected_year):
    
    data = data[data['an'] == selected_year]
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        m = folium.Map(location=[46.603354, 1.888334], zoom_start=6, tiles=tiles, attr=attr)

        
        dep_counts = data['dep'].value_counts().reset_index()
        dep_counts.columns = ['dep', 'count']

        
        for feature in geojson_data['features']:
            dep_code = feature['properties']['code']
            
            count = dep_counts[dep_counts['dep'] == dep_code]['count'].values
            feature['properties']['accidents'] = int(count[0]) if len(count) > 0 else 0

        
        q25 = dep_counts['count'].quantile(0.25)  
        median = dep_counts['count'].median()     
        q75 = dep_counts['count'].quantile(0.75)  
        max_count = dep_counts['count'].max()     

        
        threshold_scale = [0, q25, median, q75, max_count]

        
        choropleth = Choropleth(
            geo_data=geojson_data,
            name='heatmap',
            data=dep_counts,
            columns=['dep', 'count'],
            key_on='feature.properties.code',
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0,  
            threshold_scale=threshold_scale,  
            legend_name='Biking Accidents (by statistical thresholds)',
            nan_fill_color='white',  
        ).add_to(m)

        
        folium.GeoJson(
            geojson_data,
            name='department_borders',
            style_function=lambda feature: {
                'fillOpacity': 0,  
                'color': 'black',  
                'weight': 1.5  
            },
            popup=GeoJsonPopup(
                fields=['nom', 'accidents'],
                aliases=['Department', 'Accidents'],
                localize=True,
                labels=True
            ),
            highlight_function=lambda feature: {'weight': 3, 'color': 'black'}
        ).add_to(m)

        st.components.v1.html(m._repr_html_(), width=600, height=550)
        
    with col2:
        
        selected_dep = st.selectbox('Select a department code', sorted(data['dep'].unique())) 
        
        data['grav'] = data['grav'].replace({1: 'Indemne', 2: 'Tué', 3: 'Blessé hospitalisé', 4: 'Blessé léger'})
        department_info = data[data['dep'] == selected_dep]
        
        department_name = ''
        for feature in geojson_data['features']:
            if feature['properties']['code'] == selected_dep:
                department_name = feature['properties']['nom']
        
        st.write(f"""
        <p style=font-size:18px>
        <b>Department:</b> {department_name}<br>
        <b>Total number of accidents:</b> {department_info.shape[0]}<br><br>
        </p>
        """, unsafe_allow_html=True)
        
        severity_counts = department_info['grav'].value_counts().reset_index()
        severity_counts.columns = ['grav', 'count']
        
        pie_chart = alt.Chart(severity_counts).mark_arc().encode(
            theta=alt.Theta(field="count", type="quantitative"),
            color=alt.Color('grav:N', title='Category',
                scale=alt.Scale(domain=['Indemne', 'Blessé léger', 'Blessé hospitalisé', 'Tué'],
                        range=['#005EFF', '#78C2FF', '#FFA1A2', '#FF2629'])),
            tooltip=['grav', 'count']
        ).properties(
            width=300,
            height=300
        )

        st.altair_chart(pie_chart, use_container_width=True)