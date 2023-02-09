import requests
import json

from authentication import Config, account_name, auth_headers
from logging_config import configure_logger, log_path

account = Config.get_account_config(account_name)
server_url = account.get('server_url')
file_path = account.get('file_path')

relative_url = server_url + "/api/projects"

#body expected
# {
#   "name": "Imported2",
#   "groups": [
#     "grupo_nao_existe"
#   ],
#   "repoUrl": "https://bitbucket.org/cxtraining/cxql_training_app",
#   "mainBranch": "master",
#   "origin": "API",
#   "tags": {
#     "tag1": "tag1-text",
#     "tag2": "tag2-text"
#   }
# }

logger = configure_logger(log_path + "create_project_set_adidas.log")
# creates projects from the provided json file:
# line below is the default path for the project
#file_path = file_path + '/fromCSV_withGroupID_' + account_name + '.json', 'r'

file_path = 'output/adidas/new_data/fromCSV_withGroupID_canary_latest_canary.json'
def create_project_set(project):

    url=relative_url
    try:
        response = requests.post(url, json.dumps(project), headers=auth_headers)
        name = project['name']
        if response.status_code == 201:
            logger.debug("\n\nNew project with name " + name + " has been created!\n")
            print("New project with name " + name + " has been created!")
        elif response.status_code == 400:
            logger.debug("\n\nError 400: Project with name " + name + " might already exist! Not Created!\n")
            print("Error 400: Project with name " + name + " might already exist! Not Created!")
        elif response.status_code == 504:
            logger.debug("\n\nError 504: Project with name " + name + " not created. API gateway timeout!\n")
            print("Error 504: Project with name " + name + " not created. API gateway timeout!")
        else:
            logger.error(f'Error: {response.status_code} when creating project with name: ' + name + '\n')
            print(f'Error: {response.status_code} when creating project with name: ' + name + '\n')
    except requests.exceptions.RequestException as e:
        logger.error(e)


with open(file_path, 'r') as f:
    data = json.load(f)
    for project in data:
        create_project_set(project)

# create_project_set(project)