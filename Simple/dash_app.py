"""
MPE University 
November 2022
=====================

Creating powerful data analysis applications with dash in python
jjcalvom

=====================

Simple Dash Application Example

"""

import dash

# Import libraries/extensions for layouts 
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

# Import libraries/extensions for callbacks
from dash.dependencies import Input, Output, State

# Import utils for calculations
import pandas as pd
import plotly.express as px

data = pd.read_csv("data_example.csv")
data = data.astype(str)
data[['cl_incoming', 'radius', 'workweek']] = data[['cl_incoming', 'radius', 'workweek']].astype(float)

devrevstep_list = data['devrevstep'].unique().tolist()
facility_list = data['ppv_site'].unique().tolist()

data_to_graph = pd.DataFrame(
    data[data['final_bucket_name'].isin(['THe','THc'])].groupby([
        'final_bucket_name', 's_spec'],
                 as_index=False).agg(count=('cl_incoming', 'count'))
    )
fig = px.bar(
    data_to_graph, x="final_bucket_name", y="count",
    color='s_spec')

# Create a dash object
# Use external stylesheets from Bootstrap if you want to use bootstrap css style.
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(external_stylesheets=external_stylesheets)

# Create layout #

app.layout = html.Div([
    
    # Header 
    html.H1("Welcome to our dash app example."),
    html.H2("With this example, I hope you can become a bit familiar with the layout-callback model in dash."),
    html.P("MPE University Nov 2022. jjcalvom."),
    html.Hr(),
    
    # Card with dropdowns
    dbc.Card([
        dbc.CardBody([
            
            html.P("Please select a value in these dropdowns to filter the data:"),
            
            # Row with dropdowns
            dbc.Row([
                
                dbc.Col([
                   dcc.Dropdown(id = 'devrevstep_dropdown',
                         multi = True,
                         clearable = True,
                         disabled = False,
                         placeholder = 'Select DevRevStep',
                         value = [devrevstep_list[0]],
                         options = [{'label': c, 'value': c} for c in devrevstep_list]
                         ),
                ], width = 6),
                
                dbc.Col([
                   dcc.Dropdown(id = 'facility_dropdown',
                         multi = True,
                         clearable = True,
                         disabled = False,
                         placeholder = 'Select Facility',
                         value =[facility_list[0]],
                         options = [{'label': c, 'value': c} for c in facility_list]
                         ),
                ], width = 6) 
                
            ]),
            
        ])
    ], className = "mycard"),
    
    # Row with two columns    
    dbc.Row([
        
        dbc.Col([
            
            dbc.Card([
                
                dbc.CardBody([
                    
                    html.H1("Look at me, I'm a nice graph!"),
                    html.H4("We will display a graph in this space"),
                    html.Hr(),
                    
                    dcc.Graph(id = "big_graph", figure = fig, style = {'width': '95%' , 'margin': 'auto'}),
                    
                ])
                
            ], className="myothercard")
            
        ], width = 6),
       
       dbc.Col([
            
            dbc.Card([
                
                dbc.CardBody([
                    
                    html.H1("I want to configure this graph!"),
                    html.H4("We will display other controllers here."),
                    html.Hr(),
                    
                    # Range Slider: 
                    dcc.RangeSlider(0, 150, 10, value=[20, 80], id='my_range_slider'),
                    
                    # line break
                    html.Br(),
                    
                    # Input and buttons:
                    dcc.Input(id="input_start_ww", type="text", placeholder="Write a start workweek"),
                    dcc.Input(id="input_end_ww", type="text", placeholder="Write an end workweek"),
                    html.Button('Re-compute my graph!', id='submit_button', n_clicks=0),
                    
                    
                ])
                
            ], className="myothercard")
            
        ], width = 6),
       
    ]),
    
    # Footer
    html.Div([
        
        html.H2("This is the end of this application!"),
        dcc.Markdown("To learn more about dash, visit the [official documentation](https://dash.plotly.com/introduction)."),
        dcc.Markdown("For more data science/ data visualization help and consultation, contact the [MPE SDA team](https://login.microsoftonline.com/46c98d88-e344-4ed4-8496-4ed7712e255d/oauth2/authorize?client%5Fid=00000003%2D0000%2D0ff1%2Dce00%2D000000000000&response%5Fmode=form%5Fpost&response%5Ftype=code%20id%5Ftoken&resource=00000003%2D0000%2D0ff1%2Dce00%2D000000000000&scope=openid&nonce=61F2CD438E5B4DBE568BD2C4ED88336C8BB445632A41799B%2DBA77A8D3C42C28EF0BF6279249906061B0552DC207F1081144D83D2B2BB119B9&redirect%5Furi=https%3A%2F%2Fintel%2Esharepoint%2Ecom%2F%5Fforms%2Fdefault%2Easpx&state=OD0w&claims=%7B%22id%5Ftoken%22%3A%7B%22xms%5Fcc%22%3A%7B%22values%22%3A%5B%22CP1%22%5D%7D%7D%7D&wsucxt=1&cobrandid=11bd8083%2D87e0%2D41b5%2Dbb78%2D0bc43c8a8e8a&client%2Drequest%2Did=b2f576a0%2Dc0eb%2D2000%2Dcf5e%2Dd083899abfde)!"),
        html.Hr(),
        
        # Row with images:
        dbc.Row([
            
            dbc.Col([
                html.Img(src="assets/plotly.PNG", style={'width': '15%', 'border-radius':'50%'}),
                html.P("plotly"),
                ], width = 4),
            
            dbc.Col([
                html.Img(src="assets/dash.PNG", style={'width': '15%', 'border-radius':'50%'}),
                html.P("dash"),
                ], width = 4),
            
            dbc.Col([
                html.Img(src="assets/python.PNG", style={'width': '15%', 'border-radius':'50%'}),
                html.P("python"),
                ], width = 4),
            
            
        ]),
        
        # Github link:
        html.Img(src="assets/github.png", style={'width': '2%', 'border-radius': '50%'}),
        dcc.Markdown("You can find this template in [this repository](https://dash.plotly.com/introduction)."),
        
        
    ], className = "footer-container"),
    
])

