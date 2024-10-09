import altair as alt

def GravDistributionByAge(count_df):
    chart = alt.Chart(count_df).mark_bar().encode(
        x=alt.X('age:O', title='Victim age'),  # Ordinal scale for years, no x-axis title
        y=alt.Y('count:Q', title='Number of accidents'),  # Quantitative y-axis with label
        color=alt.Color('grav:N', title='Category')  # No legend for the color
    ).properties(
        title={
            "text": "The gravity of accidents by age",
            "subtitle": "Distribution of accidents by age and gravity",
        }
    ).configure_title(
        anchor='start',  # Aligns the title to the start
        fontSize=16,  # Sets the title font size
        subtitleFontSize=12  # Sets the subtitle font size
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).properties(
        width=1150,  # Set chart width
        height=400,  # Set chart height
    )

    # Display the chart
    return chart