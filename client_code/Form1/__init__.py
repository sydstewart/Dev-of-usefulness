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
   
    # Any code you write here will run before the form opens.

  # def date_picker_1_change(self, **event_args):
  #   """This method is called when the selected date changes"""
    start_date =anvil.server.call('get_chart_settings',1)  
    line_plots  = anvil.server.call('get_change_note_data', start_date)
    # self.repeating_panel_1.items = summary_records
    self.plot_1.data = line_plots
    pass
