import streamlit as st 
import pandas as pd
from tools.sidebar import write_sidebar
from Portfolio import underlined_subheader
import plotly.express as px

st.set_page_config(page_title="Uber Data", page_icon=":shark:", layout="wide")

st.title("Uber Data - April 2015")

write_sidebar()

df = pd.read_csv("data/Uber2.csv")
st.write(df)

st.divider()

underlined_subheader('New-York City on the move 🚖')

st.write("""
<p style='font-size: 18px;'>
I chose to showcase the Uber animation I managed to create using the data provided. The animation
was created using the <code>geopandas</code> and <code>matplotlib</code> libraries. I chose to use
a GIF format to display the animation, as it is the least resource-intensive format for this type
of visualization. Each point on the map represents a pickup location at a specific time of the day.
The aim is to showcase the power of data visualization and the insights that can be drawn from it.
.</p><br>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.image('./images/map_anim.gif', use_column_width=True)
    
with col2:
    code = """
    import geopandas as gpd
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from shapely.geometry import Point
    import contextily as ctx
    import pandas as pd

    # Changing the type of time columns to integers
    df['Day'] = df['Day'].astype(int)
    df['Hour'] = df['Hour'].astype(int)

    # Create the GeoDataFrame using the coordinates in df
    geometry = [Point(xy) for xy in zip(df['Lon'], df['Lat'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    # Defining the width of the map
    xmin, xmax = -74.025, -73.95
    ymin, ymax = 40.65, 40.8

    # Setting the map limits within the frame
    fig, ax = plt.subplots(figsize=(10, 20)) 
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.axis('off') 
    
    # Adding a basemap for better visualization
    ctx.add_basemap(ax, crs=gdf.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik, zoom=14)

    # Save the basemap as an image with the correct aspect ratio
    plt.savefig('basemap.png', bbox_inches='tight', pad_inches=0, dpi=300)
    plt.close()

    # Group by 'Day' and 'Hour'
    grouped = gdf.groupby(['Day', 'Hour'])

    # Load the saved basemap image
    basemap_img = plt.imread('basemap.png')

    # Set up the figure and axis with fixed size
    fig, ax = plt.subplots(figsize=(10, 20)) 

    # Prepare a list of (Day, Hour) tuples for iteration
    day_hour_list = list(grouped.groups.keys())

    # Function to update the image for each frame
    def update(i):
        # Clear the plot
        ax.clear()

        # Display the preloaded basemap with the correct aspect ratio
        ax.imshow(basemap_img, extent=[xmin, xmax, ymin, ymax], aspect='auto')

        # Get the current Day and Hour
        day, hour = day_hour_list[i]
        
        # Filter data for the current Day and Hour
        current_data = grouped.get_group((day, hour))
        
        # Plot the coordinate point on the map
        current_data.plot(ax=ax, marker='*', color='red', markersize=5)

        # Set fixed x and y axis limits again
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)

        # Add plot title
        ax.set_title(f'Scatter Plot for Day {day}, Hour {hour}')

    # Compile all the updates into an animation
    ani = animation.FuncAnimation(fig, update, frames=len(day_hour_list), interval=1000, repeat=False)

    # Save the animation as a GIF
    ani.save(filename='map_anim.gif', writer='imagemagick', dpi=50, fps=10)
    """
    
    st.code(code, language='python')