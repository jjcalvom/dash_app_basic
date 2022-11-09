import pandas as pd
import plotly.express as px

data = pd.read_csv("./data/data_example.csv")
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