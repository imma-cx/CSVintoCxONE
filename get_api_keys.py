import requests
import json
import os
# import sys

# sys.path.insert(0, os.path.abspath('/'))

from authentication import Config, account_name, auth_headers
from logging_config import configure_logger, log_path

account = Config.get_account_config(account_name)

# change account in authentication.py
iam_url = account.get('iam_url')
tenant = account.get('tenant')
file_path = account.get('file_path')


def get_ast_app_id():
    logger = configure_logger(log_path + 'get_ast_app_id_' + account_name + '.log')
    logger.info('Getting AST app ID')
    url = iam_url + '/auth/admin/realms/' + tenant + '/clients?clientId=ast-app&search=true'
    try:
        response = requests.get(url, headers=auth_headers)
        if response.status_code == 200:
            # from the below response.json() i just want the value of 'id'
            app_id = response.json()[0].get('id')
            return app_id
        else:
            print(f'Error: {response.status_code}')

    except requests.exceptions.RequestException as e:
        print(e)


def get_all_api_keys():
    logger = configure_logger(log_path + 'get_all_api_keys_' + account_name + '.log')
    logger.info('Getting All tenant API Keys')
    app_id = get_ast_app_id()
    url = iam_url + '/auth/admin/realms/' + tenant + '/clients/' + app_id + '/offline-sessions'
    try:
        response = requests.get(url, headers=auth_headers)
        if response.status_code == 200:
            # from the below response.json() i just want the value of 'secret'
            print(response.json())
            app_secret = response.json()[0].get('secret')
            print(app_secret)
        else:
            print(f'Error: {response.status_code}')

    except requests.exceptions.RequestException as e:
        print(e)

