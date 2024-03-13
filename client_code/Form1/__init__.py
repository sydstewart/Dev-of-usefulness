from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Searches_using_kwargs import search_using_kwargs

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    start_date =anvil.server.call('get_chart_settings',1)  
    self.startdate_textbox.text = start_date
    
  
     
    layout = {
      'title': '<b>'  ' Change Notes per month </b>' ,
        # + self.change_type_dropdown.selected_value 
      'yaxis': {'title': 'Value'},
 
    }

    start_date =anvil.server.call('get_chart_settings',1)  
    self.startdate_textbox.text = start_date
    

  def stage_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    search_using_kwargs(self)
    
  def change_type_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    search_using_kwargs(self)

  def startdate_textbox_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    search_using_kwargs(self)
