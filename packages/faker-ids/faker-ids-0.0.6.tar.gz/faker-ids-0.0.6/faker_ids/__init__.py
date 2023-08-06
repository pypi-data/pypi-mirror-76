import pandas as pd
import json

import os
this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "id.csv")
csv = pd.read_csv(DATA_PATH)

# csv = pd.read_csv('faker_ids/id.csv')
csv = csv.values.tolist()

def get_ids(n):
    id = []
    for i in range(n):
        temp = {}
        temp['firstName'] = csv[i][0]
        temp['lastName'] = csv[i][1]
        temp['emailId'] = csv[i][2]
        temp['mobileNumber'] = csv[i][3]    
        id.append(temp)
    return json.dumps(id, indent=4, sort_keys=True)
# print(get_ids(3))