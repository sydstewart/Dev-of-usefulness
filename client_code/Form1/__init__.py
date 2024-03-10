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

  def date_picker_1_change(self, **event_args):
    """This method is called when the selected date changes"""
    t = app_tables.chart_definition.seaarch(Chart_no = 1)
    self.date_picker_1.date = t['start_date']
    start_date = self.date_picker_1.date
    line_plots = anvil.server.call('get_change_note_data', start_date)
    self.plot_1.data = line_plots
    pass
