import requests
import json
import csv


#from auth.authHeaders import auth_headers, iam_url, tenant
from auth.authHeaders_prod import auth_headers_prod, iam_url_prod, tenant_prod
from logging_config import configure_logger, log_path

# temporary auth management
auth_headers = auth_headers_prod
iam_url = iam_url_prod
tenant = tenant_prod

#group_data = 
logger = configure_logger(log_path + 'post_groups.log')

relative_url = iam_url + "/auth/admin/realms/" + tenant + "/groups"

def __create_group_set(group_data):

    url=relative_url
    try:
        response = requests.post(url, json.dumps(group_data), headers=auth_headers)
        if response.status_code == 201:
            logger.info(f"New Group with Name {json.dumps(group_data)} has been created!")
        else:
            logger.error(f'Error: {response.status_code}')
    except requests.exceptions.RequestException as e:
        logger.exception(e)

# with open("groups.json") as f:
#     data = json.load(f)
#     for group in data:
#         __create_group_set(group)

def __create_sub_group_(sub_group_data, parent_group_id):
        if parent_group_id:
            url = relative_url + "/" + parent_group_id + "/children"
        try:
            response = requests.post(url, json.dumps(sub_group_data), headers=auth_headers)
            if response.status_code == 201:
                logger.info(f"New Subgroup with Name {json.dumps(sub_group_data)} has been created under" + parent_group_id + "!")
            else:
                logger.error(f'Error: {response.status_code}')
        except requests.exceptions.RequestException as e:
            logger.exception(e)


logger = configure_logger(log_path + 'groups_subgroups_create.log')

csv_file1 = "data/schroders/groups_mapping_1sast.csv"

def create_groups_and_subgroups(csv_file):
    groups = {}
    subgroups = {}
    try:
        with open(csv_file, newline='') as file:
            reader = csv.reader(file)
            next(reader)  # skip the header row
            for row in reader:
                group_id, subgroup_name = row
                if group_id not in groups:
                    groups[group_id] = {
                        "name": group_id,
                        "subGroups": []
                    }
                    subgroups[group_id] = []
                subgroups[group_id].append({
                    "name": subgroup_name
                })

        for group_id in groups:
            groups[group_id]["subGroups"] = subgroups[group_id]
            
        groups_json = json.dumps(list(groups.values()))
        subgroups_json = json.dumps(list(subgroups.values()))
        print(groups_json)
        print(subgroups_json)
        
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        raise e
    else:
        logger.info(f"Successfully created groups and subgroups from {csv_file}")
    return groups_json, subgroups_json
    
    
create_groups_and_subgroups(csv_file1)


