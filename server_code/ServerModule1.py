import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd


@anvil.server.callable
def get_change_note_data():
    #read in 10000 rows of data 
    print('Syd')
    dicts = app_tables.change_notes.search(classid ='Improvement')
    df = pd.DataFrame.from_dict(dicts)
    for column_headers in df.columns: 
        print(column_headers)
    # dfimprove = df.groupby(['classid']).count()
    # print(dfimprove)
    # #print the first 5 rows of the dataframe
    # print(df.head())