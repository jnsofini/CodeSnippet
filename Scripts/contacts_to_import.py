#!/usr/bin/env python
# coding: utf-8

# ## Basics instruction
# run the cell by __shift enter__
# 
# # Contact analysis
# Here we want to fingure which contacts should be imported and which shouldn't
#  - Comparing system contacts to ISR contacts
#  - Get the compliment

# In[ ]:


import pandas as pd
import numpy as np


# ### Getting data

# In[ ]:


# file location
minerva_path = r'C:\Users\Downloads\Contacts Advanced Find View 2020-09-01 11-26-04 AM.xlsx'
isr_path = r'C:\Users\Documents\List Template_ISR updates.xlsx'


# In[ ]:


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


# In[ ]:


#Get data
system_contact = pd.read_excel(minerva_path)
isr_contact = pd.read_excel(isr_path, header=1)
#format column headers to title format
system_contact.columns = [c.title() for c in system_contact.columns]


# In[ ]:


cols = ['First Name', 'Last Name', 'Email']

contacts_to_import = get_contact_difference(system_contact, isr_contact, cols)


# In[ ]:


#Save data to csv
contacts_to_import.to_csv('contacts_not_in_system.csv')


# In[ ]:


contacts_already_in_system = pd.merge(system_contact[on], isr_contact, on=cols) #Intersection
#Save data to csv
contacts_already_in_system.to_csv('contacts_already_in_system.csv')

