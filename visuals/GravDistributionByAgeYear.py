import altair as alt

def GravDistributionByAgeYear(df, year):
    return alt.Chart(df).mark_bar().encode(
        x=alt.X('age:O', title='Victim age'),
        y=alt.Y('count:Q', title='Number of accidents'),
        color=alt.Color('grav:N', title='Category',
                scale=alt.Scale(domain=['Indemne', 'Blessé léger', 'Blessé hospitalisé', 'Tué'],
                        range=['#005EFF', '#78C2FF', '#FFA1A2', '#FF2629'])),
        order=alt.Order('order:Q', sort='descending')
    ).transform_calculate(
        order=alt.expr.if_(alt.datum.grav == 'Indemne', 0,
                alt.expr.if_(alt.datum.grav == 'Blessé léger', 1,
                alt.expr.if_(alt.datum.grav == 'Blessé hospitalisé', 2, 3)))
    ).properties(
        title={"text": f"Severity of accidents per age in {year} 📊"},
        width=1150, height=400
    ).configure_title(anchor='start', fontSize=16, subtitleFontSize=12
    ).configure_axis(labelFontSize=12, titleFontSize=14)