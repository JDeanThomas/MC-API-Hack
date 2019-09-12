
import json
import logging
import requests
import pandas as pd
from io import StringIO
import azure.functions as func
from pandas.io.json import json_normalize
from azure.storage.blob import BlockBlobService
from datetime import datetime, timezone, timedelta
from .recursivejson import extract_values


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.utcnow().replace(
        tzinfo=timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    # Storage account credentials
    account_name = "XXXXXXXX"
    account_key = "XXXXXXXXX"

    blob_service = BlockBlobService(account_name=account_name, account_key=account_key)


    members = pd.read_csv(StringIO(blob_service.get_blob_to_text(container_name='oajustice', blob_name='members').content))
    #.drop(['Unnamed: 0'], axis=1)

    # API credentials
    keys = {"MCAPIKeyPublic": "XXXXXXXXXXXX",
            "MCAPIKeySecret": "XXXXXXXXXXXX"}

    r = requests.post(
        'http://apibeta.membercentral.com/v1/authenticate', json=keys)

    token = r.json()
    token = token["data"]["token"]
    token = {'Authorization': 'Bearer ' + token}

    members_url = 'http://apibeta.membercentral.com/v1/member'
    params = {"count": 10000}

    req = requests.get(members_url, json=params, headers=token)

    '''
    Query member API, check if entries have been added or updated since last
    event trigger. If so, make list of member IDs added or updated, make
    revursive calls to API to get updates and additions, update member data,
    write out CSV binary, and commit to Azure Blob storage. 
    '''

    # Get linst index of all member URIs
    last_update = pd.to_datetime(extract_values(req.json(), 'datelastupdated'), infer_datetime_format=True)
    now = datetime.now()

    # CHack for updates
    if any(last_update > now.replace(tzinfo=timezone.utc)-timedelta(days=1)):

        updates = pd.DataFrame(extract_values(req.json(), 'membernumber'), columns=['member_number'])
        updates['last_update'] = pd.to_datetime(extract_values(req.json(), 'datelastupdated'), infer_datetime_format=True)
        # Creats a data frame of member IDs and update timestamps for members with changes
        updates = updates.loc[updates['last_update'] > now.replace(tzinfo=timezone.utc)-timedelta(days=1)]

        # Make API calls to get updates and additions
        member_updates = []
        base_url = 'http://apibeta.membercentral.com/v1/member/'
        for uri in updates['member_number']:
            member_uri = base_url + str(uri)
            response = requests.get(member_uri, headers=token)
            if response.status_code == 200:
                member_updates.append(response.json()["data"]["member"])
            else:
                print(response.text)
                print(response.status_code)

        # Update data and comit to Blod storage
        member_updates = json_normalize(member_updates)
        member_updates.set_index('membernumber', inplace=True)
        members.set_index(members['membernumber'], inplace=True)
        members.update(member_updates)
        output = StringIO()
        output = members.to_csv(encoding="utf-8", index=False)
        blob_service.create_blob_from_text('oajustice', 'members', 'Members.csv', output)