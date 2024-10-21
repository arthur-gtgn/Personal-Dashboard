import altair as alt

def CountDistribution(data):

    alt.data_transformers.disable_max_rows()

    line = alt.Chart(data).mark_line(interpolate='monotone').encode(
        x=alt.X('an:N', title='Year'),
        y=alt.Y('count()', title='Number of accidents'),
        color=alt.value('grey'),
    ).properties(
        width=1150,
        height=300,     
    ).interactive()

    area = alt.Chart(data).mark_area(interpolate='monotone').encode(
        x=alt.X('an:N'),
        y='count()',
        color=alt.value('grey'),
        opacity=alt.value(0.1)
    ).properties(
        width=1150,
        height=300
    ).interactive()

    points = alt.Chart(data).mark_point(filled=True, interpolate='monotone', size=70).encode(
        x=alt.X('an:N'),
        y='count()',
        color=alt.Color('count()', scale=alt.Scale(scheme='redyellowgreen', reverse=True)),
    ).interactive()

    chart = (line + points + area).configure_axis(
        grid=False,
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        anchor='start', 
        fontSize=16,  
        subtitleFontSize=12
    ).properties(
        title={
            "text": "Distribution of accidents by year",
            "subtitle": "Chart showing the evolution of the number of accidents per year",
        }
    ).interactive()

    return chart