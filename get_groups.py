import requests
import json
import os

from authentication import Config, account_name, auth_headers
from logging_config import configure_logger, log_path

account = Config.get_account_config(account_name)

# change account in authentication.py
iam_url = account.get('iam_url')
tenant = account.get('tenant')
file_path = account.get('file_path')

url = iam_url + "/auth/admin/realms/" + tenant + "/groups"
response=""

logger = configure_logger(log_path + 'get_groups_' + account_name + '.log')

def get_groups(response):
    response = requests.get(url, headers=auth_headers)
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        with open(file_path + 'all_groups.json', 'w') as f:
            json.dump(response.json(), f)
        return response.json()

    except ValueError as e:
        print(f"Error parsing response JSON: {e}")
    return {}

get_groups(response)

def get_groups_names_file(response):
    list_names = [{"name": item["name"]} for item in response.json()]

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(file_path + 'all_groups_names.json', 'w') as f:
        json.dump(list_names, f)

#get_groups_names(response)

def __get_groups_ids(response):
    list_ids = [{"id": item["id"]} for item in response.json()]

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(file_path + 'all_groups_ids.json', 'w') as f:
        json.dump(list_ids, f)

#__get_groups_ids(response)

# NOT FINISHED - get group ID from name, into csv
#def __get_group_id(name):

#     print(name)
#     group = next(filter(lambda el: el['name'] == name.strip(), response.json()), None)
#     if group:
#         #print(group['id'])
#         return group['id']
#     else:
#         raise Exception("Não Encontrou")
#     __get_group_id(name)

# file = file_path + 'all_groups_names.json'

logger = configure_logger(log_path + 'get_group_id_' + account_name + '.log')
#group_name = "bd57cc19-7146-43a8-9706-b7c3fa584eff"
def get_group_id(group_name):
    try:
        response = requests.get(url, headers=auth_headers)
        groups = response.json()
        for group in groups:
            if group["name"] == group_name:
                #print(group["id"])
                return group["id"]
    except requests.exceptions.RequestException as e:
        logger.exception(f"An error occurred: {e}")
        raise e

#get_group_id(group_name)

logger = configure_logger(log_path + 'get_group_name_' + account_name + '.log')

def get_group_name(group_id):
    group_id = group_id.replace('"', '')
    try:
        response = requests.get(url, headers=auth_headers)
        groups = response.json()
        for group in groups:
            if group["id"] == group_id:
                return group["name"]
                
    except requests.exceptions.RequestException as e:
        logger.exception(f"An error occurred: {e}")
        raise e

#get_group_name(group_id)

# def __get_groups_id_json(file):
    
#     group_ids = []
#     with open(file, 'r') as f:
#         data = json.load(f)
#         for item in data:
#             group_name = item.get('name')
#             group = next(filter(lambda el: el['name'] == group_name, data), None)

#             if group:
#                   # group_json = json.dumps(group['id'])
#                   #  group_id = group['id']
#                     group_id = __get_group_id(group)
#                     group_ids.append(group_id)

#     if not os.path.exists(file_path):
#         os.makedirs(file_path)
#     with open(file_path + 'groups_IDs.json', 'w') as f:
#         json.dump(group_ids, f)

#__get_groups_id_json(file)

