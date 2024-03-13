import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta
# from ..Searches.using_kwargs import search_using_kwargs


def search_using_kwargs(self):
# Search definitions ========================================================================================================      
    search1 = self.stage_dropdown.selected_value 
   
    search2 = self.change_type_dropdown.selected_value 
    print(search2)

  
    search3 = self.date_picker_3.datetime
  # =========================================================================
  # Setup search dictionary
    kwargs ={}
  
#Stage
    if search1:
               
        kwargs['stage'] = search1
  
#Type of change
    if search2:
        kwargs['classid'] =  search2   

    if search3:
        kwargs['change_date'] = q.greater_than(search3) 

# Search using kwargs =================================================     
    print('kwargs=',kwargs)
    layout = {
      'title': '<b>'  ' Change Notes per month </b>' ,
        # + self.change_type_dropdown.selected_value 
      'yaxis': {'title': 'Value'},
 
    }
    line_plots, summary_records  = anvil.server.call('get_change_note_data', **kwargs)
    self.repeating_panel_2.items = summary_records
    if self.date_picker_1.date and self.date_picker_2.date:
         self.repeating_panel_2.items = app_tables.change_notes.search(change_date=q.between(self.date_picker_1.date, self.date_picker_2.date))
    self.plot_1.data = line_plots
    self.plot_1.layout = layout
    pass










  
#     search3 = self.search_class_drop_down.selected_value #class
#     print(search3)
#     search4 = self.search_function_drop_down.selected_value #function
#     print(search4)
#     search5 = self.search_product_area_drop_down.selected_value  #product area
#     print(search5)
#  #search6 defined in code below
#     search7 = self.id_search_textbox.text
#     # date range fields  
#     search8 = self.start_date_picker.date
#     search9 = self.end_date_picker.date
#     search10 = self.search_creator_dropdown.selected_value
#     search11 = self.over_due_chkbox.checked
#     search12 = self.priority_search_dropdown.selected_value
#     search14 = self.search_investigator_dropdown.selected_value
#     # search15 = self.text_search_textbox.text
#  #============================================================================================================
# #search6 defined
#     if self.date_search_dropdown.selected_value ==  'This week':
#         day = datetime.today()
#         print('ToDay=',day)
# #         start= day - timedelta(days=4)
# #         dt = datetime.strptime(day, '%d/%b/%Y')
#         dt = datetime.now()
#         print('Datetime is:', dt)
        
#         # get day of week as an integer
#         x = dt.weekday()
#         start = datetime.now() + timedelta(days=-x)
#         print('Start of Week=',start)
#         search6 = q.greater_than_or_equal_to(start)
#     elif self.date_search_dropdown.selected_value is None:
#         search6 = None
#     elif self.date_search_dropdown.selected_value ==  'Today':
       
#         start = datetime.now() + timedelta(days=0)
#         start = start.replace(hour=0)
#         start = start.replace(minute =0)
#         start =start.replace(second = 0)
#         print('Today=',start)
#         search6 = q.greater_than(start)
#     elif self.date_search_dropdown.selected_value ==  'Last week':
#         dt = datetime.now()
#         x = dt.weekday()
#         end = datetime.now() + timedelta(days=-(x+1))
#         start = datetime.now() + timedelta(days=-(x+8))
#         print('Start of Last Week=',start)
#         print('end of last week=',end)
#         search6 = q.between(start, end)
#     elif self.date_search_dropdown.selected_value ==  'Last 90 Days':
#         dt = datetime.now()
#         print('Last 90 Days  Date Now=',dt)
#         x = dt.weekday()
#         end = datetime.now() + timedelta(days=0)
#         start = datetime.now() + timedelta(days=-90)
#         print('Start of 90 days=',start)
#         print('end of 90 daysk=',end)
#         search6 = q.between(start, end)
#     elif self.date_search_dropdown.selected_value ==  'This Month':
#         dt = datetime.now()
#         x = dt.weekday()
#         this_month = dt.month
#         start = dt.replace(day=1)
#         end = datetime.now() + timedelta(days=0)
        
#         print('Start of 90 days=',start)
#         print('end of 90 daysk=',end)
#         search6 = q.between(start, end)
#     elif self.date_search_dropdown.selected_value ==  'Last Month':
#         dt = datetime.now()
               
#         this_month = dt.month
#         if this_month == 1:
#              last_month = 12
#              year =dt.year -1
#         else:
#             last_month = dt.month -1
#             year = dt.year
             
