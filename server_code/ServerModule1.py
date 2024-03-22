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
def get_change_note_data1(startdate, classid, stage, pick):

    search1 = stage
   
    search2 = classid
       
    search3 = startdate
    print('pick1',pick)
    search4 = pick
   
  # =========================================================================
  # Setup search dictionary
    kwargs ={}
  
#Stage
    if search1 == 'Released':
        kwargs['stage'] = 'Released'

#Type of change
    if search2:
         kwargs['classid'] = search2

    if search3:
        date = startdate
        year = int(date.strftime('%Y'))
        month = int(date.strftime('%m'))
        day = int(date.strftime('%d'))
        start = datetime(year, month, day)
        print('Start Date=',start)
        kwargs['change_date']=q.greater_than_or_equal_to(start)
      
    if search4:
        kwargs['pick'] = search4

    
  
    changes = app_tables.change_notes.search(**kwargs)

    return  len(changes) 












@anvil.server.callable
def get_change_note_data2(startdate, classid, stage, pick):
    search1 = stage
   
    search2 = classid
       
    search3 = startdate
    print('pick1',pick)
    search4 = pick
   
  # =========================================================================
  # Setup search dictionary
    kwargs ={}
  
#Stage
    if search1 == 'Released':
        kwargs['stage'] = 'Released'

#Type of change
    if search2:
         kwargs['classid'] = search2

    if search3:
        date = startdate
        year = int(date.strftime('%Y'))
        month = int(date.strftime('%m'))
        day = int(date.strftime('%d'))
        start = datetime(year, month, day)
        print('Start Date=',start)
        kwargs['change_date']=q.greater_than_or_equal_to(start)
      
    if search4:
        kwargs['pick'] = search4

    
  
    changes = app_tables.change_notes.search(**kwargs)
    if len(changes) > 0:
        no_of_rows = len(changes)
        print('No of Rows', no_of_rows)
        dicts = [{'change_date': r['change_date'], 'Class': r['classid']}
            for r in changes]
        print('dicts',len(dicts))
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
        print('Sta Daate', res['ym-date'].min())
        print('End Date', res['ym-date'].max())
      # Fill in Missing months with zero change Notes =========================================================
        today = date.today()
        startdate = datetime.now() + timedelta(days=-300)
        d1 = today.strftime("%Y-%m-%d")
        
        print('d1',d1)
        res["ym-date"] = pd.to_datetime(res["ym-date"]) 
        
        all_dates = pd.DataFrame({"ym-date":pd.date_range(start=res['ym-date'].min(),end=res['ym-date'].max(),freq="MS")})
        print('all dates', all_dates)
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
        print('summary_records', summary_records)
        # app_tables.improvements_by_month.delete_all_rows()
        # for row in summary_records:
        #   app_tables.improvements_by_month.add_row(ym_date =row['ym-date'], Counts= row['Counts']) 
        # print('summary_records', summary_records)
    
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
    return

#========================================PIES++++++++++++++++++++++++++++++++++++++++

@anvil.server.callable
def get_change_note_data_pies(startdate, classid, stage, pick):
    search1 = stage
   
    search2 = classid
       
    search3 = startdate
    print('pick1',pick)
    search4 = pick
   
  # =========================================================================
  # Setup search dictionary
    kwargs ={}
  
#Stage
    if search1 == 'Released':
        kwargs['stage'] = 'Released'

#Type of change
    if search2:
         kwargs['classid'] = search2

    if search3:
        date = startdate
        year = int(date.strftime('%Y'))
        month = int(date.strftime('%m'))
        day = int(date.strftime('%d'))
        start = datetime(year, month, day)
        print('Start Date=',start)
        kwargs['change_date']=q.greater_than_or_equal_to(start)
      
    if search4:
        kwargs['pick'] = search4

    
  
    changes = app_tables.change_notes.search(**kwargs)
    if len(changes) > 0:
        no_of_rows = len(changes)
        print('No of Rows', no_of_rows)
        dicts = [{'change_date': r['change_date'], 'Class': r['classid']}
            for r in changes]
        print('dicts',len(dicts))
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
      
        print('df1',df1)
        grouped = df1.groupby(['Class'])
        print('grouped',grouped)
            
        res = grouped[['Counts']].agg(np.sum)
        res['index'] = range(len(res))
        res = res.reset_index()
        print('res for pies', res)
      #   print('Sta Daate', res['ym-date'].min())
      #   print('End Date', res['ym-date'].max())
      # # Fill in Missing months with zero change Notes =========================================================
      #   today = date.today()
      #   startdate = datetime.now() + timedelta(days=-300)
      #   d1 = today.strftime("%Y-%m-%d")
        
      #   print('d1',d1)
      #   res["ym-date"] = pd.to_datetime(res["ym-date"]) 
        
      #   # all_dates = pd.DataFrame({"ym-date":pd.date_range(start=res['ym-date'].min(),end=res['ym-date'].max(),freq="MS")})
      #   # print('all dates', all_dates)
      #   # res = pd.merge(all_dates, res, how="left", on='ym-date').fillna(0)
    
      # # =====Calculate Range and Range Mean =========================================================
      #   res['mean'] = res['Counts'].mean()
        
      #   Mean = res['Counts'].mean()
      #   sqmean = math.sqrt(Mean)
      #   res['sqmean']= sqmean
      #   res['Range']=abs(res['Counts'] -res['Counts'].shift(1))
      #   res['Range'].dropna()
      #   print('Ranges', res['Range'])
      #   res['rangemean']  = res['Range'].mean()
      #   RangeMean =  res['Range'].mean() 
      #   print('rangemean=', res['Range'].mean())
        
      #   res['median'] = res['Range'].median()
      #   RangeMedian= res['Range'].median()
      #   print('median of Range=', RangeMedian)
      
      # #== Calcuate UCLs ========================================================
      #   UCLMedian = (RangeMedian  * 3.14) + Mean
      #   print(' UCL using Range Median =', UCLMedian)
      #   UCLMean = RangeMean *2.66 + Mean
      #   print(' UCL using Range Mean =', UCLMean)
      #   UCLcChart = (math.sqrt(Mean) * 3) + Mean
      
      #====== prepare records for display in form =======        
        summary_records ={}
        summary_records = res.to_dict(orient="records")
        print('summary_records', summary_records)
        # app_tables.improvements_by_month.delete_all_rows()
        # for row in summary_records:
        #   app_tables.improvements_by_month.add_row(ym_date =row['ym-date'], Counts= row['Counts']) 
        # print('summary_records', summary_records)
    
      #==== prepare Chart +++++++++++++++++++++++++++++++++++++++++++++++
        pie_plots = [
          
          go.Pie(res, values=res['Counts'] , names =res['Class']),
                    ]
          # # go.Scatter(x=res['ym-date'], y=res['mean'],  name='Mean of Changes per month ='  + str(round(Mean,1))),
    
          # # go.Scatter(x=res['ym-date'], 
          # #           y=(res['rangemean'] * 2.66) + res['mean'], 
          # #           name='UCL based on range mean = ' + str(round(UCLMean,1))),
    
          # # go.Scatter(x=res['ym-date'], 
          # #           y=(res['median'] * 3.14) + res['mean'], 
          # #           name='UCL based on range median  =' + str(round(UCLMedian,1)) ),
          
          # go.Scatter(x=res['ym-date'], 
          #           y= ((res['sqmean'])) * 3 + res['mean'], 
          #           name='UCL based on c-Chart  =' + str(round(UCLcChart,1)) )
                    
          #           ]
      
        print(pie_plots)
    # ============returns==================================
        return pie_plots, summary_records
    return
