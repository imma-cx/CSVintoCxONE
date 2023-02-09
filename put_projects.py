import requests
import logging
import json
import random

from authentication import Config, account_name, auth_headers
from logging_config import configure_logger, log_path
from get_groups import get_group_name, get_group_id
from get_projects import get_projects, get_project_name, get_project, get_project_id
from post_groups import create_group

account = Config.get_account_config(account_name)
server_url = account.get('server_url')
file_path = account.get('file_path')
tenant = account.get('tenant')

# projects_json var with all the tenant projects
projects_json = get_projects()
# projects_json_file var path to json file with the projects details to update
projects_json_file = 'output/adidas/new_data/fromCSV_withGroupID_adidas_latest.json'
relative_url = server_url + "/api/projects"


def change_project_group(project_id, parent_group_id):
    logger = configure_logger(log_path + 'change_project_group.log')

    # Check if the projects_json is empty
    if not projects_json:
        logger.info("No projects found")
        return {}

    # Check if the groups_json is empty
    if not parent_group_id:
        logger.info("No parent groups found")
        return {}

    body = {
        "groups": [parent_group_id]
    }

    url = relative_url + "/" + project_id
    response = requests.put(url, headers=auth_headers, json=body)
    if response.status_code == 204:
        try:
            logger.info(
                "Project " + get_project_name(project_id) + " moved to Group " + get_group_name(parent_group_id))
            return response.json()
        except ValueError as e:
            logging.error(f"Error parsing response JSON: {e}")
            return {}
    else:
        logging.error(f"Error updating project, status code: {response.status_code}")
        return {}


def move_projects_to_parent_group_sch(projects_json, groups_json):
    logger = configure_logger(log_path + 'move_projects_to_parent_group_sch.log')

    # Check if the projects_json is empty
    if not projects_json:
        logger.info("No projects found")
        return {}

    # Check if the groups_json is empty
    if not groups_json:
        logger.info("No groups found")
        return {}

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


def clear_all_projects_tags(projects_json):
    logger = configure_logger(log_path + 'clear_all_projects_tags_' + account_name + '.log')

    for project in projects_json["projects"]:
        project_id_tenant = project['id']
        project_groups_tenant = project['groups']
        project_repourl_tenant = project['repoUrl']
        project_mainbranch_tenant = project['mainBranch']
        project_origin_tenant = project['origin']
        project_criticality_tenant = project['criticality']

        body = {
            "groups": project_groups_tenant,
            "tags": {},
            "repoUrl": project_repourl_tenant,
            "mainBranch": project_mainbranch_tenant,
            "origin": project_origin_tenant,
            "criticality": project_criticality_tenant,
        }
        url = relative_url + '/' + project_id_tenant
        response = requests.put(url, headers=auth_headers, json=body)
        if response.status_code == 204:
            print("Project " + get_project_name(project_id_tenant) + " tags removed!")
            logger.info("Project " + get_project_name(project_id_tenant) + " tags removed!")
        else:
            logging.error(f"Error updating project, status code: {response.status_code}")

# clear_all_projects_tags(projects_json)

def clear_all_projects_groups(projects_json):
    logger = configure_logger(log_path + 'clear_all_projects_groups_' + account_name + '.log')

    for project in projects_json["projects"]:
        project_id_tenant = project['id']
        project_tags_tenant = project['tags']
        project_repourl_tenant = project['repoUrl']
        project_mainbranch_tenant = project['mainBranch']
        project_origin_tenant = project['origin']
        project_criticality_tenant = project['criticality']

        body = {
            "groups": [],
            "tags": project_tags_tenant,
            "repoUrl": project_repourl_tenant,
            "mainBranch": project_mainbranch_tenant,
            "origin": project_origin_tenant,
            "criticality": project_criticality_tenant,
        }

        url = relative_url + '/' + project_id_tenant
        response = requests.put(url, headers=auth_headers, json=body)
        if response.status_code == 204:
            print("Project " + get_project_name(project_id_tenant) + " groups removed!")
            logger.info("Project " + get_project_name(project_id_tenant) + " groups removed!")
        else:
            logging.error(f"Error updating project, status code: {response.status_code}")


# clear_all_projects_groups(projects_json)

