import auth.authHeaders as authHeaders
#import auth.authHeaders_sch as authHeaders_sch
import auth.authHeaders_prod as authHeaders_prod

import requests
import json
import os


iam_url = authHeaders_prod.iam_url_prod
tenant = authHeaders_prod.tenant_prod
auth_headers = authHeaders_prod.auth_headers_prod
file_path = "output/production/"

url = iam_url + "/auth/admin/realms/" + tenant + "/groups"

response = requests.get(url, headers=auth_headers)
#print(response.json())

def __get_groups(response):
    try:
        return response.json()
    except ValueError as e:
        print(f"Error parsing response JSON: {e}")
    return {}


def __get_groups_names(response):
    list_names = [{"name": item["name"]} for item in response.json()]

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(file_path + 'all_groups_names.json', 'w') as f:
        json.dump(list_names, f)

#__get_groups_names(response)

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

