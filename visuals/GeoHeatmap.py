import folium
import pandas as pd
from folium import Choropleth, GeoJsonPopup

attr = (
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
    'contributors, &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'
)
tiles = "https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png"

def GeoHeatmap(data, geojson_data):
    
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
        highlight_function=lambda feature: {'weight': 3, 'color': 'blue'}
    ).add_to(m)

    
    return m