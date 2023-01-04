import requests
import json

from authHeaders import iam_url, tenant, auth_headers
from authHeaders_sch import iam_url_sch, tenant_sch, auth_headers_sch, server_url_sch
from authHeaders_prod import iam_url_prod, tenant_prod, auth_headers_prod, server_url_prod

# *** which TENANT?  ******
# Canary [Default]
#file_path = "/outputs"

# Schroders:
# server_url = server_url_sch
# tenant = tenant_sch
# auth_headers = auth_headers_sch
# iam_url = iam_url_sch
# file_path = "output/schroders/"

# Production
server_url = server_url_prod
tenant = tenant_prod
auth_headers = auth_headers_prod
iam_url = iam_url_prod
file_path = "output/production/"

url = server_url + "/api/projects?offset=0&limit=500"

response = requests.get(url, headers=auth_headers)
print(response.json())

def __get_projects_names(response, cxone_env):

    list_names = [{"name": project["name"]} for project in response.json()['projects']]

    with open(file_path + 'all_projects_names.json', 'w') as f:
        json.dump(list_names, f)

__get_projects_names(response)

def __get_groups_ids(response):
    list_ids = [{"id": item["id"]} for item in response.json()]

    with open(file_path + 'all_groups_ids.json', 'w') as f:
        json.dump(list_ids, f)

#__get_groups_ids(response)


def __get_group_id(name):

    print(name)
    group = next(filter(lambda el: el['name'] == name.strip(), response.json()), None)
    if group:
        print(group['id'])
        return group['id']
    else:
        raise Exception("Não Encontrou")
    __get_group_id(name)

file = 'all_groups_names.json'

def __get_groups_id_json(file):
    
    group_ids = []
    with open(file, 'r') as f:
        data = json.load(f)
        for item in data:
            group_name = item.get('name')
            group = next(filter(lambda el: el['name'] == group_name, data), None)

            if group:
                  # group_json = json.dumps(group['id'])
                    group_id = group['id']
                    group_ids.append(group_id)

    with open('group_ID.json', 'w') as f:
        json.dump(group_ids, f)

#__get_groups_id_json(file)

