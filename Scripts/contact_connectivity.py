from contactConnectivity import load_data, get_non_duplicate_contacts, get_duplicates
import pandas as pd

file_path = r'C:\Users\Downloads\Contacts Advanced Find View 2020-08-20 8-46-05 AM.xlsx'

raw_data = load_data(file_path, ignore_hash=False)

#Get unique accounts that should remain
clean_contact = get_non_duplicate_contacts(raw_data, ' Full Name')
#Get duplicates that should be removed from the system
names_duplicate = get_duplicates(raw_data, ' Full Name')