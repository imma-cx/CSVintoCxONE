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
        print(response.json())
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
        print(response.json())
        return response.json()
    except ValueError as e:
        print(f"Error parsing response JSON: {e}")
    return {}

get_proj_queries("f61cfb11-78d1-4b4d-8c9d-20e3ecebadf4")