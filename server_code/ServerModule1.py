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
    df["change_Date"] = pd.to_datetime(df["change_date"])
    # df['date'] = df['change_date'].dt.strftime('%Y/%m')
    print(df)
   # line_plots = go.Scatter(x=df['Date_entered'], y=df['delta_work'], name='Delta Work Completed', marker=dict(color='#e50000'))
    # df.index = pd.to_datetime(change_date.df_cdc.index, utc=True)
    # df1["Change_Date"] = pd.to_datetime(df["change_date"])
    # print(df1)
    df['year'] = df['change_date'].str[1:7]
    # df['change_date'] = pd.to_datetime(df['change_date'])
    # # df['Year'] = df['change_date'].dt.to_period('Y')
    # # df['date'] = pd.to_datetime(df['change_date'])
    # # df['year'], df['month'] = df['date'].dt.year, df['date'].dt.month
    # # df['yyyy'] = pd.to_datetime(df['change_date']).dt.year (utc=True)
    # # # df['mm'] = pd.to_datetime(df['change_date']).dt.month
      
    # df = df.groupby('Class').count()
    print('df',df)