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
      'title': '<b>Improvement Change Notes Released per month</b> ',
       
      'yaxis': {'title': 'Value'},
 
    }

    start_date =anvil.server.call('get_chart_settings',1)  
    self.text_box_1.text = start_date
    line_plots  = anvil.server.call('get_change_note_data', start_date) #, self.end_date_picker.date, self.class_dropdown.selected_value, self.stage_dropdown.selected_value)
    
    self.repeating_panel_1.items = app_tables.improvements_by_month.search(tables.order_by("ym_date", ascending=False))
    self.date_picker_1.date
    self.plot_1.data = line_plots
    self.plot_1.layout = layout
    pass
   
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.date_picker_1.date and self.date_picker_2.date:
        self.repeating_panel_2.items = app_tables.change_notes.search(q.all_of(
                                                                      change_date=q.between(
                                                                      self.date_picker_1.date,self.date_picker_2.date),
                                                                      classid ='Improvement' , 
                                                                      stage ='Released') )    
        self.text_box_2.text = len(self.repeating_panel_2.items)

 