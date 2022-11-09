import pandas as pd
import plotly.express as px

def get_graph(data_filtered):
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