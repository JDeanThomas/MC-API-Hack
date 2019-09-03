import json
import requests
from pandas.io.json import json_normalize


keys = {"MCAPIKeyPublic": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "MCAPIKeySecret": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"}

r = requests.post('http://apibeta.membercentral.com/v1/authenticate', json=keys)

token = r.json()
token = token["data"]["token"]
token = {'Authorization': 'Bearer ' + token}

membersURL = 'http://apibeta.membercentral.com/v1/member'
params = {"count": 10000}

req = requests.get(membersURL, json=params, headers=token)

members = req.json()
members["data"]["members"]

out = json_normalize(members["data"]["members"])