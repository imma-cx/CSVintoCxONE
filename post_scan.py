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

relative_url = server_url + "/api/scans"

# {
#   "type": "upload",
#   "handler": {
#     "branch": "string",
#     "commit": "string",
#     "tag": "string",
#     "repoUrl": "string",
#     "credentials": {
#       "username": "string",
#       "type": "apiKey",
#       "value": "string"
#     }
#   },
#   "project": {
#     "id": "string",
#     "tags": {
#       "test": "",
#       "priority": "high"
#     }
#   },
#   "config": [
#     {
#       "type": "sast",
#       "value": {
#         "incremental": "true",
#         "presetName": "Default"
#       }
#     }
#   ],
#   "tags": {
#     "test": "",
#     "priority": "high"
#   }
# }

def new_scan(project_id, scan_type, repo_url, branch, scanners, preset, tags):
    project_name = get_project_name(project_id)
    logger = configure_logger(log_path + 'new_scan_project_' + project_name + '.log')

    body = {
              "type": scan_type,
              "handler": {
                "branch": branch,
                "tag": tags,
                "repoUrl": repo_url
              },
              "project": {
                "id": project_id,
                "tags": {
                    tags
                }
              },
              "config": [
                {
                  "type": "sast",
                  "value": {
                    "incremental": "true",
                    "presetName": preset
                  }
                }
              ],
              "tags": {
                "test": "",
                "priority": "high"
              }
            }

    url = relative_url
    try:
        response = requests.post(url, body, headers=auth_headers)


