import requests
import json

from authHeaders import auth_headers, iam_url, tenant

def __delete_group_set(groupid):

    url = iam_url + "/auth/admin/realms/" + tenant + "/groups/" + groupid

    try:
        response = requests.delete(url, headers=auth_headers)
        if response.status_code == 204:
            print("Project with ID " + groupid + " deleted!")
        else:
            print(f'Error: {response.status_code}')

    except requests.exceptions.RequestException as e:
        print(e)

with open("all_groups_ids.json") as f:
    data = json.loads(f.read())

for group in data:
    group_id = group['id']
    print(group_id)
 # commented below line to avoid mistakes   
    __delete_group_set(group_id)