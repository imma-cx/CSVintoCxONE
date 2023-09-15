import requests
import json
import os
import get_groups
import csv

from authentication import Config, account_name, auth_headers
from logging_config import configure_logger, log_path


account = Config.get_account_config(account_name)
server_url = account.get('server_url')
file_path = account.get('file_path')


def get_projects():
    logger = configure_logger(log_path + "get_projects_" + account_name + ".log")
    url = server_url + "/api/projects?offset=0&limit=1000"
    response = requests.get(url, headers=auth_headers)
    try:
        logger.info('Projects list retrieved')
        return response.json()
    except ValueError as e:
        print(f"Error parsing response JSON: {e}")
    return {}


def get_projects_to_file():
    logger = configure_logger(log_path + "get_projects_to_file_" + account_name + ".log")
    url = server_url + "/api/projects?offset=0&limit=500"
    response = requests.get(url, headers=auth_headers)
    try:
        if not os.path.exists(file_path):
            print('Folder ' + file_path + ' does not exist, creating it')
            os.makedirs(file_path)
        with open(file_path + '/all_projects.json', 'w') as f:
            json.dump(response.json(), f)
        logger.info('File all_projects.json created in ' + file_path + ' folder')
        return response.json()

    except ValueError as e:
        print(f"Error parsing response JSON: {e}")
    return {}

get_projects_to_file()


def get_project(project_id):
    logger = configure_logger(log_path + "get_project_" + account_name + ".log")

    if project_id == '' or project_id is None:
        logger.error("Project id is empty or null")
        return {}

    try:
        url = server_url + "/api/projects/" + project_id
        response = requests.get(url, headers=auth_headers)
        if response.status_code == 200:
            project = response.json()
            logger.info("Project " + project["name"] + " exists!")
            return response

    except requests.exceptions.RequestException as e:
        logger.exception(f"An error occurred: {e}")
        raise e


# project_id = '236246ca-1c02-4960-b0bf-9cb1bbce75d0'


def get_project_name(project_id):
    logger = configure_logger(log_path + 'get_project_name_' + account_name + '.log')

    url = server_url + "/api/projects/" + project_id
    try:
        response = requests.get(url, headers=auth_headers)
        if response.status_code == 200:
            project = response.json()
            if project["id"] == project_id:
                logger.info("Project name is " + project["name"])
                return project["name"]
        else:
            logger.error(f"Error updating project, status code: {response.status_code}")
        return {}

    except requests.exceptions.RequestException as e:
        logger.exception(f"An error occurred: {e}")
        raise e

# get_project_name(project_id)


def get_projects_names(response):
    list_names = [{"name": project["name"]} for project in response.json()['projects']]

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(file_path + 'all_projects_names.json', 'w') as f:
        json.dump(list_names, f)

#get_projects_names(response)


def get_projects_ids(response):
    list_ids = [{"id": project["id"]} for project in response.json()['projects']]

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(file_path + 'all_projects_ids.json', 'w') as f:
        json.dump(list_ids, f)

    get_projects_ids(response)


def get_project_id(name):
    projects = get_projects()
    projects_list = projects['projects']
    project = next((p for p in projects_list if p['name'] == name.strip()), None)
    if project:
        return project['id']
    else:
        return None

# get_project_id(name)


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


def get_projects_by_group(group_id):
    logger = configure_logger(log_path + 'get_project_by_group_' + account_name + '.log')

    projects_json = get_projects()
    try:
        for project in projects_json:
            print(project)
            print(group_id)
            if project["groups"] == group_id:
                project_name = project["name"]
                group_name = get_groups.get_group_name(group_id)
                logger.info("Project name is " + project_name + "belongs to group " + group_name)
                return project["name"]
            else:
                logger.error(f"Error getting project, status code: {response.status_code}")
            return {}

    except requests.exceptions.RequestException as e:
        logger.exception(f"An error occurred: {e}")
        raise e
#get_projects_by_group('4093787c-d184-4ad7-b9cd-2bc722ef1883')


# as an admin user, GET {{Cx1_IAM}}/auth/admin/realms/{{Cx1_Tenant}}/clients?briefRepresentation=true

# response:
#   {
#       "id":"bc5884f2-19b5-4783-a697-86ca44bab03e",
#       "clientId":"mikek_jenkins_oauth",
#       "surrogateAuthRequired":false,
#       "enabled":true,
#       "alwaysDisplayInConsole":false,
#       "clientAuthenticatorType":"client-secret",
#       "secret":"c9592102-7ac8-4eee-a80b-75e770919a1d",


def print_projects_with_no_groups_or_tags(response):
    output_projects = []

    for project in response['projects']:
        if not project['groups'] and not project['tags']:
            print(project['name'])


all_projects = get_projects()
# print_projects_with_no_groups_or_tags(response)


def print_projects_with_no_groups_or_tags_csv_file(json_response: str, file_path: str) -> None:
    data = json_response
    
    # filter projects with no groups and no tags
    no_groups = [p['name'] for p in data['projects'] if not p['groups']]
    no_tags = [p['name'] for p in data['projects'] if not p['tags']]
    no_groups_no_tags = [p['name'] for p in data['projects'] if not p['groups'] and not p['tags']]
    
    # create CSV file
    with open(file_path + '/projects_with_groups_and_tags.csv', mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Projects without groups', 'Projects without tags', 'Projects without groups and tags'])
        
        # write data to CSV file
        for i in range(max(len(no_groups), len(no_tags), len(no_groups_no_tags))):
            row = []
            
            if i < len(no_groups):
                row.append(no_groups[i])
            else:
                row.append('')
                
            if i < len(no_tags):
                row.append(no_tags[i])
            else:
                row.append('')
                
            if i < len(no_groups_no_tags):
                row.append(no_groups_no_tags[i])
            else:
                row.append('')
                
            writer.writerow(row)
    
    print(f"CSV file written to {file_path}")

# print_projects_with_no_groups_or_tags_csv_file(all_projects, file_path)