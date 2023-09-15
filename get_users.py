import requests
import json
import os

from authentication import Config, account_name, auth_headers
from logging_config import configure_logger, log_path

account = Config.get_account_config(account_name)

# change account in authentication.py
iam_url = account.get('iam_url')
tenant = account.get('tenant')
file_path = account.get('file_path')

users_url = iam_url + "/auth/admin/realms/" + tenant + "/users"


def get_user(user_id):
    logger = configure_logger(log_path + 'get_user_' + account_name + '.log')
    url = users_url + "/" + user_id
    response = requests.get(url, headers=auth_headers)
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        with open(file_path + '/user.json', 'w') as f:
            json.dump(response.json(), f)
            print('File user.json saved in ' + str(file_path))
        return response.json()

    except ValueError as e:
        logger.exception(f"Error parsing response JSON: {e}")
    return response


def get_users():
    logger = configure_logger(log_path + 'get_users_' + account_name + '.log')
    url = users_url
    response = requests.get(url, headers=auth_headers)
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        with open(file_path + '/all_users.json', 'w') as f:
            json.dump(response.json(), f)
            print('File all_users.json saved in ' + str(file_path))
        return response.json()
    except ValueError as e:
        logger.exception(f"Error parsing response JSON: {e}")
    return response


def get_users_count():
    logger = configure_logger(log_path + 'get_users_count' + account_name + '.log')
    url = users_url + "/count"
    response = requests.get(url, headers=auth_headers)
    try:
        if response.status_code == 200:
            print(f"There are {response.json()} users.")
            return response
        else:
            logger.error(f"Failed to retrieve user list. Status Code: {response.status_code}")
            return None
    except ValueError as e:
        logger.exception(f"Error parsing response JSON: {e}")


def get_username(user_id):
    logger = configure_logger(log_path + 'get_username_' + account_name + '.log')
    url = users_url + "/" + user_id
    response = requests.get(url, headers=auth_headers)
    username = ""
    try:
        if response.status_code == 200:
            user_data = response.json()
            firstname = user_data.get("firstName", "")
            lastname = user_data.get("lastName", "")
            username = user_data.get("username", "")

            if firstname and lastname:
                full_name = f"{firstname} {lastname}"
            else:
                full_name = "Unknown"

            print(f"User with ID {user_id} is named {full_name}. \nUsername: {username}")
            return user_data
        else:
            logger.error(f"Failed to retrieve user data. Status Code: {response.status_code}")
            return None

    except ValueError as e:
        logger.exception(f"Error parsing response JSON: {e}")

    return username


def get_user_id(username):
    logger = configure_logger(log_path + 'get_user_id_' + account_name + '.log')
    try:
        response = get_users()
        if response is not None:
            for user in response:
                if user.get("username") == username:
                    user_id = user.get("id")
                    print(f"The username {username} has the id: {user_id}")
                    return user_id
            # If the username is not found
            logger.info(f"User with username '{username}' not found.")
            return None
        else:
            logger.error(f"Failed to retrieve user list. Status Code: {response}")
            return None

    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        return None


def main():
    get_user("ccbdc6c1-6943-4798-ac41-8d36b37f112f")
    get_users()
    get_username("ccbdc6c1-6943-4798-ac41-8d36b37f112f")
    get_user_id("emanuel_ribeiro_gst")
    get_users_count()

    pass
# end of main


if __name__ == '__main__':

    main()
    exit(0)
