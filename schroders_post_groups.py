import requests
import json
import csv
import get_groups

from auth.authHeaders_prod import auth_headers_prod, iam_url_prod, tenant_prod
from logging_config import configure_logger, log_path

# temporary auth management
auth_headers = auth_headers_prod
iam_url = iam_url_prod
tenant = tenant_prod

logger = configure_logger(log_path + 'create_groups_subgroups.log')

# function to create a group
def create_group(group_name):
    url = f"{iam_url}/auth/admin/realms/{tenant}/groups"
    group_data = {
        "name": group_name,
        "realmRoles": [],
        "subGroups": []
    }
    try:
        response = requests.post(url, json=group_data, headers=auth_headers)
        if response.status_code != 201:
            raise ValueError(f"Error creating group {group_name}. Status code: {response.status_code}")
        return response.json()["id"]
    except requests.exceptions.RequestException as e:
        logger.exception(e)

# function to create a subgroup
def create_subgroup(parent_group_id, subgroup_name):
    url = f"{iam_url}/auth/admin/realms/{tenant}/groups/{parent_group_id}/children"
    subgroup_data = {
        "name": subgroup_name
    }
    try:
        response = requests.post(url, json=subgroup_data, headers=auth_headers)
        if response.status_code != 201:
            raise ValueError(f"Error creating subgroup {subgroup_name} under group {parent_group_id}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.exception(e)

def create_groups_and_subgroups(csv_file):
    try:
        with open(csv_file, newline='') as file:
            reader = csv.reader(file)
            next(reader)  # skip the header row
            for row in reader:
                group_name, subgroup_name = row
                create_group(group_name)
                parent_group_id = get_groups.get_group_id(group_name)
                create_subgroup(parent_group_id, subgroup_name)
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        raise e
    else:
        logger.info(f"Successfully created groups and subgroups from {csv_file}")

#csv_file = "data/schroders/groups_mapping_1sast.csv"
create_groups_and_subgroups(csv_file)
