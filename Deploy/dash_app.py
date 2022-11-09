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
import dash_bootstrap_components as dbc
from utils import layouts, callbacks


# Create a dash object
# Use external stylesheets from Bootstrap if you want to use bootstrap css style.
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(external_stylesheets=external_stylesheets)

# Connect to layout

app.layout = layouts.app_layout 

# Connect to callbacks
callbacks.connect_callbacks(app)

# Run the app

if __name__ == '__main__':
    print("Starting our dash example ...")
    port = int(8080)
    app.run_server(debug = True, port = port)

