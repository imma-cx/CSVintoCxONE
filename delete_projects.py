import requests
import json
import get_projects

from config import Config
from authentication import account_name, auth_headers, auth_headers
from get_projects import get_projects, get_project_name
from logging_config import configure_logger, log_path

account = Config.get_account_config(account_name)
server_url = account.get('server_url')

logger = configure_logger(log_path + 'delete_project_' + account_name + '.log')

def delete_project(project_id):
    url = server_url + "/api/projects/" + project_id
    if project_id != "":
        project_name = get_project_name(project_id)
        try:
            response = requests.delete(url, headers=auth_headers)
            if response.status_code == 200:
                logger.debug("Project with ID " + project_id + ", named " + project_name + " was deleted!")
            else:
                logger.info("ELSE: project name " + project_name)
                logger.debug(f'Error: {response.status_code}')

            return response

        except requests.exceptions.RequestException as e:
            logger.exception(f"An error occurred: {e}")
            raise e
    else:
        logger.info("No Project ID provided")
#delete_project(project_id)

response = ""
projects_json = get_projects(response)
logger = configure_logger(log_path + 'delete_all_project_' + account_name + '.log')

def delete_all_projects(projects_json):
    try:
        projects = json.loads(json.dumps(projects_json))
        for project in projects["projects"]:
            project_id = project["id"]
            delete_project(project_id)

    except requests.exceptions.RequestException as e:
        logger.exception(f"An error occurred: {e}")
        raise e

#delete_all_projects(projects_json)