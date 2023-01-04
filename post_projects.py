import requests
import json

from authHeaders import auth_headers, ast_url

relative_url = ast_url + "/api/projects"

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

def __create_project_set(project):

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

with open("fromCSV_withGroupID.json", 'r') as f:
    data = json.load(f)
    for project in data:
        __create_project_set(project)

