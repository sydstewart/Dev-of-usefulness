import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, time , date , timedelta


@anvil.server.callable
def get_change_note_data():
    #read in 10000 rows of data 
    print('Syd')
    changes = app_tables.change_notes.search()
  
    dicts = [{'change_date': r['change_date'], 'Class': r['classid']} for r in changes]
    df = pd.DataFrame.from_dict(dicts)
  
   # line_plots = go.Scatter(x=df['Date_entered'], y=df['delta_work'], name='Delta Work Completed', marker=dict(color='#e50000'))
    df['ym-date'] = df['change_date'].dt.strftime('%Y-%m')
    df = df.groupby('Class','month_year').count()
    print('df',df)