#             start = datetime(year, last_month, day = 1, hour = 0)
#             end = datetime(year, last_month, calendar.monthrange(dt.year, last_month)[-1])
#             search6 = q.between(start, end)
#     elif self.date_search_dropdown.selected_value ==  'This Month':
#             dt = datetime.now()
#             x = dt.weekday()
#             this_month = dt.month
#             start = dt.replace(day=1)
#             end = datetime.now() + timedelta(days=0)
            
#             print('Start of 90 days=',start)
#             print('end of 90 daysk=',end)
#             search6 = q.between(start, end)
      
#     elif self.date_search_dropdown.selected_value ==  'Last Year':
#         dt = datetime.now()
               
#         last_year = dt.year - 1
#         print('last_year=', last_year)
 
#         start = datetime(year =last_year, month = 1, day =1, hour =0)
#         print('start=' ,start)

#         end = datetime(year =dt.year, month = 1, day =1, hour = 0)
#         print('end=' ,end)
      
#         search6 = q.between(start, end)
#     elif self.date_search_dropdown.selected_value ==  'This Year':
#         dt = datetime.now()
               
#         last_year = dt.year - 1
#         print('last_year=', last_year)
 
#         start = datetime(year =dt.year, month = 1, day =1, hour =0)
#         print('start=' ,start)

#         end = datetime.now()
#         print('end=' ,end)
      
#         search6 = q.between(start, end)
      
      
#     else: #last month
#             last_month = this_month -1
#             print('last Month=',last_month)
#             start = dt.replace(day=1)
#             start = dt.replace(month = last_month)
#             start= datetime(dt.year, dt.month -1 , 1)
#             end = datetime(dt.year, dt.month -1 , calendar.monthrange(dt.year, dt.month -1)[-1])
#             print('last Month end date=',end)
#             print('Start of Last Month=',start)
#             print('end of Last  Month=',end)
#             search6 = q.between(start, end)

    
# # Setup search dictionary
#     kwargs ={}

   
# #Stage
#     if search1:
#         kwargs['stage'] = search1
  
# #Type
#     if search2:
#         kwargs['type'] =  search2   

# # Class
#     if search3:       
#        kwargs['classid'] = search3
      
# # Function
#     if search4:
#         kwargs['function'] = search4

# #Product Area
#     if search5:
#         kwargs['product_area'] = search5
# #date search
#     if search6:
#         kwargs['change_date'] = search6

# # id search
#     if search7:
#        kwargs['change_note_id'] = q.like('%' + search7 + '%')

# # date range search
#     if search8 and not search9:
#         self.date_search_dropdown.selected_value = None
#         # print('day=', date(search8.day))
#         date = self.start_date_picker.date
#         year = int(date.strftime('%Y'))
#         month = int(date.strftime('%m'))
#         day = int(date.strftime('%d'))
#         # hour = int(self.start_date_picker.selected_value[:2])
#         # minutes = int(self.start_date_picker.selected_value[-2:])
#         start = datetime(year, month, day)
#         print('Start Date=',start)
#         kwargs['change_date'] = q.greater_than_or_equal_to(start)  
   
#     if search9 and search8:
#         print('search8 and search9')
#         self.date_search_dropdown.selected_value = None
      
#         date = self.start_date_picker.date
#         year = int(date.strftime('%Y'))
#         month = int(date.strftime('%m'))
#         day = int(date.strftime('%d'))
#         start = datetime(year, month, day)
#         print('Start Date=',start)
  
#         endate = self.end_date_picker.date
#         endyear = int(endate.strftime('%Y'))
#         endmonth = int(endate.strftime('%m'))
#         endday = int(endate.strftime('%d'))
#         end = datetime(endyear,endmonth, endday)
#         print('End Date=',end)
#         kwargs['change_date']= q.between(start,end)
# # # Creator
#     if search10:
#        kwargs['user']= search10
# # Investigator
#     if search14:
#         kwargs['investigator']= search14
      
# # over_due_chkbox.checked ( removed)
#     if search11 == True:
#           kwargs['due_date'] =  q.less_than_or_equal_to(datetime.today())
#           kwargs['stage'] = q.none_of('Released', 'Reviewed', 'Archive','Rejected')
# # Priority     
#     if search12:
#           kwargs['priority'] = search12

#     # if search15: #r['title'].lower() or query in r['description'].lower()]
#     #   kwargs['title'] = search15
       
# # Search using kwargs      
#     print('kwargs=',kwargs)
#     results = anvil.server.call('get_results', kwargs)
#     # results= app_tables.change_notes.search(tables.order_by('change_date', ascending = False),**kwargs)
#     # results = app_tables.change_notes.search(q.any_of(**kwargs)) 
#     print('results', results)
#     self.repeating_panel_1.items = results
#     self.hits_textbox.text  = len(results)
