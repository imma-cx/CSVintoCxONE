import requests
import json
import os

from authentication import Config, account_name, auth_headers
from logging_config import configure_logger, log_path

account = Config.get_account_config(account_name)
server_url = account.get('server_url')
file_path = account.get('file_path')

logger = configure_logger(log_path + "get_projects.log")

def get_projects(response):
    url = server_url + "/api/projects?offset=0&limit=500"
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

logger = configure_logger(log_path + 'get_project_name_' + account_name + '.log')

#project_id = '236246ca-1c02-4960-b0bf-9cb1bbce75d0'

def get_project_name(project_id):
    url = server_url + "/api/projects/" + project_id
    try:
        response = requests.get(url, headers=auth_headers)
        if response.status_code == 200:
            projects = response.json()
            for project in projects:
                if int(project["id"]) == project_id:
                    logger.info("Project name is " + project["name"])
                    return project["name"]
        else:
            logger.error(f"Error updating project, status code: {response.status_code}")
        return {}

    except requests.exceptions.RequestException as e:
        logger.exception(f"An error occurred: {e}")
        raise e

#get_project_name(project_id)

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
response = ""
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



# [09:02] Michael Kubiaczyk
# as an admin user, GET {{Cx1_IAM}}/auth/admin/realms/{{Cx1_Tenant}}/clients?briefRepresentation=true

# [09:03] Michael Kubiaczyk
# response: 
#     {
#         "id": "bc5884f2-19b5-4783-a697-86ca44bab03e",
#         "clientId": "mikek_jenkins_oauth",
#         "surrogateAuthRequired": false,
#         "enabled": true,
#         "alwaysDisplayInConsole": false,
#         "clientAuthenticatorType": "client-secret",
#         "secret": "c9592102-7ac8-4eee-a80b-75e770919a1d",