def update_projects(projects_json_file):
    logger = configure_logger(log_path + 'update_projects_' + account_name + '_final.log')

    with open(projects_json_file, 'r') as f:
        projects = json.load(f)

    for project_file in projects:
        project_name_file = project_file['name']
        project_group_file = project_file['groups']
        project_tags_file = project_file['tags']
        project_id = get_project_id(project_name_file)
        if project_id:
            project = get_project(project_id).json()

            project_id_tenant = project['id']
            project_name_tenant = project['name']
            project_groups_tenant = project['groups']
            project_tags_tenant = project['tags']
            project_repourl_tenant = project['repoUrl']
            project_mainbranch_tenant = project['mainBranch']
            project_origin_tenant = project.get('origin', '')  # added line to check if 'origin' field exists
            project_criticality_tenant = project['criticality']

        else:
            print(f"Project {project_name_file} not found in tenant!")
            logger.error(f"Project {project_name_file} not found in tenant!")
            continue

        # When there are changes to Groups and Tags
        if project_name_file == project_name_tenant \
                and project_groups_tenant != project_group_file \
                and project_tags_tenant != project_tags_file \
                or project_groups_tenant == '' \
                or project_tags_tenant == '':

            groups_final = []
            tags_final = {}
            for tag_key, tag_value in project_tags_tenant.items():
                if tag_key in project_tags_file:
                    if tag_value != project_tags_file[tag_key]:
                        logger.info(
                            f"Tag value mismatch for key '{tag_key}': '{tag_value}' (project) vs '{project_tags_file[tag_key]}' (file)")
                    tags_final[tag_key] = tag_value
                else:
                    tags_final[tag_key] = tag_value

            for tag_key, tag_value in project_tags_file.items():
                if tag_key not in tags_final:
                    tags_final[tag_key] = tag_value

            for group_tenant in project_groups_tenant:
                if group_tenant not in groups_final:
                    groups_final.append(group_tenant)
            for group_file in project_group_file:
                if group_file not in groups_final:
                    groups_final.append(group_file)

            body = {
                "groups": groups_final,
                "tags": tags_final,
                "repoUrl": project_repourl_tenant,
                "mainBranch": project_mainbranch_tenant,
                "origin": project_origin_tenant,
                "criticality": project_criticality_tenant,
            }

            # log the body for later verification
            logger.info("The following JSON payload will be sent in Project with name: " + project_name_tenant)
            logger.info(json.dumps(body, indent=4))

            # Prompt the user to confirm
            # confirmation = input("Do you want to proceed? (y/n): ")
            confirmation = "y"
            if confirmation.lower() == "y":
                # Proceed with the request
                url = relative_url + "/" + project_id_tenant
                response = requests.put(url, headers=auth_headers, json=body)
                if response.status_code == 204:
                    try:
                        print(f"Project {get_project_name(project_id_tenant)} groups and tags updated!")
                        logger.info(f"\nProject {get_project_name(project_id_tenant)} groups and tags updated!")
                    except ValueError as e:
                        logging.error(f"Error parsing response JSON: {e}")
                else:
                    logging.error(f"Error updating project, status code: {response.status_code}")
            else:
                print("Request cancelled.")

# update_projects(projects_json_file)


def add_random_groups_to_projects(projects_json):
    logger = configure_logger(log_path + 'add_random_groups_to_projects_' + account_name + '.log')

    for project in projects_json["projects"]:
        project_id = project['id']
        project_groups = project['groups']
        project_tags = project['tags']
        project_repourl = project['repoUrl']
        project_mainbranch = project['mainBranch']
        project_origin = project['origin']
        project_criticality = project['criticality']

        # Generate a list of random group names
        num_groups = random.randint(1, 5)  # Randomly select a number of groups to add
        groups = []
        for i in range(num_groups):
            group_name = f"group_{i}"
            create_group(group_name)  # Create a new group with the given name
            group_id = get_group_id(group_name)  # Retrieve the ID of the newly created group

            groups.append(group_id)
        groups.append(project_groups)

        # Update the project body to include the random groups
        body = {
            "groups": groups,
            "tags": project_tags,
            "repoUrl": project_repourl,
            "mainBranch": project_mainbranch,
            "origin": project_origin,
            "criticality": project_criticality,
        }

        print(f"body: \n{body}")

        url = relative_url + '/' + project_id
        response = requests.put(url, headers=auth_headers, json=body)
        if response.status_code == 204:
            print("Random groups added to project " + get_project_name(project_id) + "!")
            logger.info("Random groups added to project " + get_project_name(project_id) + "!")
        else:
            logging.error(f"Error updating project, status code: {response.status_code}")

