import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, time , date , timedelta


@anvil.server.callable
def get_change_note_data(start_date):
    #read in 10000 rows of data 
    print('Syd')
    import pandas as pd
    import numpy as np

    data = [
        {'group_name': 'GROUP 1', 'client': 'CLIENT 1', 'messages': 100, 'supplier': 'SUP 1', 'blocked': 0}, 
        {'group_name': 'GROUP 2', 'client': 'CLIENT 1', 'messages': 200, 'supplier': 'SUP 1', 'blocked': 27}, 
        {'group_name': 'GROUP 3', 'client': 'CLIENT 1', 'messages': 300, 'supplier': 'SUP 1', 'blocked': 0}, 
        {'group_name': 'GROUP 1', 'client': 'CLIENT 2', 'messages': 400, 'supplier': 'SUP 1', 'blocked': 4}, 
        {'group_name': 'GROUP 2', 'client': 'CLIENT 2', 'messages': 500, 'supplier': 'SUP 1', 'blocked': 0}, 
        {'group_name': 'GROUP 4', 'client': 'CLIENT 3', 'messages': 600, 'supplier': 'SUP 1', 'blocked': 9}, 
    ] 
    
    df = pd.DataFrame(data)
    grouped = df.groupby(['client','supplier'])
    print(grouped)
    res = grouped[['messages','blocked']].agg(np.sum)
    res['index'] = range(len(res))
    res = res.reset_index()
    res.to_dict('records')
    print(res)
    
  
    changes = app_tables.change_notes.search(change_date = q.greater_than(start_date))
    no_of_rows = len(changes)
    dicts = [{'change_date': r['change_date'], 'Class': r['classid']}
         for r in changes]
    df1 = pd.DataFrame.from_dict(dicts)
    df1['change_date'] = pd.to_datetime(df1['change_date'], infer_datetime_format=True, utc=True )
    # df1['Year_Month'] = df1['change_date'].dt.to_period('M')
    df1['year'] = df1['change_date'].dt.year
    df1['month'] = df1['change_date'].dt.month
    df1['YM'] = df1['year'].astype(str) + "-" + df1['month'].astype(str)
    print(df1['YM'])
    df1['Counts'] = 1
    df1[df1['year'] >= 2020]
  
    print(df1)
    grouped = df1.groupby(['YM'])
    print(grouped)
    res = grouped[['Counts']].agg(np.sum)
    res['index'] = range(len(res))
    res = res.reset_index()
    
    line_plots = go.Scatter(x=res['YM'] , y=res['Counts'], name='Improvements per month', marker=dict(color='#e50000'))
  
    print(line_plots)
    # res.to_dict('records')
    # print(res)
    # line_plots = go.Scatter(x=res['Year_Month'] , y=res['Counts'], name='Improvements per month', marker=dict(color='#e50000'))
    return line_plots
# df = pandas.DataFrame.from_dict(dicts)
  #   Impcount = 0
  #   # for row in changes:
  #   #   if (row['classid']) == 'Improvement':
  #   #        ImpCount = 1 + Impcount
  #   # print(ImpCount)
  #   # app_tables.change_summary.add_row(ImpCount = Impcount, classid = 'Improvement')   
  #   dicts = [{'change_date': r['change_date'], 'Class': r['classid']} for r in changes]
  #   df = pd.DataFrame.from_dict(dicts)
  #   df['change_date'] = pd.to_datetime(df['change_date'], infer_datetime_format=True, utc=True )
  #   df['Counts'] = 1
  # # # selecting rows based on condition 
  #   options = ['Improvement'] 
  #   df['Year_Month'] = df['change_date'].dt.to_period('M')
  #   df = df[df['Class'].isin(options)] 
  # #   # df['Counts'] = 1
  #   # df.groupby["Year_Month"].count()
  # #   results = df.groupby(["Year_Month"])['Year'].count()
  #   df.groupby('Year_Month').agg({'Counts': ['sum']})
  
  #   # print('df',df)
  #   xlist = df['Year_Month'].tolist()
  #   ylist = df['Counts'].tolist()

  #   print(xlist)
  #   print(ylist)
  #   line_plots = go.Scatter(x=xlist, y=ylist, name='Improvements per month', marker=dict(color='#e50000'))
  #   # return line_plots