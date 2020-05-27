# Import Libraries


import pandas as pd
import plotly.graph_objects as go
import os
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# Auxiliary functions ---------------------------------------------------------

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


# Path where the csv files are and the extension that we want DB2 - with the indicatores per column
df1 = pd.read_csv('Dataset_Comb_Final1.csv')
df2 = pd.read_csv('world.csv')

# First world map
fig1 = px.choropleth(df1, locations=df1['Code'],
                     color=df1["Happiness scores"], color_discrete_sequence=["#02818a", "#67a9cf",  "#bdc9e1", "#f6eff7"],
                     hover_name=df1["Country"] + " Rank Position: " + df1["Happiness Rank"].astype(str),
                     animation_frame=df1["Year"])

fig1.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=False,
        showocean=True,
        oceancolor='#f9f9f9',
        projection_type='equirectangular'),width=1000,height=800,
    plot_bgcolor='white',
    paper_bgcolor='rgba(0,0,0,0)',
    showlegend=True,
    font=dict( size=22)
)


# Second Line PLOT ------------------------------------------------------
y = df2['Score']
x = df2['Year']

fig2 = go.Figure(data=go.Scatter(x=x, y=y, line_color="gray"))
fig2.update_layout(
    # title='World Happiness score',
    xaxis_title='Year',
    yaxis_title='Happiness Score',
    xaxis=dict(
        tickmode='array',
        tickvals=[2015, 2016, 2017, 2018, 2019],
        ticktext=[2015, 2016, 2017, 2018, 2019]),
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(
        size=19)
)

# Third Plot with default values -----------------------------------------
filtered_by_year_df = df1[df1['Year'] == 2015]

y_parameters = ['GDP per capita', 'Social support', 'Healthy life expectancy', 'Freedom to make life choices',
                'Generosity', 'Perceptions of corruption']

data = []

filtered_by_year_and_country_df = filtered_by_year_df[filtered_by_year_df['Country'] == 'Portugal']

# Forth PLOT ---------------------------------------------------------------------

A = df1[['Year', 'Continent', 'Happiness score']]
fig4 = px.histogram(A, x="Continent", y='Happiness score', histfunc='avg', animation_frame="Year",
                    color_discrete_sequence=['#02818a'])



fig4.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)', }, xaxis_title='Continent',
    yaxis_title='Score', font=dict(
        size=19))

# Interactive Components ---------------------------------------------------------

country_options = [dict(label=country, value=country) for country in df1["Country"].unique()]

dropdown_country = dcc.Dropdown(
    id='country_drop',
    options=country_options,
    multi=True
)