# add_random_groups_to_projects(projects_json)


def add_random_tags_to_projects(projects_json):
    logger = configure_logger(log_path + 'add_random_tags_to_projects_' + account_name + '.log')

    for project in projects_json["projects"]:
        print(f"project: \n{project}")
        project_id = project['id']
        project_groups = project['groups']
        project_tags = project['tags']
        project_repourl = project['repoUrl']
        project_mainbranch = project['mainBranch']
        project_criticality = project['criticality']

        # Generate a list of random tag names
        num_tags = random.randint(1, 5)  # Randomly select a number of tags to add
        tags = {}
        for i in range(num_tags):
            tag_name = f"tag_{i}"
            tag_value = f"value_{i}"
            tags[tag_name] = tag_value

        #concatenate tags and project_tags
        tags.update(project_tags)

        # Update the project body to include the random tags
        body = {
            "groups": project_groups,
            "tags": tags,
            "repoUrl": project_repourl,
            "mainBranch": project_mainbranch,
            "criticality": project_criticality,
        }

        print(f"body: \n{body}")

        url = relative_url + '/' + project_id
        response = requests.put(url, headers=auth_headers, json=body)
        if response.status_code == 204:
            print("Random tags added to project " + get_project_name(project_id) + "!")
            logger.info("Random tags added to project " + get_project_name(project_id) + "!")
        else:
            logging.error(f"Error updating project, status code: {response.status_code}")

# add_random_tags_to_projects(projects_json)

# Delete random groups from projects
def delete_random_groups(projects_json):
    logger = configure_logger(log_path + 'delete_random_groups_' + account_name + '.log')

    for project in projects_json["projects"]:
        project_id = project['id']
        project_tags = project['tags']
        project_repourl = project['repoUrl']
        project_mainbranch = project['mainBranch']
        project_origin = project['origin']
        project_criticality = project['criticality']

        groups = project.get('groups', [])  # Get existing groups or empty list
        if not groups:
            print(f"No groups to delete in project {get_project_name(project_id)}")
            continue

        # Delete a random number of groups, between 1 and the total number of groups
        num_groups_to_delete = random.randint(1, len(groups))
        groups_to_delete = random.sample(groups, num_groups_to_delete)

        # Remove selected groups from the list
        for group in groups_to_delete:
            groups.remove(group)

        body = {
            "groups": groups,
            "tags": project_tags,
            "repoUrl": project_repourl,
            "mainBranch": project_mainbranch,
            "origin": project_origin,
            "criticality": project_criticality,
        }

        url = relative_url + '/' + project_id
        response = requests.put(url, headers=auth_headers, json=body)
        if response.status_code == 204:
            print(f"{num_groups_to_delete} group(s) deleted from project {get_project_name(project_id)}")
            logger.info(f"{num_groups_to_delete} group(s) deleted from project {get_project_name(project_id)}")
        else:
            logging.error(f"Error updating project, status code: {response.status_code}")

# delete_random_groups(projects_json)


def delete_all_groups_from_random_projects():
    logger = configure_logger(log_path + 'delete_all_projects_groups_' + account_name + '.log')

    # Select a random subset of projects
    num_projects_to_delete_groups = random.randint(1, len(projects_json["projects"]))
    projects_to_delete_groups = random.sample(projects_json["projects"], num_projects_to_delete_groups)

    # Delete all groups from selected projects
    for project in projects_to_delete_groups:
        project_id_tenant = project['id']
        project_tags_tenant = project['tags']
        project_repourl_tenant = project['repoUrl']
        project_mainbranch_tenant = project['mainBranch']
        project_origin_tenant = project['origin']
        project_criticality_tenant = project['criticality']

        body = {
            "groups": [],
            "tags": project_tags_tenant,
            "repoUrl": project_repourl_tenant,
            "mainBranch": project_mainbranch_tenant,
            "origin": project_origin_tenant,
            "criticality": project_criticality_tenant,
        }

        url = relative_url + '/' + project_id_tenant
        response = requests.put(url, headers=auth_headers, json=body)
        if response.status_code == 204:
            print(f"All groups deleted from project {get_project_name(project_id_tenant)}")
            logger.info(f"All groups deleted from project {get_project_name(project_id_tenant)}")
        else:
            logging.error(f"Error updating project, status code: {response.status_code}")

# delete_all_groups_from_random_projects()