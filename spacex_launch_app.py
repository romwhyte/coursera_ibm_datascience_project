# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_site = spacex_df["Launch Site"].unique().tolist()
launch_site.insert(0,"ALL")
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                 dcc.Dropdown(id='site-dropdown', 
                                                     # Update dropdown values using list comphrehension
                                                     options=[{'label': i, 'value': i} for  i in launch_site],
                                                     value = 'ALL',
                                                     placeholder="Select a Launch Site Here",
                                                          searchable  = 'True'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',min=0,max=10000,step=1000, value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart',component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))

# Add computation to callback function and return graph
def get_pie(launch_site):

    if launch_site == 'ALL':
        data = spacex_df.groupby(['Launch Site']).sum().reset_index()
        fig = px.pie(data, values='class', names='Launch Site', title='Mission Success Rate')
        return fig
    else:
        data = spacex_df[spacex_df['Launch Site'] == launch_site]["class"].value_counts().to_frame().reset_index()
        fig = px.pie(data, values='class', names='index', title='Mission Success Rate')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter(launch_site,payload):
    print(payload)
    if launch_site == 'ALL':
        data = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])]
        fig = px.scatter(data, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                 title='Report on Payload Mass vs Success Rate')
        return fig
    else:
        data = spacex_df[(spacex_df['Launch Site'] == launch_site) & (spacex_df['Payload Mass (kg)'].between(payload[0],payload[1]))]
        fig = px.scatter(data, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                 title='Report on Payload Mass vs Success Rate')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
