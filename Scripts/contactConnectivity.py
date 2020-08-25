#!/usr/bin/env python
# coding: utf-8

#  Working package*********************
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

# Updated 15/08
def load_data(path, sheet=None, ignore_hash=True):
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
    # Remove n columns are system hash, remove them
    if ignore_hash:
        data = data[[col for col in data.columns if not '(Do Not Modify)' in col]]
        
    data.dropna(axis=1, how='all', inplace=True)
    #Get dataframe with distince columns calues
    data = data[[c for c in data.columns if len(data[c].unique()) > 1]]
    
    return data 


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
    fin_contact_mask = multiple_app(data_with_excluded_col, 'FinContactName', 'Reference Number')
    auth_contact_mask = multiple_app(data_with_excluded_col, 'AuthContactName', 'Reference Number')
    
    # Filter original data for these with excluded cols
    app_fin_contact = filter_data(data_with_excluded_col, 'FinContactName', fin_contact_mask)
    app_auth_contact = filter_data(data_with_excluded_col, 'AuthContactName', auth_contact_mask)
    #combine the data and remove duplicstes
    combined_data = pd.concat([app_fin_contact, app_auth_contact]).drop_duplicates('Reference Number')
    
    return combined_data.sort_values(by=['AuthContactName', 'FinContactName'])

#Created 15/08 Tested to get only unique dplicates according to columns
def get_duplicates(df, subset=None, unique=False): 
    """Takes a dataframe and a set of column names and return unque duplicates

    Args:
        df (pd.dataframe): The dataframe tp process
        subset (str or list): column(s) to get duplicates on
        unique (bool): Defaults to false so all duplicated are returned. If true only unique list of 
                       duplicates are returned

    Returns:
        duplicates: Dataframe of duplicates
    """
    #mask = df.duplicated(subset=subset, keep=False)
    if unique:
        duplicates = df[df.duplicated(subset=subset, keep=False)].drop_duplicates(subset=subset)
    else:
        duplicates = df[df.duplicated(subset=subset, keep='first')]
    
    #duplicates = df[df.duplicated(subset=subset, keep=False)].drop_duplicates(subset=subset)

    return duplicates.sort_values(by=subset, ascending=False)
#------------- end helpers -----------------------------------------------

def get_non_duplicates(df, subset=None, keep='first'): 
    """Takes a dataframe and a set of column names and return unique rows

    Args:
        df (pd.dataframe): The dataframe tp process
        subset (str or list): column(s) to get duplicates on

    Returns:
        data: Dataframe of processed data
    """
    
    non_duplicates = df.drop_duplicates(subset=subset, keep=keep)

    return non_duplicates

def get_non_duplicate_contacts(df, subset=None, keep='first'):
    """Takes a dataframe and a set of column names and return unique rows

    Args:
        df (pd.dataframe): The dataframe tp process
        subset (str or list): column(s) to get duplicates on

    Returns:
        non_duplicates: Dataframe of processed data
    """

    #add column of row counts for nan. This will be used to determine which is upto date
    data = df.drop_duplicates()
    data['NanCount'] = data.isnull().sum(axis=1)
    data.sort_values(by=[' Full Name', 'NanCount'], ascending=False, inplace=True)
    #drop column of row counts for nan
    non_duplicates = data.drop('NanCount', axis=1).drop_duplicates(subset=subset, keep=keep)     
    
    #non_duplicates.sort_values(by=[' Full Name'], ascending=False, inplace=True)

    return non_duplicates.reset_index()
    
#------------- end helpers -----------------------------------------------
