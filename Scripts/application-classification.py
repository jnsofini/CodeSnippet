"""
There are about 1500 applications, each with about 200+ columns. We want to search which data has medical
related data. This was achieved via a simple word search. Bellow are simple functions to perform these task
and then add a column to tbe data called area.
"""

import pandas as pd
import pickle
import csv

data_path = "data.xlsx"

#print(os.path.split(data_path))

def load_data(path, sheet=None):
    """Loads data from a multisheet excel fil

    Args:
        path (file): the excel file containing the data
        sheet (excel sheet), optional): The specific excel sheet to load. Defaults to None.

    Returns:
        data: pandas dataframe
    """
    if sheet:
        xls = pd.ExcelFile(data)
        data = pd.read_excel(xls, sheet)
    else:
        data = pd.read_excel(data)
        
    #first two columns are system hash, so we remove them
    return data #[data.columns[3:]]


data = load_data(data_path, sheet="Application Advanced Find View")

#print(data.columns)
#columns to select from data
selected_col = ['Reference Number', 'Detailed Project Description', 'Applicant Business Overview',
       'Nature Of Organization', 'Recommendation Details', 'NAICS', 'Area']

selected_data = data[selected_col]

search_words = set(
    'clinic', 'clinical', 'drug', 'health office', 'hospital', 
    'medical', 'medical office', 'medical offices', 'medicals', 
    'medicine')

def get_medical(df, words=None):
    """Gets dataframe of data containing specific words

    Args:
        df (dataframe): application data
        words (words to searc, optional): Set of words to search for. Defaults to None.

    Returns:
        datafeame: selected data
    """
    return df[df['Applicant Business Overview'].str.contains('|'.join(search_words), na=False)]

#Strorage: Prickle file and then reload it. I use this when I want to regular save a file

def storeData(db, storage='test_store'): 
    """Stores the data in a dump

    Args:
        data (dict): dict with key, alue pair representing id num and tag
    """

    # Its important to use binary mode 
    dbfile = open(f'{storage}.pkl', 'ab') 
      
    # source, destination 
    pickle.dump(db, dbfile)                      
    dbfile.close() 
  
def loadData(storage='test_store'): 
    # for reading also binary mode is important 
    dbfile = open(f'{storage}.pkl', 'rb')      
    db = pickle.load(dbfile) 
    #for keys in db: 
    #    print(keys, '=>', db[keys]) 
    dbfile.close() 
    return db

def addDataToDict(db, idd,  tag):
    #add record preventing the data from overwriting what is already shored
    if idd in db.keys():
        print("Error, Item already in list, check key!")
        raise Exception
    else: 
        print('Adding Item')
        db[idd] = tag

def addArea(df, areas):
    dfcopy = df.drop(['NAICS'], axis=1)
    dfcopy = dfcopy.set_index('ReferenceNumber')
    counter = 0
    for i in dfcopy.index:
        if str(i) in areas.keys():
            #print(i)
            dfcopy.at[i, 'Area'] = areas[str(i)] 
            counter += 1
    #print(counter)

    return dfcopy.reset_index()