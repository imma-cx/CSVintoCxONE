import requests
import json
import os

#from auth.authHeaders import iam_url, tenant, auth_headers
#from auth.authHeaders_sch import iam_url_sch, tenant_sch, auth_headers_sch, server_url_sch
from auth.authHeaders_prod import iam_url_prod, tenant_prod, auth_headers_prod, server_url_prod

from logging_config import configure_logger, log_path

server_url = server_url_prod
tenant = tenant_prod
auth_headers = auth_headers_prod
iam_url = iam_url_prod
file_path = "output/production/"

url = server_url + "/api/projects?offset=0&limit=500"

#response = requests.get(url, headers=auth_headers)

def get_projects(response):
    response = requests.get(url, headers=auth_headers)
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        with open(file_path + 'all_projects.json', 'w') as f:
            json.dump(response.json(), f)
        
        return response.json()

    except ValueError as e:
        print(f"Error parsing response JSON: {e}")
    return {}

#get_projects(response)

logger = configure_logger(log_path + 'get_group_name.log')

def get_project_name(project_id):
    url = server_url + "/" + project_id
    try:
        response = requests.get(url, headers=auth_headers)
        projects = response.json()
        for project in projects:
            if project["id"] == project_id:
                return project["name"]
    except requests.exceptions.RequestException as e:
        logger.exception(f"An error occurred: {e}")
        raise e

#get_group_name(group_id)

def __get_projects_names(response):
    list_names = [{"name": project["name"]} for project in response.json()['projects']]

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(file_path + 'all_projects_names.json', 'w') as f:
        json.dump(list_names, f)

#__get_projects_names(response)


def __get_projects_ids(response):
    list_ids = [{"id": project["id"]} for project in response.json()['projects']]

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(file_path + 'all_projects_ids.json', 'w') as f:
        json.dump(list_ids, f)

#__get_projects_ids(response)


name = ''
def __get_project_id(name):

    print(name)
    project = next(filter(lambda el: el['name'] == name.strip(), response.json()['projects']), None)
    if project:
        print("The id of the project named " + name + " is " + project['id'])
        return project['id']
    else:
        raise Exception("Not Found")

#__get_project_id(name)


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

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(file_path + 'group_ID.json', 'w') as f:
        json.dump(group_ids, f)

#__get_groups_id_json(file)

