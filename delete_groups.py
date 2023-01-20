import requests
import json

from authentication import Config, account_name, auth_headers
from logging_config import configure_logger, log_path
from get_groups import get_group_name

account = Config.get_account_config(account_name)

# change account in authentication.py
iam_url = account.get('iam_url')
tenant = account.get('tenant')
file_path = account.get('file_path')

#deletes all the projects in the csv file by id
logger = configure_logger(log_path + 'delete_group_set_' + account_name + '.log')

def delete_group_set(groupid):
    url = iam_url + "/auth/admin/realms/" + tenant + "/groups/" + groupid
    try:
        response = requests.delete(url, headers=auth_headers)
        if response.status_code == 204:
            print("Project with ID " + groupid + " deleted!")
        else:
            print(f'Error: {response.status_code}')

    except requests.exceptions.RequestException as e:
        print(e)

with open(file_path + "/all_groups_ids.json") as f:
    data = json.loads(f.read())

for group in data:
    group_id = group['id']
# commented below line to avoid mistakes   
#    delete_group_set(group_id)


logger = configure_logger(log_path + 'delete_group_' + account_name + '.log')
group_id='31eceefb-d606-4e08-bb1c-a849c258801f'
def delete_group(group_id):
    url = iam_url + "/auth/admin/realms/" + tenant + "/groups/" + group_id
    try:
        response = requests.delete(url, headers=auth_headers)
        if response.status_code == 204:
            group_name = get_group_name(group_id)
            print("Project with name " + group_name + " deleted!")
        else:
            print(f'Error: {response.status_code}')

    except requests.exceptions.RequestException as e:
        print(e)

