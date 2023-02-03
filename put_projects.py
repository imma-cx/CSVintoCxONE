import requests
import logging
import json
import os
import get_projects
import get_groups
from auth import authHeaders_prod

from authentication import Config, account_name, auth_headers
from logging_config import configure_logger, log_path

account = Config.get_account_config(account_name)
server_url = account.get('server_url')
file_path = account.get('file_path')
tenant = account.get('tenant')

from get_groups import get_groups, get_group_name
from get_projects import get_projects, get_project_name

log_path = "logs/"

response = ""
body = ""

projects_json = get_projects(response)
groups_json = get_groups(response)

relative_url = server_url + "/api/projects"



#body expected
# {
#   "name": "Imported2",
#   "groups": [
#     "group"
#   ],
#   "repoUrl": "https://bitbucket.org/what/repo",
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



logger = configure_logger(log_path + 'change_project_group.log')

def change_project_group(project_id, parent_group_id):

    body = {
        "groups": [parent_group_id]
    }

    url = relative_url + "/" + project_id
    response = requests.put(url, headers=auth_headers, json=body)
    if response.status_code == 204:
        try:
            logger.info("Project " + get_project_name(project_id) + " moved to Group " + get_group_name(parent_group_id))
            return response.json()
        except ValueError as e:
            logging.error(f"Error parsing response JSON: {e}")
            return {}
    else:
        logging.error(f"Error updating project, status code: {response.status_code}")
        return {}


logger = configure_logger(log_path + 'move_projects_to_parent_group_sch.log')

def move_projects_to_parent_group_sch(projects_json, groups_json):
    try:
        # Get the list of projects from the json response
        projects = projects_json["projects"]

        # Iterate through the list of projects
        for project in projects:
            project_id = project["id"]
            project_group_ids = project["groups"]
            # Check if the project has a group
            if project_group_ids:
                for project_group_ids in project["groups"]:
                    project_group_name = get_group_name(project_group_ids)

                    # Iterate through the list of groups and get subgroups
                    for group in groups_json:
                        parent_group_id = group["id"]
                        sub_groups = group["subGroups"]
                        # Check if the group has no subGroups and if the end of the group name matches the subGroup name
                        if sub_groups:
                            for sub_group in sub_groups:
                                sub_group_name = sub_group["name"]
                                
                                if project_group_name.endswith(sub_group_name):
                                    change_project_group(project_id, parent_group_id)
                                
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        raise e

move_projects_to_parent_group_sch(projects_json, groups_json)