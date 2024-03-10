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
       # Specify the layout
    layout = {
      'title': 'Improvement Change Notes Raised per month',
      'yaxis': {'title': 'Value'},
 
    }

    start_date =anvil.server.call('get_chart_settings',1)  
    self.text_box_1.text = start_date
    line_plots, summary_records  = anvil.server.call('get_change_note_data', start_date)
    self.repeating_panel_1.items = app_tables.improvements_by_month.search(tables.order_by("ym_date", ascending=False))
    self.plot_1.data = line_plots
    self.plot_1.layout = layout
    pass
