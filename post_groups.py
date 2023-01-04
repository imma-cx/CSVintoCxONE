import requests
import json

from authHeaders import auth_headers, iam_url, tenant

relative_url = iam_url + "/auth/admin/realms/" + tenant + "/groups"

def __create_group_set(group_data, parent_group=None):

    url=relative_url
    if parent_group:
        url=url + "/" + parent_group
    try:
        response = requests.post(url, json.dumps(group_data), headers=auth_headers)
        if response.status_code == 201:
            print("New Group with Name " + json.dumps(group_data) + " has been created!")
        else:
            print(f'Error: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(e)

with open("groups.json") as f:
    data = json.load(f)
    for group in data:
        __create_group_set(group)

