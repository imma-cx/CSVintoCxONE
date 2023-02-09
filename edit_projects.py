import requests
import json

from authentication import Config, account_name, auth_headers
from logging_config import configure_logger, log_path
from get_projects import get_projects

account = Config.get_account_config(account_name)
server_url = account.get('server_url')
file_path = account.get('file_path')
response = ""

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

logger = configure_logger(log_path + "edit_projetcs_" + account_name + ".log")

projects = get_projects(response)

def edit_project(project):
    repo_url_tag = project.get("tags", {}).get("RepoURL", None)
    project_repo_url = project.get("repoUrl", None)

    if repo_url_tag and not project_repo_url:
        project['repoUrl'] = repo_url_tag
        url = server_url + "/api/projects/" + project['id']

        try:
            response = requests.put(url, json.dumps(project), headers=auth_headers)
            if response.status_code == 200:
                logger.info(f"Successfully updated project {project['id']} with repo URL {repo_url_tag}")
            else:
                logger.error(f"Failed to update project {project['id']} with repo URL {repo_url_tag}. Response: {response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException caught while updating project {project['id']} with repo URL {repo_url_tag}. Exception: {str(e)}")
    else:
        if not repo_url_tag:
            logger.warning(f"RepoUrl tag not found in project {project['id']}")
        if project_repo_url:
            logger.warning(f"Project {project['id']} already has a repo URL set: {project_repo_url}")

for project in projects['projects']:
    edit_project(project)



