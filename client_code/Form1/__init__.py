from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta 

# from ..Searches_using_kwargs import search_using_kwargs
from ..dosearch import dosearch

class Form1(Form1Template):
  def __init__(self, **properties):
# Set Form properties and Data Bindings.
    self.init_components(**properties)
    # start_date =anvil.server.call('get_chart_settings',1)  
    system_type = app_tables.system_type.get(System='Test')
    
    self.date_picker_3.date = '2020-01-01'
    self.change_type_dropdown.selected_value ='Improvement'
    self.stage_dropdown.selected_value = 'Created'
    dosearch(self)

  def stage_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    dosearch(self)
    
  def change_type_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    dosearch(self)

  def date_picker_3_change(self, **event_args):
      """This method is called when the selected date changes"""
      dosearch(self)
   
     
   

