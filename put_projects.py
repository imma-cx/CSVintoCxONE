import requests
import logging
import json
import os
import get_projects
import get_groups

#import auth.authHeaders as authHeaders
#import auth.authHeaders_sch as authHeaders_sch
import auth.authHeaders_prod as authHeaders_prod

from logging_config import configure_logger, log_path
from get_groups import get_groups, get_group_name
from get_projects import get_projects, get_project_name

ast_url = authHeaders_prod.server_url_prod
tenant = authHeaders_prod.tenant_prod
auth_headers = authHeaders_prod.auth_headers_prod
file_path = "output/production/"
log_path = "logs/"

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

# Update group, ignores subgroups.
# PUT /{realm}/groups/{id}
# Consumes
# application/json

relative_url = ast_url + "/api/projects"

response = ""

logger = configure_logger(log_path + 'change_project_group.log')


def change_project_group(project_id, parent_group_id):

    body = {
        "groups": [parent_group_id]
    }
    body = json.loads(json.dumps(body))

    url = relative_url + "/" + project_id
    response = requests.put(url, headers=auth_headers, json=body)
    if response.status_code == 200:
        try:
            logger.info("Project " + get_project_name(project_id) + " moved to Group " + get_group_name(parent_group_id))
            return response.json()
        except ValueError as e:
            logging.error(f"Error parsing response JSON: {e}")
            return {}
    else:
        logging.error(f"Error updating project, status code: {response.status_code}")
        return {}



projects_json = get_projects(response)
groups_json = get_groups(response)

logger = configure_logger(log_path + 'move_projects_to_parent_group_sch.log')

def move_projects_to_parent_group_sch(projects_json, groups_json):
    try:
        # Get the list of projects from the json response
        projects = projects_json["projects"]

        # Iterate through the list of projects
        for project in projects:
            project_group ={}
            project_name = project["name"]
            logger.info("Project Name: " + project_name)
            project_id = project["id"]
            logger.info("Project ID: " + project_id)
            project_group = project["groups"]
            if project_group:
                for project_group in project["groups"]:
                    logger.info("Project groups: " + project_group)
                    project_group_name = get_group_name(project_group)

                    # Iterate through the list of groups
                    for group in groups_json:
                        parent_group_name = group["name"]
                        parent_group_id = group["id"]
                        sub_groups = group["subGroups"]
                        if sub_groups:
                            for sub_group in sub_groups:
                                sub_group_id = sub_group["id"]
                                sub_group_name = sub_group["name"]
                                
                                if project_group_name.endswith(sub_group_name):
                                    change_project_group(project_id, parent_group_id)
                                
                            # Check if the group has no subGroups and if the end of the group name matches the subGroup name

    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        raise e

move_projects_to_parent_group_sch(projects_json, groups_json)