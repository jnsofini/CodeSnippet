#!/usr/bin/env python
# coding: utf-8

#  Working package*********************
# The idea of this work is to compare two csv files which contain contacts information and identify the di
# difference. One file contain the contacts that are already in the system, and the other contains a list
# that should be added to the system. However, some of these contacts are already in the system. SO we want
# to identify those that are already in the system and then upload only the difference
# 

import pandas as pd
import numpy as np
from contactConnectivity import load_data
import csv


# file location
minerva_path = r'C:\Users\Downloads\Contacts Advanced Find View 2020-09-01 11-26-04 AM.xlsx'
isr_path = r'C:\Users\Documents\List Template_ISR updates.xlsx'
# --------------- Helper functions --------------------------------

# load
system_contact = load_data(minerva_path)
#format column headers to title format
system_contact.columns = [c.title() for c in system_contact.columns]

#Load contacts to be imported from isr
isr_contact = data = pd.read_excel(isr_path, header=1)

# ## 2.  Common data
# The common data can be identified via an inner join. We start by a less regorous condition which is the 
# first and last names. That leads to 362 contacts that are already in the system. 

common_contacts = pd.merge(system_contact[['First Name', 'Last Name']], isr_contact, on=['First Name', 'Last Name'])

# Common contacts are those that are already in the system
# To get the difference that whould be imported, we use concat
contacts_to_import = pd.concat([common_contacts, isr_contact], sort=False).drop_duplicates(keep=False)
# contacts_to_import.to_csv('contacts_not_in_system_FL.csv', index=False)


# ## 3.  Common data on three fields
# Here a more regorous condition which is the first and last names and email is used. That leads to 362 contacts 
# that are already in the system. This leads to 193
common_contacts_3 = pd.merge(
    system_contact[['First Name', 'Last Name', 'Email']], 
    isr_contact, on=['First Name', 'Last Name', 'Email']
    )

contacts_to_import_3 = pd.concat([common_contacts_3, isr_contact], sort=False).drop_duplicates(keep=False)

# Putting all together
def get_contact_difference(system_file, external_file, on):
    """Takes two pd.dataframe objects and create complement file of external_file. That is data that is in
    external_file and not in system_file

    Args:
        system_file (pd.dataframe): data that is present in the system
        external_file (pd.dataframe): external file to be imported
        on (list): columns to base the comparison on

    Returns:
        pd.dataframe: the difference data equivalent to B n A - A for set A and B
    """

    common_contacts = pd.merge(system_file[on], external_file, on=on) #Intersection
    contacts_to_import = pd.concat(
        [common_contacts, external_file], sort=False
        ).drop_duplicates(keep=False) #Use intersection and original file to get the difference

    return contacts_to_import




