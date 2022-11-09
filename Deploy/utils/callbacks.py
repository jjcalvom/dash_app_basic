# Import libraries/extensions for callbacks
from dash.dependencies import Input, Output, State
from utils import data, functions

def connect_callbacks(app):
    
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
        data_filtered = data.data[
            (data.data['devrevstep'].isin(devrevstep)) & 
            (data.data['ppv_site'].isin(facility))]
        
        # Filter Data using radius
        data_filtered = data_filtered[
            (data_filtered['radius'] >= range_slider_value[0]) & 
            (data_filtered['radius'] <= range_slider_value[1])]
        
        # Filter by workweek:
        if n_clicks!=0:
            data_filtered = data_filtered[
                (data_filtered['workweek'] >= int(start_ww)) & 
                (data_filtered['workweek'] <= int(end_ww))]
        
        fig_filtered = functions.get_graph(data_filtered)
        
        return fig_filtered