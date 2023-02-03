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

logger = configure_logger(log_path + "create_project_set.log")

def create_project_set(project):

    url=relative_url
    try:
        response = requests.post(url, json.dumps(project), headers=auth_headers)
        if response.status_code == 201:
            name = project['name']
            print("New project with name " + name + " has been created!")
        else:
            print(f'Error: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(e)

with open(file_path + '/fromCSV_withGroupID_' + account_name + '.json', 'r') as f:
    data = json.load(f)
    for project in data:
        create_project_set(project)

