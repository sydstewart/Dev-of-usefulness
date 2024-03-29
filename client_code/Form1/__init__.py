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
    if system_type:
       self.system_type_label.text = 'Test'
    self.date_picker_3.date = '2020-01-01'
    self.change_type_dropdown.selected_value ='Improvement'
    self.stage_dropdown.selected_value = 'Created'
    self.PICK_drop_down.selected_value = None
    self.run_chart_radio_button.selected
    
    dosearch(self)

  def stage_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    records = dosearch(self)
    
    
  def change_type_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    dosearch(self)

  def date_picker_3_change(self, **event_args):
      """This method is called when the selected date changes"""
      dosearch(self)

  def PICK_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    dosearch(self)
    pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    pass
   
     
   

