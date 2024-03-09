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
    no_of_rows = len(changes)
    print(no_of_rows)
    Impcount = 0
    for row in changes:
       if row['classid'] == 'Improvement':
            ImpCount = 1 + Impcount
    app_tables.change_summary.add_row(ImpCount = Impcount, classid = 'Improvement')   
  #   dicts = [{'change_date': r['change_date'], 'Class': r['classid']} for r in changes]
  #   df = pd.DataFrame.from_dict(dicts)
  #   df['change_date'] = pd.to_datetime(df['change_date'], infer_datetime_format=True, utc=True )
  #   # df['change_date'] = df['local_date'].dt.tz_localize('UTC')
  #   # df["change_Date"] = pd.to_datetime(df["change_date"])
  #   # df['date'] = df['change_date'].dt.strftime('%Y/%m')
  #   print(df)
   

  #   df['Year'] = df['change_date'].dt.to_period('Y')
  #   # df['Year'] = df['Year'].astype('int')
  # # selecting rows based on condition 
  #   # df = df[df['Year'] >= 2020] 
  #   options = ['Improvement'] 
  #   df['Year_Month'] = df['change_date'].dt.to_period('M')
  #   df = df[df['Class'].isin(options)] 
  #   # df['Counts'] = 1
  #   # df.groupby(["Year_Month"].count().reset_index(name='total_count'))
  #   results = df.groupby(["Year_Month"])['Year'].count()
  
  #   print('df',results)
  #   line_plots = go.Scatter(x=results['Year_Month'], y=results['Year'], name='Improvements per month', marker=dict(color='#e50000'))
  #   return line_plots