# DASH App --------------------------------------------------------------------

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(children='HAPPINESS WORLDWIDE 2015-2019',
                        className='card-title',
                        style={'textAlign': 'center','color': 'teal'}
                        ),
            ],
            className='box'
        ),
        html.Div(
            [
                html.H4(children='This dashboard presents an overview of the happiness score worldwide.'
                                 ''
                                 '  Happiness is described by the status of 6 indicators: GDP per capita, Social support, Healthy life expectancy, freedom to make life choices, Generosity, and Perception of the corruption.'
                                 ''
                                 '  This story starts with a map look, where it is possible to see the evolution of the happiness score ranges across years, developed countries are the  happier ones and in development the less happier - with a clear exception of South America countries. '
                                 ''
                                 '  Then, the line chart shows the total world score per year, where is visible a decrease in the last year. '
                                 ''
                                 '  In terms of regions, the bar chart on the right shows that Oceania is the happier region in all years.'
                                 '        '
                                 '  Last, the interactive bar chart on the bottom allows us to check the indicators per country and year so you can do a lot of combinations. More than one country can be selected.',
                        className='card-title',
                        style={'textAlign': 'left', 'font-size': '30px', 'color': 'teal', 'font-family': 'Calibri', 'font-weight': 'normal'}
                        ),
            ],
            className='box'
        ),

        # Main container with 3 sub containers
        html.Div(
            [
                # Left Sub container
                html.Div(
                    [
                        html.Div(
                            # Figure Title
                            html.H2(children='Happiness Score per country and year',
                                    className='card-title',
                                    style={'textAlign': 'center','color': 'dimgray','font-family': 'Calibri', 'font-weight': 'bold'},
                                    ),
                            className='card_header',
                        ),

                        # Figure Image
                        dcc.Graph(
                            id='Happiness Scores',
                            figure=fig1,
                            style={'margin': '5px 5px', 'Align': 'right'}
                        )
                    ],
                    style={'width': '45%', 'margin': '10px 10px'},
                    className='new_box'
                ),

                # Middle Sub container
                html.Div(
                    [
                        html.Div(
                            # Figure Title
                            html.H2(children='World Happiness Score',
                                    className='card-title',
                                    style={'textAlign': 'center','color': 'dimgray','font-family': 'Calibri', 'font-weight': 'bold'}
                                    ),
                            className='card_header',
                        ),

                        dcc.Graph(
                            id='World Happiness Scores',
                            figure=fig2,
                            style={'margin': '20px 20px'}
                        )
                    ],
                    style={'width': '25%', 'margin': '10px 10px'},
                    className='new_box'
                ),

                # Right Sub container
                html.Div(
                    [
                        html.Div(
                            # Figure Title
                            html.H2(children='Average Happiness Score By Region',
                                    className='card-title',
                                    style={'textAlign': 'center','color': 'dimgray','font-family': 'Calibri', 'font-weight': 'bold'}
                                    ),
                            className='card_header',
                        ),

                        dcc.Graph(
                            id='Average Happiness Score By Region',
                            figure=fig4,
                            style={'margin': '10px 10px'}
                        )
                    ],
                    style={'width': '30%', 'margin': '10px 10px'},
                    className='new_box'
                ),
            ],
            style={'display': 'flex'}
        ),

        # Main container with 2 sub containers
        html.Div(
            [
                # Left Sub container
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2(children='Countries',
                                        className='card-title',
                                        style={'textAlign': 'center','color': 'dimgray','font-family': 'Calibri', 'font-weight': 'bold'}
                                        ),

                                # Range Slider for the Countries
                                dcc.Dropdown(
                                    id='country_drop',
                                    options=country_options,
                                    multi=True,
                                    value=['Portugal', 'United Kingdom'],
                                    style={'font-size': '26px', 'font-family': 'Calibri', 'font-weight': 'normal'}
                                )
                            ],
                            style={'margin': '5px 10px', 'width': '70%'},
                            className='box_filters'
                        ),
                        html.Br(),
                        html.Div(
                            [
                                html.H2(children='Year',
                                        className='card-title',
                                        style={'textAlign': 'center','color': 'dimgray','font-family': 'Calibri', 'font-weight': 'bold'}
                                        ),

                                html.Br(),

                                dcc.RadioItems(
                                    id='year_selection',
                                    options=[dict(label='2015', value=2015),
                                             dict(label='2016', value=2016),
                                             dict(label='2017', value=2017),
                                             dict(label='2018', value=2018),
                                             dict(label='2019', value=2019)],
                                    value=2015,
                                    labelStyle={'display': 'block', 'font-size': '26px', 'font-family': 'Calibri'},
                                    style={'textAlign': 'center'},
                                )
                            ],
                            style={'margin': '5px 10px', 'width': '30%'},
                            className='box_filters'
                        ),
                    ],
                    style={'margin': '0px 5px', 'display': 'flex', 'width': '25%'},
                    # className = 'box'
                ),

                # Right Sub container
                html.Div(
                    [
                        html.Div(
                            html.H2(children='Happiness Indicators per Country and Year',
                                    className='card-title',
                                    style={'textAlign': 'center','color': 'dimgray','font-family': 'Calibri','font-weight':'bold'}
                                    ),
                            className='card_header',
                        ),

                        html.Br(),

                        dcc.Graph(
                            id='Happiness Indicators',
                            # figure = fig3
                        )
                    ],
                    style={'margin': '5px 5px', 'width': '75%'},
                    className='new_box'
                )
            ],
            style={'display': 'flex'}
        ),
                html.Div(
                                            [
                                                html.H4(children='Data Source: World Happiness Report on: https://worldhappiness.report/archive/',
                                                        className='card-title',
                                                        style={'textAlign': 'right', 'font-size': '20px', 'color': 'teal', 'font-family': 'Calibri', 'font-weight': 'normal'}
                                                        ),
                                            ],
                                            className='box'
                                        ),
                html.Div(
                            [
                                html.H4(children='Made by: Sofia Santos, Fabiola Mousinho, Ana Beatriz, Ana Catarina',
                                        className='card-title',
                                        style={'textAlign': 'left', 'font-size': '20px', 'color': 'teal', 'font-family': 'Calibri', 'font-weight': 'normal'}
                                        ),
                            ],
                            className='box'
                        )
]
)


