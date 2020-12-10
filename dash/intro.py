import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("intro_bees.csv")

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),
    
    #select year dropdown
    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018}],
                 multi=False,
                 value=2015,
                 style={'width': "40%"}
                 ),
    
    #display choropleth map
    html.Div(id='choropleth_container', children=[]),
    html.Br(),

    dcc.Graph(id='choropleth_map', figure={}),
    
    html.Br(),
    html.Br(),
    html.Br(),
    
    #dispaly bar graph
    html.Div(id='bar_container', children=[]),
    html.Br(),

    dcc.Graph(id='bar_map', figure={}),
    
    html.Br(),
    html.Br(),
    html.Br(),

    #select Affected by reason
    dcc.Dropdown(id='slct_affectedBy',
                options=[
                    {"label": "Disease", "value":"Disease"},
                    {"label": "Pesticides", "value":"Pesticides"},
                    {"label": "Unknown", "value":"Unknown"}],
                multi=False,
                value='Disease',
                style={'width':"40%"} 
                ),
    
    html.Br(),

    #display line graph
    #dispaly bar graph
    html.Div(id='line_container', children=[]),
    html.Br(),

    dcc.Graph(id='line_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='choropleth_container', component_property='children'),
     Output(component_id='choropleth_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def choropleth_map(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    #df processing for choropleth map
    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]
    dff = dff[dff["Affected by"] == "Varroa_mites"]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )
    

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    fig.update_layout(
        title_text="Bees Affected by Mites in the USA",
        title_xanchor="center",
        title_font=dict(size=24),
        title_x=0.5,
        geo=dict(scope='usa'),
    )

    return container, fig

@app.callback(
    [Output(component_id='bar_container', component_property='children'),
     Output(component_id='bar_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def bar_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    #df processing for bar graph
    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]
    dff = dff[dff["Affected by"] == "Varroa_mites"]

    
    #bar graph
    fig = px.bar(
        data_frame=dff,
        x='State',
        y='Pct of Colonies Impacted',
        color='Pct of Colonies Impacted',
        color_continuous_scale=px.colors.sequential.YlOrRd,  
        template='plotly_dark'
    )

    fig.update_layout(
        title_text="Bees Affected by Mites according to US states",
        title_xanchor="center",
        title_font=dict(size=24),
        title_x=0.5,
        geo=dict(scope='usa'),
    )
    return container, fig

@app.callback(
    [Output(component_id='line_container', component_property='children'),
     Output(component_id='line_map', component_property='figure')],
    [Input(component_id='slct_affectedBy', component_property='value')]
)
def line_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
    
    container = "Bees Affected due to: {}".format(option_slctd)
    #df processing for line graph
    dff = df.copy()
    dff = dff[dff['Affected by']==option_slctd]
    #keep only three states for analysis(Texas, New York, California)
    states = ['Texas', 'New York', 'California']
    dff = dff[dff['State'].isin(states)]
  
    #line graph
    fig = px.line(
        data_frame=dff,
        x='Year',
        y='Pct of Colonies Impacted',
        line_group='State',
        color='State',
        hover_name='State',
        #template='plotly_dark'
    )
    
    fig.update_layout(
        title_text="Trend of Bees affected in important states",
        title_xanchor="center",
        title_font=dict(size=24),
        title_x=0.5,
        showlegend=True,
        template='plotly_dark'
    )
    return container, fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)