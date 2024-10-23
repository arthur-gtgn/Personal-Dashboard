import pandas as pd
import altair as alt

def DateTimeHeatmap(data):
    # Convert the 'hrmn' column to datetime to extract the hour
    data['hrmn'] = pd.to_datetime(data['hrmn'], format='%H:%M')
    data['accident_hour'] = data['hrmn'].dt.hour  # Extract the hour from the time

    # Ensure 'jour' is in English and properly ordered
    day_mapping = {
        'lundi': 'Monday', 'mardi': 'Tuesday', 'mercredi': 'Wednesday',
        'jeudi': 'Thursday', 'vendredi': 'Friday', 'samedi': 'Saturday', 'dimanche': 'Sunday'
    }
    data['day_of_week'] = data['jour'].map(day_mapping)

    # Group the data by 'day_of_week' and 'accident_hour' to get the count of accidents
    accident_counts = data.groupby(['day_of_week', 'accident_hour']).size().reset_index(name='count')

    # Ensure the days are sorted in the correct order
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Create the heatmap using Altair
    return alt.Chart(accident_counts).mark_rect().encode(
        x=alt.X('accident_hour:O', title='Hour of the Day'),
        y=alt.Y('day_of_week:O', sort=days_order, title='Day of the Week'),
        color=alt.Color('count:Q', scale=alt.Scale(scheme='reds'), title='Number of Accidents'),
        tooltip=[
        alt.Tooltip('day_of_week', title='Day of Accidents'),
        alt.Tooltip('accident_hour:O', title='Hour of the Day'),  
        alt.Tooltip('count:Q', title='Number of Accidents')  
    ]
    ).properties(
        title={
            "text": "Accidents on the clock ⏱️",
        },
        width=600,
        height=400
    ).interactive()