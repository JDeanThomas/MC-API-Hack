#!/usr/bin/env python3

import json
import requests
import pandas as pd
from pandas.io.json import json_normalize
from recursivejson import extract_values


keys = {"MCAPIKeyPublic": "0919b40440994633bd1dae39efcb9abc",
        "MCAPIKeySecret": "1173d0ec6d57489c8b43c73394049a58"}

r = requests.post('http://apibeta.membercentral.com/v1/authenticate', json=keys)

token = r.json()
token = token["data"]["token"]
token = {'Authorization': 'Bearer ' + token}

members_url = 'http://apibeta.membercentral.com/v1/member'
params = {"count": 10000}

req = requests.get(members_url, json=params, headers=token)

# Get linst index of all member URIs
member_index = extract_values(req.json(), 'x-api-uri')

# Iterate calls to member URIs
data = []
base_url = 'http://apibeta.membercentral.com'
for uri in member_index:
    member_uri = base_url + str(uri)
    response = requests.get(member_uri, headers=token)
    if response.status_code == 200:
        data.append(response.json()["data"]["member"])
    else:
        print(response.text)
        print(response.status_code)



out = json_normalize(data)
out.to_csv('Members.csv')

member_index = pd.DataFrame({'Member_URIs': member_index})
member_index.to_csv('Member_index.csv')