# Create callbacks #

# 3. Use the button and filter start and end workweek.

@app.callback(
    Output('big_graph', 'figure'),
    Input('devrevstep_dropdown','value'),
    Input('facility_dropdown','value'),
    Input('my_range_slider','value'),
    Input('submit_button','n_clicks'),
    State('input_start_ww','value'),
    State('input_end_ww','value')
)

def update_graph(devrevstep, facility, range_slider_value, n_clicks, start_ww, end_ww):
    
    # Filter Data using devrevstep and facility
    data_filtered = data[
        (data['devrevstep'].isin(devrevstep)) & 
        (data['ppv_site'].isin(facility))]
    
    # Filter Data using radius
    data_filtered = data_filtered[
        (data_filtered['radius'] >= range_slider_value[0]) & 
        (data_filtered['radius'] <= range_slider_value[1])]
    
    # Filter by workweek:
    if n_clicks!=0:
        data_filtered = data_filtered[
            (data_filtered['workweek'] >= int(start_ww)) & 
            (data_filtered['workweek'] <= int(end_ww))]
    
    # Create Graph
    data_to_graph_filtered = pd.DataFrame(
    data_filtered[data_filtered['final_bucket_name'].isin(['THe','THc'])].groupby([
        'final_bucket_name', 's_spec'],
                 as_index=False).agg(count=('cl_incoming', 'count'))
    )
    fig_filtered = px.bar(
        data_to_graph_filtered, x="final_bucket_name", y="count",
        color='s_spec')
    
    return fig_filtered
    

# Run the app

if __name__ == '__main__':
    print("Starting our dash example ...")
    port = int(8080)
    app.run_server(debug = True, port = port)

