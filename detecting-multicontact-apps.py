#!/usr/bin/env python
# coding: utf-8

# # I have a few thousand applications that contain lot's of information about the applicant, the business,
# business contact and other useful info. The task in this notebook is the analysis of multiple business with 
# one contacts 
# 
# 
# Import usedful packages

import pandas as pd
import pickle 
import string
import csv
import os


# ======================= Helper functions =========================

def load_data(path, sheet=None):
    """Function to load data from an excel file

    Args:
        path (string): contain the path to the file
        sheet (string, optional): Identify the sheet to read in a multisheet. Defaults to None.

    Returns:
        pandas dataframe: The loaded data
    """
    if sheet:
        xls = pd.ExcelFile(path)
        data = pd.read_excel(xls, sheet)
    else:
        data = pd.read_excel(path)        
    # if the first n columns are system hash, remove them with the second command
    return data [data.columns[3:]]


def get_selection(df, colname):
    """Get dataframe with columns colname name

    Args:
        df (dataframe): data from which a columns are selected
        colname (list of columns): list of columns

    Returns:
        dataframe: data with columns colname
    """
    
    return df[colname]

def get_contacts(df):
    """Gets the list of names of contacts that appears more than once

    Args:
        df (dataframe): full list of application

    Returns:
        list: list of names that are linked to more than one application
    """    
    names_ref_count = df.groupby(
        ['First Name','Last Name'], as_index=False
    )['Reference Number'].count().sort_values(['Reference Number'], ascending=False)
    
    #Get list for which more than 2 contact names occur
    more_occurance_name = names_ref_count[names_ref_count['Reference Number']>1]
    names = [' '.join([fn, ln]) for fn, ln, _ in more_occurance_name.values]
    
    return names
    
def filter_data(df, col, vals):
    #filter for values of col in vals    
    data = df[df[col].isin(vals)]
    
    return data

def add_column(d, cols='', new_col='ContactName'):
    """Adds a new column to the df by combining two columns in the application

    Args:
        d (dataframe): Data to which a new colum is to be added
        cols (str, optional): Name of new column. Defaults to ''.
        new_col (str, optional): Name of new column. Defaults to 'ContactName'.

    Returns:
        dataframe: The dataframe with new column added
    """
    if not cols:
        cols = ['First Name', 'Last Name']
    df = d.copy()
    df[new_col] = df[cols[0]].map(str) + ' ' + df[cols[1]].map(str)
    
    return df


# ----------------------------------------------------------------------------------------
# Here, we will check applications that are linked to a single financial contact. 
# The approached used is to group the data according to that column and then count 
# the number of applications submitted


data_path = "C:\\Users\\data\\data.xlsx"
sheet = "Application Advanced Find View"
raw_data = load_data(data_path, sheet=sheet)


app_col = ['Reference Number', 'Business Number', 
                            'Legal Name', 'Operating Name',
                            'First Name', 'Last Name', 'Application Status', 
                            'Authorized Business Contact Email',
                            'Authorized Business Contact First Name',
                            'Authorized Business Contact Last Name',
                            'Authorized Business Contact Title',
                            'Authorized Business Telephone Number']


#select columns we want to work with and then add new column
selected_raw_data = get_selection(raw_data, app_col)


selected_raw_data_FN = add_column(selected_raw_data)
print(selected_raw_data_FN.head(2))

contacts_with_multiple_app = get_contacts(selected_raw_data_FN)

print(contacts_with_multiple_app[:4])

# 5. Retrieve applications belonging to these individuals

multiple_app_one_contact = filter_data(selected_raw_data_FN, 'ContactName', contacts_with_multiple_app)

multiple_app_one_contact_sorted = multiple_app_one_contact.sort_values(by='ContactName')

#multiple_app_one_contact_sorted.to_csv('All-applications-lined-one-contact.csv')
print(multiple_app_one_contact_sorted.head(2))







