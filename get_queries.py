import requests
import json
import os
import csv

from authentication import Config, account_name, auth_headers
from logging_config import configure_logger, log_path


account = Config.get_account_config(account_name)
server_url = account.get('server_url')
file_path = account.get('file_path')

relative_url = "/api/cx-audit/queries"


def get_proj_queries(project_id):
    logger = configure_logger(log_path + "get_proj_queries_" + project_id + "_" + account_name + ".log")
    url = server_url + relative_url + "?projectId=" + project_id
    response = requests.get(url, headers=auth_headers)
    try:
        logger.info('Queries list retrieved')
        return response.json()
    except ValueError as e:
        print(f"Error parsing response JSON: {e}")
    return {}


def get_all_queries():
    logger = configure_logger(log_path + "get_all_queries_" + account_name + ".log")
    url = server_url + relative_url
    response = requests.get(url, headers=auth_headers)
    try:
        logger.info('Queries list retrieved')
        return response.json()
    except ValueError as e:
        print(f"Error parsing response JSON: {e}")
    return {}


def get_all_queries_to_json():
    queries = get_all_queries()
    queries_json = json.dumps(queries, indent=4)
    if queries_json is None:
        print("Error parsing response JSON")
        return
    else:
        with open(file_path + "/all_queries.json", "w") as outfile:
            outfile.write(queries_json)
    print("File all_queries.json created in " + file_path + " folder")
    return queries_json


def get_project_queries_to_json(project_id):
    queries = get_proj_queries(project_id)
    queries_json = json.dumps(queries, indent=4)
    if queries_json is None:
        print("Error parsing response JSON")
        return
    else:
        with open(file_path + "/project_" + project_id + "_queries.json", "w") as outfile:
            outfile.write(queries_json)
    print("File project_queries.json created in " + file_path + " folder")
    return queries_json


def main():

    get_all_queries_to_json()

    get_project_queries_to_json("79a84680-2cdc-45b3-b65a-55af30c9b80a")

    get_proj_queries("79a84680-2cdc-45b3-b65a-55af30c9b80a")

    pass


if __name__ == '__main__':

    main()
    exit(0)