# CALLBACK --------------------------------------------------------------------

@app.callback(
    Output('Happiness Indicators', 'figure'),
    [Input('country_drop', 'value'),
     Input('year_selection', 'value')]
)
def update_graph(countries, year):
    filtered_by_year_df = df1[df1['Year'] == year]

    y_parameters = ['GDP per capita', 'Social support', 'Healthy life expectancy', 'Freedom to make life choices',
                    'Generosity', 'Perceptions of corruption']

    data = []

    for country in countries:

        filtered_by_year_and_country_df = filtered_by_year_df[filtered_by_year_df['Country'] == country]



        # Check if is the last country of the list. Last one has legend activated
        if country == countries[-1]:
            is_last = True
        else:
            is_last = False

        temp_data_1 = dict(
            type='bar',
            x=filtered_by_year_and_country_df['Country'],
            y=filtered_by_year_and_country_df['GDP per capita'],
            legendgroup="group",
            offsetgroup=0,
            name='GDP per capita',
            marker_color='#02818a',
            showlegend=is_last
        )

        temp_data_2 = dict(
            type='bar',
            x=filtered_by_year_and_country_df['Country'],
            y=filtered_by_year_and_country_df['Social support'],
            legendgroup="group",
            offsetgroup=1,
            name='Social support',
            marker_color='gold',
            showlegend=is_last
        )

        temp_data_3 = dict(
            type='bar',
            x=filtered_by_year_and_country_df['Country'],
            y=filtered_by_year_and_country_df['Healthy life expectancy'],
            legendgroup="group",
            offsetgroup=2,
            name='Healthy life expectancy',
            marker_color='LightSteelBlue',
            showlegend=is_last
        )

        temp_data_4 = dict(
            type='bar',
            x=filtered_by_year_and_country_df['Country'],
            y=filtered_by_year_and_country_df['Freedom to make life choices'],
            legendgroup="group",
            offsetgroup=3,
            name='Freedom to make life choices',
            marker_color='#225ea8',
            showlegend=is_last
        )

        temp_data_5 = dict(
            type='bar',
            x=filtered_by_year_and_country_df['Country'],
            y=filtered_by_year_and_country_df['Generosity'],
            legendgroup="group",
            offsetgroup=4,
            name='Generosity',
            marker_color='MediumTurquoise',
            showlegend=is_last

        )

        temp_data_6 = dict(
            type='bar',
            x=filtered_by_year_and_country_df['Country'],
            y=filtered_by_year_and_country_df['Perceptions of corruption'],
            legendgroup="group",
            offsetgroup=5,
            name='Perceptions of corruption',
            marker_color='LightSlateGray',
            showlegend=is_last
        )

        data.append(temp_data_1)
        data.append(temp_data_2)
        data.append(temp_data_3)
        data.append(temp_data_4)
        data.append(temp_data_5)
        data.append(temp_data_6)

    scatter_layout = dict(xaxis=dict(title=str(year)),
                          yaxis=dict(title='Score'),
                          paper_bgcolor='#f9f9f9',
                          bargap=0.15,  # gap between bars of adjacent location coordinates.
                          bargroupgap=0.1,  # gap between bars of the same location coordinate.
                          font=dict(
                              family='sans-serif',
                              size=22,
                              color='#000'
                          ),
                          hovermode="x unified"
                          )

    fig3 = go.Figure(data=data, layout=scatter_layout)

    fig3.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0,0,0,0)',
        uniformtext_minsize=22,
        font=dict(
            family='sans-serif',
            size=22,
            color='#000')
    )

    return fig3


if __name__ == '__main__':
    # Preparation
    cls = cls()
    # Run App
    app.run_server(debug=True, host='127.0.0.1', port=8050)