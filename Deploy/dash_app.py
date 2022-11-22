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
import time
import flask
import dash_bootstrap_components as dbc
from utils import layouts, callbacks

# Create a dash object
# Use external stylesheets from Bootstrap if you want to use bootstrap css style.
external_stylesheets = [dbc.themes.BOOTSTRAP]

class myApp(dash.Dash):
    def __init__(self, **kwargs):
        self.start = time.perf_counter()
        print("Super!")
        super().__init__(__name__, **kwargs)
        
server = flask.Flask(__name__)
server.secret_key = 'd001d46f42b16aed2c6s635305f0f9b9'  # Hardcode so shared between instances and cookies not reset
app = myApp(server = server, external_stylesheets = external_stylesheets)

@app.server.route('/')
def serve_layout():
    return layouts.app_layout 

print('Creating layout')
app.layout = serve_layout

# Connect to callbacks
callbacks.connect_callbacks(app)

# Run the app

if __name__ == '__main__':
    print("Starting our dash example ...")
    port = int(8080)
    app.run_server(debug = False, host="0.0.0.0", port = port, ssl_context = 'adhoc')

