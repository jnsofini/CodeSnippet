from contactConnectivity import load_data, get_non_duplicate_contacts, get_duplicates
import pandas as pd

file_path = r'C:\Users\Downloads\Contacts Advanced Find View 2020-08-15 1-55-00 PM.xlsx'

raw_data = load_data(file_path, ignore_hash=False)

# ## 1.  Identifying duplicates
# There are multiple ways to identifying diplicates. Here we use the few robust combination starting with the most strigent to the less stringent. The following are used according to preference
#  - Full name / Phone / Email / Parent 
#  - Full name / Phone / Email 
#  - Full name / Phone 
#  - Full name (less efficient way)
#Get all contacts that are duplicates and they can then be merge

dup_detection_col = [' Full Name', 'Business Phone', 'Email', 'Parent account']

duplicates_FN_BP_E_PA = get_duplicates(raw_data, dup_detection_col)
print(duplicates_FN_BP_E_PA.head(2))
print(duplicates_FN_BP_E_PA.shape)

duplicates_FN_BP_E = get_duplicates(raw_data, dup_detection_col[:-1])
print(duplicates_FN_BP_E.head(2))
print(duplicates_FN_BP_E.shape)

duplicates_FN_BP = get_duplicates(raw_data, dup_detection_col[:2])
print(duplicates_FN_BP.head(2))
print(duplicates_FN_BP.shape)
