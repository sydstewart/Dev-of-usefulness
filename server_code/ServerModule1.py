import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, time , date , timedelta
import math

@anvil.server.callable
def get_chart_settings(chartno):        
    t = app_tables.chart_definition.get(chart_no = chartno)
    title =  t['title']
    start_date =t['start_date']
    return start_date


@anvil.server.callable
def get_change_note_data(**kwargs):
    #read in 10000 rows of data 
    # print('Syd')
    # import pandas as pd
    # import numpy as np
    # print('classid', classid)
    # data = [
    #     {'group_name': 'GROUP 1', 'client': 'CLIENT 1', 'messages': 100, 'supplier': 'SUP 1', 'blocked': 0}, 
    #     {'group_name': 'GROUP 2', 'client': 'CLIENT 1', 'messages': 200, 'supplier': 'SUP 1', 'blocked': 27}, 
    #     {'group_name': 'GROUP 3', 'client': 'CLIENT 1', 'messages': 300, 'supplier': 'SUP 1', 'blocked': 0}, 
    #     {'group_name': 'GROUP 1', 'client': 'CLIENT 2', 'messages': 400, 'supplier': 'SUP 1', 'blocked': 4}, 
    #     {'group_name': 'GROUP 2', 'client': 'CLIENT 2', 'messages': 500, 'supplier': 'SUP 1', 'blocked': 0}, 
    #     {'group_name': 'GROUP 4', 'client': 'CLIENT 3', 'messages': 600, 'supplier': 'SUP 1', 'blocked': 9}, 
    # ] 
    
    # df = pd.DataFrame(data)
    # grouped = df.groupby(['client','supplier'])
    # print(grouped)
    # res = grouped[['messages','blocked']].agg(np.sum)
    # res['index'] = range(len(res))
    # res = res.reset_index()
    # res.to_dict('records')
    # print(res)
    
  
    changes = app_tables.change_notes.search( tables.order_by("change_date", ascending=False),**kwargs)
    no_of_rows = len(changes)
    dicts = [{'change_date': r['change_date'], 'Class': r['classid']}
        for r in changes]
    df1 = pd.DataFrame.from_dict(dicts)
    df1['change_date'] = pd.to_datetime(df1['change_date'], infer_datetime_format=True, utc=True )
    df1['ym-date'] = df1['change_date'].dt.strftime('%Y-%m')
    print(df1['ym-date'])
    # df1['Year_Month'] = df1['change_date'].dt.to_period('M')
    df1['year'] = df1['change_date'].dt.year
    df1['month'] = df1['change_date'].dt.month
    df1['YM'] = df1['year'].astype(str) + "-" + '0'+ df1['month'].astype(str)
    df1 = df1.fillna(0)
    print(df1['YM'])
    df1['Counts'] = 1
    
    # df1.sort_values(by=['YM'])
  
    print(df1)
    grouped = df1.groupby(['ym-date'])
    print(grouped)
        
    res = grouped[['Counts']].agg(np.sum)
    res['index'] = range(len(res))
    res = res.reset_index()
    
  # Fill in Missing months with zero change Notes =========================================================
    today = date.today()
    d1 = today.strftime("%Y-%m")
    
    res["ym-date"] = pd.to_datetime(res["ym-date"]) 
    
    all_dates = pd.DataFrame({"ym-date":pd.date_range(start=res['ym-date'].min(),end=res['ym-date'].max(),freq="MS")})
    
    res = pd.merge(all_dates, res, how="left", on='ym-date').fillna(0)

  # =====Calculate Range and Range Mean =========================================================
    res['mean'] = res['Counts'].mean()
    
    Mean = res['Counts'].mean()
    sqmean = math.sqrt(Mean)
    res['sqmean']= sqmean
    res['Range']=abs(res['Counts'] -res['Counts'].shift(1))
    res['Range'].dropna()
    print('Ranges', res['Range'])
    res['rangemean']  = res['Range'].mean()
    RangeMean =  res['Range'].mean() 
    print('rangemean=', res['Range'].mean())
    
    res['median'] = res['Range'].median()
    RangeMedian= res['Range'].median()
    print('median of Range=', RangeMedian)
  
  #== Calcuate UCLs ========================================================
    UCLMedian = (RangeMedian  * 3.14) + Mean
    print(' UCL using Range Median =', UCLMedian)
    UCLMean = RangeMean *2.66 + Mean
    print(' UCL using Range Mean =', UCLMean)
    UCLcChart = (math.sqrt(Mean) * 3) + Mean
  
  #====== prepare records for display in form =======        
    summary_records ={}
    summary_records = res.to_dict(orient="records")
    app_tables.improvements_by_month.delete_all_rows()
    for row in summary_records:
      app_tables.improvements_by_month.add_row(ym_date =row['ym-date'], Counts= row['Counts']) 
    print('summary_records', summary_records)

  #==== prepare Chart +++++++++++++++++++++++++++++++++++++++++++++++
    line_plots = [
      
      go.Scatter(x=res['ym-date'] , y=res['Counts'],mode='lines+markers', name='Changes per month', marker=dict(color='#e50000')),
    
      go.Scatter(x=res['ym-date'], y=res['mean'],  name='Mean of Changes per month ='  + str(round(Mean,1))),

      # go.Scatter(x=res['ym-date'], 
      #           y=(res['rangemean'] * 2.66) + res['mean'], 
      #           name='UCL based on range mean = ' + str(round(UCLMean,1))),

      # go.Scatter(x=res['ym-date'], 
      #           y=(res['median'] * 3.14) + res['mean'], 
      #           name='UCL based on range median  =' + str(round(UCLMedian,1)) ),
      
      go.Scatter(x=res['ym-date'], 
                y= ((res['sqmean'])) * 3 + res['mean'], 
                name='UCL based on c-Chart  =' + str(round(UCLcChart,1)) )
                
                ]
  
    print(line_plots)
  # ============returns==================================
    return line_plots, summary_records





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