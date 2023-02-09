import csv
import json
import os
import get_groups

from authentication import Config, account_name, auth_headers
from logging_config import configure_logger, log_path

# Change account in authentication.py
account = Config.get_account_config(account_name)
server_url = account.get('server_url')
file_path = 'output/adidas'
file_path = file_path + '/new_data'
tenant = account.get('tenant')

# CSV file path
file = "data/adidas/adidas_data.csv"

f = open(file, 'r')

# skip the first line of csv file
next(f)

# Change each field name to the appropriate name, the first row of the csv file.
reader = csv.DictReader( 
    f, 
    delimiter=';', 
    fieldnames = (
            "LeanixId",
            "Profile",
            "ProductName",
            "ProductDomain",
            "ProductArea",
            "Assignee",
            "SecurityChampion",
            "isMostCritical",
            "isInternetExposed",
            "SPE",
            "Groups(Team List)",
            "Project Created (Y/N)",
            "Initial assessment (Threat modelling) (Y/N)",
            "Initial Optimization (Y/N)",
            "Migration Finalized (Y/N)"
        ))


# read from csv file and creates json in format to create CxONE Projects with the mapped 
# designated csv first row fields as project tags in the following format:
# [
#     {
#         "name": "cdp_config_server",
#         "groups": [
#             "7ab7bc0f-7d0d-4f2e-9715-7129b52500c9"
#         ],
#         "origin": "API",
#         "tags": {
#             "feedback-app-LeanIX ID": "8f7c9200-58e5-4b19-8317-a660666ecfea",
#             "feedback-Custom-2": "Consumer&CustomerExperience",
#             "feedback-Custom-1": "ConsumerEngagement",
#             "feedback-Assignee": "Jon.Doe@test.com",
#             "SecurityChampion": "Jon.Doe@test.com",
#             "feedback-Custom-7": "Most_Critical",
#             "feedback-Custom-5": "None"
#         }
#     }
# ]


logger = configure_logger(log_path + 'csv_to_json_' + account_name + '.log')
def csv_to_json(reader):
    try:
        # read from csv and create json body for API POST
        out = []
        for row in reader:
            item =  {}
            item['name'] = row['Profile']

            # use below line for groups from csv file
            #item['groups'] = row['Groups(Team List)'].split(',')

            # use to get group id from the name, directly from API Response in get_groups.py
            item['groups'] = {}
            groups = row['Groups(Team List)'].split(',')
            for group in groups:
                item['groups'] = [get_groups.get_group_id(group) for group in groups]
            item['origin'] = 'API'

            # creates tag mapping key:value
            item['tags'] = {}
            if row['LeanixId']:
                item['tags']['feedback-LeanIX ID'] = row['LeanixId']
            if row['ProductName']:
                item['tags']['ProductName'] = row['ProductName']
            if row['ProductDomain']:
                item['tags']['feedback-Custom-2'] = row['ProductDomain']
            if row['ProductArea']:
                item['tags']['feedback-Custom-1'] = row['ProductArea']
            if row['Assignee']:
                item['tags']['feedback-Assignee'] = row['Assignee']
            if row['SecurityChampion']:
                item['tags']['SecurityChampion'] = row['SecurityChampion']            
            if row['isMostCritical']:
                item['tags']['feedback-Custom-7'] = row['isMostCritical']
            if row['isInternetExposed']:
                item['tags']['feedback-Custom-5'] = row['isInternetExposed']

            out.append(item)

        # Parse the CSV into JSON
        outjson = json.dumps(out)

        # Save the JSON
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        f = open(file_path + '/fromCSV_withGroupID_' + account_name + '_latest_canary.json', 'w')
        f.write(outjson)
        logger.info('JSON File Created!\n')
            
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        raise e

csv_to_json(reader)

# get groups from csv file. collumn with heather: Groups(Team List)
# Output: groups.json       - all unique groups
#         all_groups.json   - all groups including duplicates
logger = configure_logger(log_path + 'get_groups_json_' + account_name + '.log')
def get_groups_json(reader):
    try:
        # get all groups (including duplicates)
        out = []
        for row in reader:
            item =  {}
            item['name'] = row['Groups(Team List)']

            out.append(item)

        outjson = json.dumps(out)

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        f = open(file_path + '/all_groups.json','w')
        f.write(outjson)

        # get's unique groups names in json format
        data = json.loads(outjson)
        group_out = ''
        groups = []
        for d in data:
            for group in d['name'].split(','):
                groups.append(group.strip())
                unique_groups = set(groups)

                groupout = [{'name': item} for item in unique_groups]

            group_out = json.dumps(groupout)

        if not os.path.exists(file_path):
            os.makedirs(file_path)
        f = open(file_path + '/groups.json', 'w')
        f.write(group_out)
        f.close

    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        raise e
    
# get_groups_json(reader)

file = 'output/adidas/new_data/groups.json'
def count_groups_from_file(file):
    with open(file, 'r') as f:
        json_input = json.load(f)

    groups = set()
    for item in json_input:
        name = item.get('name')
        if name:
            groups.add(name)

    print(f"Number of groups found: {len(groups)}")

# count_groups_from_file(file)

# counts the number of projects in the provided json (just for confirmation)
file_path = 'output/adidas/new_data/fromCSV_withGroupID_canary.json'
def count_projects_from_file(file_path):
    with open(file_path, 'r') as f:
        json_input = json.load(f)

    projects = set()
    for item in json_input:
        name = item.get('name')
        if name:
            projects.add(name)

    print(f"Number of projects found: {len(projects)}")

# count_projects_from_file(file_path)

# check duplicates in csv file given a collumn name (for confirmation)
# 1 duplicates found: digital-comms-double-opt-in-consumer

file_path = 'data/adidas/adidas_data.csv'
def check_duplicates(file_path, column_name):
    # Create a set to hold unique values
    unique_values = set()

    # Create a list to hold duplicate values
    duplicate_values = []

    # Open the CSV file and read its contents into a list of dictionaries
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            # Get the value of the specified column for the current row
            value = row.get(column_name)

            # If the value exists, check if it's already in the unique values set
            if value:
                if value in unique_values:
                    # If the value is a duplicate, add it to the list of duplicate values
                    duplicate_values.append(value)
                else:
                    # If the value is not a duplicate, add it to the unique values set
                    unique_values.add(value)

    # Print the number of unique values found in the specified column
    print(f"Number of unique values in column '{column_name}': {len(unique_values)}")

    if duplicate_values:
        # If there are duplicate values, print them and the number of duplicates found
        num_duplicates = len(duplicate_values)
        duplicates_str = ', '.join(duplicate_values)
        print(f"{num_duplicates} duplicates found: {duplicates_str}")
    else:
        # If there are no duplicate values, print a message saying so
        print("No duplicates found in the specified column.")
column_name = 'Profile'
#check_duplicates(file_path, column_name)