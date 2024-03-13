from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
 

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    start_date =anvil.server.call('get_chart_settings',1)  
    self.text_box_1.text = start_date
    
  
     
    layout = {
      'title': '<b>' + self.drop_down_1.selected_value +  ' Change Notes per month </b>' ,
       
      'yaxis': {'title': 'Value'},
 
    }

    start_date =anvil.server.call('get_chart_settings',1)  
    self.text_box_1.text = start_date
    line_plots, summary_records  = anvil.server.call('get_change_note_data', start_date, self.drop_down_1.selected_value)
    self.repeating_panel_1.items = app_tables.improvements_by_month.search(tables.order_by("ym_date", ascending=False))
    if self.date_picker_1.date and self.date_picker_2.date:
         self.repeating_panel_2.items = app_tables.change_notes.search(change_date=q.between(self.date_picker_1.date, self.date_picker_2.date))
    self.plot_1.data = line_plots
    self.plot_1.layout = layout
    pass

  def stage_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    search_using_kwargs(self)
    
  def change_type_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    search_using_kwargs(self)
