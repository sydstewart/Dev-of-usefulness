import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta

def dosearch(self):
        startdate =self.date_picker_3.date
        classid = self.change_type_dropdown.selected_value
        stage = self.stage_dropdown.selected_value
        pick = self.PICK_drop_down.selected_value
        print('pick', pick)
        records_found =  anvil.server.call('get_change_note_data1',startdate, classid, stage, pick)
        if records_found > 0:
            line_plots, summary_records = anvil.server.call('get_change_note_data2',startdate, classid, stage, pick)
           
            self.plot_1.data = line_plots
            layout = {
              'title': '<b>' + str(classid)  + ' Change Notes per month '  + str(stage) + ' - Starting at ' + str(startdate) + '</b>' ,
                # + self.change_type_dropdown.selected_value 
              'yaxis': {'title': 'Value'},
            }
            self.plot_1.layout = layout                                                                
            self.repeating_panel_1.items = summary_records
        # else:
        #       alert('No Date Found')