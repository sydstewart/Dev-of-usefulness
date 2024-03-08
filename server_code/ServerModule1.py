import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd


@anvil.server.callable
def get_change_note_data():
    #read in 10000 rows of data 
    data = app_tables.change_notes.search()
    df = pd.DataFrame(data)
    
    #print the first 5 rows of the dataframe
    print(df.head())