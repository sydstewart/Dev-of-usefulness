import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import plotly.graph_objects as go

@anvil.server.callable
def get_change_note_data():
    #read in 10000 rows of data 
    print('Syd')
    changes = app_tables.change_notes.search()
    # df = pd.DataFrame.from_dict(dicts)
    # # for column_headers in df.columns: 
    # #     print(column_headers)
    # # dfimprove = df.groupby(['classid']).count()
    # # print(dfimprove)
    # # #print the first 5 rows of the dataframe
    # print(df.head())

   # chart_data = app_tables.completed_work.search()
   dicts = [{'change_date': r['change_date'], 'Class': r['classid']} for r in changes]
   df = pd.DataFrame.from_dict(dicts)
   print('df',df)
   line_plots = go.Scatter(x=df['Date_entered'], y=df['delta_work'], name='Delta Work Completed', marker=dict(color='#e50000'))