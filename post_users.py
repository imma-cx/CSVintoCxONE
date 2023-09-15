import requests
import json
import csv

from authentication import Config, account_name, auth_headers
from logging_config import configure_logger, log_path

account = Config.get_account_config(account_name)

# change account in authentication.py
iam_url = account.get('iam_url')
tenant = account.get('tenant')
file_path = account.get('file_path')

logger = configure_logger(log_path + 'post_users_' + account_name + '.log')

relative_url = iam_url + "/auth/admin/realms/" + tenant + "/users"


def create_user(group_name):
    url = relative_url
    try:
        response = requests.post(url, json.dumps({"name": group_name}), headers=auth_headers)
        if response.status_code == 201:
            logger.info(f"New Group with name " + group_name + " has been created!")
        elif response.status_code == 409:
            logger.info(f"Group with name " + group_name + " already exists!")
        else:
            logger.error(f'Error: {response.status_code}')
    except requests.exceptions.RequestException as e:
        logger.exception(e)


# {
#   "id": "ccbdc6c1-6943-4798-ac41-8d36b37f112f",
#   "createdTimestamp": 1586521033884,
#   "username": "emanuel_ribeiro_gst",
#   "enabled": true,
#   "totp": true,
#   "emailVerified": true,
#   "firstName": "Emanuel",
#   "lastName": "R",
#   "email": "emanuel.ribeiro@checkmarx.com",
#   "attributes": {
#     "lastLogin": [
#       "2023-09-13T08:40:49.077186Z"
#     ],
#     "country": [],
#     "other": [],
#     "serviceTokenUser": [],
#     "resetOtpRequested": [],
#     "jobTitle": [],
#     "serviceUserTimeoutDays": [],
#     "landingPageData": [],
#     "fingerprints": [
#       "e73f385480748497c1b874c0a1364f2a604f6fadb25c1971d9aca1fcf2bdbe41:7702f04c-4eb6-414d-8430-190a9835dab7",
#       "edc2d799a6c926144d4e816a263e93116f3b549335aecd4d39666b6b9c3f5f06:4558ba56-ac69-4ba0-bd24-9c5f0fbcb573",
#       "863eeb212abeb77aa8b94a5b6d89743a44c16b09dd612e753437984f6e81268b:b23cc4fc-7675-4c05-a339-bb05c5d68ac8",
#       "29ad907282236d61b575460199c3d51249455470926dda6bd888cc9cc31dd597:422be61a-b110-4ff6-ba48-a2ed47a5fdc7"
#     ],
#     "serviceUser": []
#   },
#   "disableableCredentialTypes": [],
#   "requiredActions": [],
#   "federatedIdentities": [],
#   "notBefore": 0,
#   "access": {
#     "manageGroupMembership": true,
#     "view": true,
#     "mapRoles": true,
#     "impersonate": true,
#     "manage": true
#   }
# }