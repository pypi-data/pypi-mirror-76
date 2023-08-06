import pandas as pd
import json

csv = pd.read_csv('id.csv')
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
