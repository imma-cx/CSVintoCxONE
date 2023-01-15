#import auth.authHeaders as authHeaders
#import auth.authHeaders_sch as authHeaders_sch
import auth.authHeaders_prod as authHeaders_prod

import requests
import logging
import json
import os

ast_url = authHeaders_prod.server_url_prod
tenant = authHeaders_prod.tenant_prod
auth_headers = authHeaders_prod.auth_headers_prod
file_path = "output/production/"
log_path = "logs/"

#body expected
# {
#   "name": "Imported2",
#   "groups": [
#     "grupo_nao_existe"
#   ],
#   "repoUrl": "https://bitbucket.org/cxtraining/cxql_training_app",
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

relative_url = ast_url + "/api/projects"

#move projects log file
log_file = "project_move.log"
logging.basicConfig(filename=log_file, level=logging.ERROR)

def __move_project_from_group(src_prj_id, dst_group_id):

    body = {
        "groups": [dst_group_id]
    }
    url = relative_url + "/" + src_prj_id
    response = requests.put(url, headers=auth_headers, json=body)
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError as e:
            logging.error(f"Error parsing response JSON: {e}")
            return {}
    else:
        logging.error(f"Error updating project, status code: {response.status_code}")
        return {}