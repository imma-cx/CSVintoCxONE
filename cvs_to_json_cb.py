import csv
import json
import os
import get_groups

from authentication import Config, account_name, auth_headers
from logging_config import configure_logger, log_path

# Change account in authentication.py
account = Config.get_account_config(account_name)
server_url = account.get('server_url')
file_path = 'output/caixabank'
file_path = file_path + '/'
tenant = account.get('tenant')

# CSV file path
csv_file = "data/data.csv"


def from_csv(file):
    f = open(file, 'r')
    # skip the first line of csv file
    next(f)
    # Change each field name to the appropriate name, the first row of the csv file.
    reader = csv.DictReader(
        f,
        delimiter=';',
        fieldnames=(
            "Profile",
            "Groups"
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
    return reader


logger = configure_logger(log_path + 'csv_to_json_' + account_name + '.log')


reader = from_csv(csv_file)


def csv_to_json(reader):
    # read from csv and create json body for API POST
    out = []
    for row in reader:
        item = {}

        item['name'] = row['Profile']
        # use below line for groups from csv file
        # item['groups'] = row['Groups(Team List)'].split(',')

        # use to get group id from the name, directly from API Response in get_groups.py
        item['groups'] = {}
        groups = row['Groups'].split(',')
        for group in groups:
            item['groups'] = [get_groups.get_group_id(group)]
        item['origin'] = 'API'
        item['tags'] = {}

        out.append(item)

    # Parse the CSV into JSON
    outjson = json.dumps(out)

    # Save the JSON
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    f = open(file_path + '/fromCSV_withGroupID_' + account_name + '.json', 'w')
    f.write(outjson)
    logger.info('JSON File Created!\n')



csv_to_json(reader)
