#!/usr/bin/env python
# coding: utf-8

# 
# Analysis of multiple businesses in linked to one financial or authorized contact
# This notebook makes multiple analysis. The analysis are splitted into various sections. 
# They are splittted connectibity via authorized  financial or authorized contact.# 
# 
# Import usedful packages

import pandas as pd
import pickle 
import string
import csv
import os

# --------------- Helper functions --------------------------------

def load_data(path, sheet=None):
    """Function to load data from an excel file

    Args:
        path (string): contain the path to the file
        sheet (string, optional): Name of sheet to read in a multisheet. Defaults to None.

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


def select_column(df, colname):
    """Get dataframe with columns colname name

    Args:
        df (dataframe): data from which a columns are selected
        colname (list of columns): list of columns

    Returns:
        dataframe: data with columns colname
    """
    
    return df[colname]


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


def filter_data(df, col_name, row_vals, select=True):
    """Filter for values of col in row_vals   

    Args:
        df (pd.dataframe): Data to operate on
        col_name (str): column name
        row_vals (list): list if column values to operate on
        select (bool, optional): Decision to select or exclude on row_vals. Defaults to True.

    Returns:
        data: list of values
    """
 
    if select:
        data = df[df[col_name].isin(row_vals)]
    else:
        data = df[~df[col_name].isin(row_vals)]
    
    return data

def multiple_app(df, group_col, filter_col):
    """Takes a dataframe and column name and indices that satisfy a condition

    Args:
        df (pd.dataframe): The dataframe tp process
        group_col (str or list): column(s) to group by
        filter_col (str): column to filter on

    Returns:
        data: Dataframe of processed data
    """

    selected = df.groupby(
        group_col, as_index=False
    )[filter_col].count().sort_values([filter_col], ascending=False)
    filtered = selected[selected[filter_col]>1]
    multiple_vals = filtered[group_col].unique()

    return multiple_vals

# Putting everything together
def get_apps(df, exclude_status):
    """Putting all the functions together to get the apps

    Args:
        df (pd.dataframe): dataframe to process
        exclude_status (list): List of values to exclude

    Returns:
        dataframe: the processed applications
    """
    
    data_with_excluded_col = filter_data(df, 'Application Status', exclude_status, select=False)
    #print(data_with_excluded_col.head(2))
    fin_contact_mask = multiple_app(data_with_excluded_col, 'FinContactName', 'Reference')
    auth_contact_mask = multiple_app(data_with_excluded_col, 'AuthContactName', 'Reference')
    
    # Filter original data for these with excluded cols
    app_fin_contact = filter_data(data_with_excluded_col, 'FinContactName', fin_contact_mask)
    app_auth_contact = filter_data(data_with_excluded_col, 'AuthContactName', auth_contact_mask)
    #combine the data and remove duplicstes
    combined_data = pd.concat([app_fin_contact, app_auth_contact]).drop_duplicates('Reference')
    
    return combined_data.sort_values(by=['AuthContactName', 'FinContactName'])


#------------- end helpers -----------------------------------------------

data_path = r"data.xlsx"
sheet = "Application Advanced Find View"
raw_data = load_data(data_path, sheet=sheet)

#Example
app_col = ['Reference', 'Business Number', 'LegalName', 'OperatingName',
           'First Name', 'Last Name', 'Application Status', 'Authorized Contact Email',
           'Authorized Contact First Name', 'Authorized Contact Last Name',
           'Authorized Contact Title', 'Authorized Telephone Number']


sel_data = select_column(raw_data, app_col)
authorized_contact =  ['Authorized Contact First Name', 'Authorized Contact Last Name']
financial_contact =  ['First Name', 'Last Name']
d1 = add_column(sel_data, authorized_contact, 'AuthContactName')
data_with_added_col = add_column(d1, financial_contact, 'FinContactName')


exclude_status = ['Application Incomplete', 'Duplicate Application']
data_ex_incomplete_duplicates = get_apps(data_with_added_col, exclude_status)
print(data_ex_incomplete_duplicates.head(2))
print(data_ex_incomplete_duplicates.shape)

#data_ex_incomplete_duplicates.to_csv('data_ex_incomplete_duplicates-08-06.csv')


exclude_status = ['Application Ineligible',
       'Application Incomplete',
       'Not Supported',
       'Duplicate Application']

data_ex_incomplete_duplicates_notsup = get_apps(data_with_added_col, exclude_status)
print(data_ex_incomplete_duplicates_notsup.head(2))
print(data_ex_incomplete_duplicates_notsup.shape)


#data_ex_incomplete_duplicates_notsup.to_csv('data_ex_incomplete_duplicates_notsup_ineli-08-06.csv')
