#!/usr/bin/env python
# coding: utf-8

# 
# Analysis of multiple businesses in linked to one financial or authorized contact
# This notebook makes multiple analysis. The analysis are splitted into various sections. 
# They are splittted connectibity via authorized  financial or authorized contact.# 
# 
# Import usedful packages
from contactConnectivity import load_data, get_non_duplicate_contacts, get_duplicates, add_column,\
     get_apps, select_column, combine_account, get_connectivity
import pandas as pd
import numpy as np
import pickle 
import string
import csv
import os


#------------- end helpers -----------------------------------------------

data_path = r'C:\Users\Downloads\Application Advanced Find View 2020-08-29 2-29-22 PM.xlsx'
sheet = "Application Advanced Find View"
raw_data = load_data(data_path, sheet=sheet)


app_col = [
    'Reference Number', 'Business Number', 'Legal Name', 'Operating Name',
    'First Name', 'Last Name', 'Application Status', 
    'Authorized Business Contact Email', 'Authorized Business Contact First Name',
    'Authorized Business Contact Last Name', 'Authorized Business Contact Title',
    'Authorized Business Telephone Number'
    ]


sel_data = select_column(raw_data, app_col)
authorized_contact =  ['Authorized Business Contact First Name', 'Authorized Business Contact Last Name']
financial_contact =  ['First Name', 'Last Name']
d1 = add_column(sel_data, authorized_contact, 'AuthContactName')
data_with_added_col = add_column(d1, financial_contact, 'FinContactName')

#data_ex_incomplete_duplicates.to_csv('data_ex_incomplete_duplicates-08-06.csv')


exclude_status = ['Application Ineligible | Demande non admissible', 'Application Incomplete | Demande incomplète',
       'Not Supported | Non soutenus', 'Duplicate Application | Double de la demande']

data_ex_incomplete_duplicates_notsup = get_apps(data_with_added_col, exclude_status)
#print(data_ex_incomplete_duplicates_notsup.head(2))
print(data_ex_incomplete_duplicates_notsup.shape)

print()
print('-----------------------------------------------------------------------------------')




dropcols = ['First Name', 'Last Name', 'Application Status',
    'Authorized Business Contact Email',
    'Authorized Business Contact First Name',
    'Authorized Business Contact Last Name',
    'Authorized Business Contact Title',
    'Authorized Business Telephone Number'
    ]
related_fin_contact = get_connectivity(
    data_ex_incomplete_duplicates_notsup.drop(dropcols, axis=1), 'FinContactName'
    )
related_aut_contact = get_connectivity(
    data_ex_incomplete_duplicates_notsup.drop(dropcols, axis=1), 'AuthContactName'
    )
    
fc = combine_account(related_fin_contact, 'Financial Contact')
ac = combine_account(related_aut_contact, 'Authorized Contact')

dd = pd.concat([fc, ac])