import requests
import json
import os

from authentication import Config, account_name, auth_headers
from logging_config import configure_logger, log_path

account = Config.get_account_config(account_name)
server_url = account.get('server_url')
file_path = account.get('file_path')

relative_url = "/api/cx-audit/queries"


import hashlib


def compute_hash(json_obj):
    # Serialize the JSON object as a string and compute its hash
    json_str = json.dumps(json_obj, sort_keys=True)
    hash_obj = hashlib.sha256(json_str.encode())
    return hash_obj.hexdigest()


def get_all_queries2():
    # Set up logging
    logger = configure_logger(log_path + "get_all_queries_" + account_name + ".log")

    # Define the URL to fetch the queries from
    url = server_url + relative_url

    try:
        # Check if the folder for JSON files exists, create if not
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            logger.info(f'Created folder: {file_path}')

        # Check if the JSON file with queries exists
        if os.path.exists(file_path + '/all_queries.json'):
            logger.info(f'File all_queries.json exists (up to date)')

            # Load the existing JSON data from the file
            with open(file_path + '/all_queries.json', 'r') as file:
                json_file_contents = json.load(file)

            # Fetch the latest JSON data from the API
            response = requests.get(url, headers=auth_headers)

            if response.status_code == 200:
                # Compute hashes for both the response and the file contents
                response_hash = compute_hash(response.json())
                file_hash = compute_hash(json_file_contents)

                if response_hash == file_hash:
                    logger.info("JSON response matches the file contents.")
                    print("JSON response matches the file contents.")

                else:
                    logger.info("JSON response differs from the file contents.")
                    print("JSON response differs from the file contents.")
                    # Update the file with the latest JSON data
                    with open(file_path + '/all_queries.json', 'w') as f:
                        json.dump(response.json(), f, indent=4)
                        logger.info(f'File all_queries.json updated in {file_path}')

                return response.json()

        else:
            # Fetch the JSON data from the API
            response = requests.get(url, headers=auth_headers)
            response.raise_for_status()  # Check for HTTP errors

            if response.status_code == 200:
                # Create the file and save the JSON data
                with open(file_path + '/all_queries.json', 'w') as f:
                    json.dump(response.json(), f, indent=4)

                logger.info(f'File all_queries.json created in {file_path}')
                return response.json()

    except requests.exceptions.RequestException as req_err:
        logger.error(f"HTTP request failed: {str(req_err)}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

    return {}

def normalize_json(json_obj):
    # Serialize the JSON object, sort keys, and remove whitespace
    return json.dumps(json_obj, sort_keys=True, separators=(',', ':'))


def get_all_queries3():
    # Set up logging
    logger = configure_logger(log_path + "get_all_queries_" + account_name + ".log")

    # Define the URL to fetch the queries from
    url = server_url + relative_url

    try:
        # Check if the folder for JSON files exists, create if not
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            logger.info(f'Created folder: {file_path}')
            print(f'Created folder: {file_path}')

        # Check if the JSON file with queries exists
        if os.path.exists(file_path + '/all_queries.json'):
            logger.info(f'File all_queries.json exists (up to date)')
            print(f'File all_queries.json exists (up to date)')

            # Load the existing JSON data from the file and normalize it
            with open(file_path + '/all_queries.json', 'r') as file:
                json_file_contents = json.load(file)
                json_file_normalized = normalize_json(json_file_contents)

            # Fetch the latest JSON data from the API and normalize it
            response = requests.get(url, headers=auth_headers)

            if response.status_code == 200:
                response_json = response.json()
                response_json_normalized = normalize_json(response_json)

                # Compare the normalized JSON strings
                if response_json_normalized == json_file_normalized:
                    logger.info("JSON response matches the file contents.")
                    print("JSON response matches the file contents.")
                else:
                    logger.info("JSON response differs from the file contents.")
                    print("JSON response differs from the file contents.")
                    # Update the file with the latest JSON data
                    with open(file_path + '/all_queries.json', 'w') as f:
                        json.dump(response_json, f, indent=4)
                        logger.info(f'File all_queries.json updated in {file_path}')
                        print(f'File all_queries.json updated in {file_path}')

                return response_json

        else:
            # Fetch the JSON data from the API
            response = requests.get(url, headers=auth_headers)
            response.raise_for_status()  # Check for HTTP errors

            if response.status_code == 200:
                response_json = response.json()

                # Create the file, save the JSON data, and normalize it
                with open(file_path + '/all_queries.json', 'w') as f:
                    json.dump(response_json, f, indent=4)

                logger.info(f'File all_queries.json created in {file_path}')
                print(f'File all_queries.json created in {file_path}')
                return response_json

    except requests.exceptions.RequestException as req_err:
        logger.error(f"HTTP request failed: {str(req_err)}")
        print(f"HTTP request failed: {str(req_err)}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")

    return {}


def get_all_queries():
    # Set up logging
    logger = configure_logger(log_path + "get_all_queries_" + account_name + ".log")
    # Define the URL to fetch the queries from
    url = server_url + relative_url
    try:
        # Check if the folder for JSON files exists, create if not
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            logger.info(f'Created folder: {file_path}')

        # Check if the JSON file with queries exists
        if os.path.exists(file_path + '/all_queries.json'):
            logger.info(f'File all_queries.json exists (up to date)')

            # Load the existing JSON data from the file
            with open(file_path + '/all_queries.json', 'r') as file:
                json_file_contents = json.load(file)

            # Fetch the latest JSON data from the API
            response = requests.get(url, headers=auth_headers)

            if response.status_code == 200:
                # Serialize both JSON objects before comparison
                response_json_str = json.dumps(response.json(), sort_keys=True)
                file_json_str = json.dumps(json_file_contents, sort_keys=True)

                if response_json_str == file_json_str:
                    logger.info("JSON response matches the file contents.")

                else:
                    logger.info("JSON response differs from the file contents.")

                    # Update the file with the latest JSON data
                    with open(file_path + '/all_queries.json', 'w') as f:
                        json.dump(response.json(), f)
                        logger.info(f'File all_queries.json updated in {file_path}')


                return response.json()

        else:
            # Fetch the JSON data from the API
            response = requests.get(url, headers=auth_headers)
            response.raise_for_status()  # Check for HTTP errors

            if response.status_code == 200:
                # Create the file and save the JSON data
                with open(file_path + '/all_queries.json', 'w') as f:
                    json.dump(response.json(), f)

                logger.info(f'File all_queries.json created in {file_path}')
                return response.json()

    except requests.exceptions.RequestException as req_err:
        logger.error(f"HTTP request failed: {str(req_err)}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

    return {}


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


def alter_query_path(query_path):
    if query_path is not None:
        query_path = query_path.replace("/", "%2F")
        query_path = query_path.replace(" ", "%20")
        return query_path


def alter_query_path_back(query_path):
    if query_path is not None:
        query_path = query_path.replace("%2F", "/")
        query_path = query_path.replace("%20", " ")
        return query_path


def get_corp_query_details(query_name):
    logger = configure_logger(log_path + "get_corp_query_details_" + account_name + ".log")
    queries_data = get_all_queries()
    if queries_data is not None:
        for query in queries_data:
            data_query_name = query["name"]
            if data_query_name == query_name:
                query_path = query["path"]
                query_path_fixed = alter_query_path(query_path)
                url = server_url + relative_url + "/Corp/" + query_path_fixed
                response = requests.get(url, headers=auth_headers)
                try:
                    logger.info('Queries Corp Details retrieved')
                    return response.json()
                except ValueError as e:
                    print(f"Error parsing response JSON: {e}")
                return {}


def get_corp_query_details_from_path(query_path):
    logger = configure_logger(log_path + "get_corp_query_details_" + account_name + ".log")
    queries_data = get_all_queries()
    if queries_data is not None:
        for query in queries_data:
            data_query_path = query["path"]
            if data_query_path == query_path:
                query_path = query["path"]
                query_path_fixed = alter_query_path(query_path)
                url = server_url + relative_url + "/Corp/" + query_path_fixed
                response = requests.get(url, headers=auth_headers)
                try:
                    logger.info('Queries Corp Details from path provided, retrieved')
                    return response.json()
                except ValueError as e:
                    print(f"Error parsing response JSON: {e}")
                return {}


def get_all_queries_to_json():
    queries = get_all_queries()
    queries_json = json.dumps(queries)
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
    queries_json = json.dumps(queries)
    if queries_json is None:
        print("Error parsing response JSON")
        return
    else:
        with open(file_path + "/project_" + project_id + "_queries.json", "w") as outfile:
            outfile.write(queries_json)
    print("File project_queries.json created in " + file_path + " folder")
    return queries_json


def get_query_to_json(query_id):
    queries = get_all_queries()
    queries_json = json.dumps(queries)
    if queries_json is None:
        print("Error parsing response JSON")
        return
    else:
        for query in queries:
            if query.get('Id') == query_id:
                query_json = json.dumps(query)
                # with open(file_path + "/query_" + query_id + ".json", "w") as outfile:
                #     outfile.write(query_json)
                #     print("File query_" + query_id + ".json created in " + file_path + " folder")
                return query_json


def get_query_name(query_id):
    queries = get_all_queries()
    for query in queries:
        if query.get('Id') == query_id:
            print("test: " + query.get('name'))
            return query.get('name')
    return None


def get_query_path(query_id):
    queries = get_all_queries()
    for query in queries:
        if query.get('Id') == query_id:
            return query.get('path')
    return None


def get_query_group(query_id):
    queries = get_all_queries()
    for query in queries:
        if query.get('Id') == query_id:
            return query.get('group')
    return None


def get_query_language(query_id):
    queries = get_all_queries()
    for query in queries:
        if query.get('Id') == query_id:
            return query.get('lang')
    return None


def get_query_level(query_id):
    queries = get_all_queries()
    for query in queries:
        if query.get('Id') == query_id:
            return query.get('level')
    return None


def get_query_id(query_name):
    queries = get_all_queries()
    for query in queries:
        if query.get('name') == query_name:
            return query.get('Id')
    return None


def find_all_language_query_info(query_name):
    all_queries = get_all_queries()
    existing_queries = set()  # To keep track of queries already written to the file

    with open(file_path + "/find_all_language_query_info_" + query_name + ".txt", "a") as outfile:
        for query in all_queries:
            if query.get('name') == query_name:
                query_id = query.get('Id')
                query_lang = query.get('lang')
                query_group = query.get('group')
                query_path = query.get('path')
                query_level = query.get('level')

                # Create a unique identifier for the query based on its properties
                query_identifier = f"{query_name}_{query_id}_{query_lang}_{query_group}_{query_path}_{query_level}"

                # Debugging output to identify duplicates
                if query_identifier in existing_queries:
                    print(f"Duplicate found: {query_identifier}")

                # Check if the query information has already been written
                if query_identifier not in existing_queries:
                    outfile.write(f"Query Name: {query_name}\n"
                                  f"Query ID: {query_id}\n"
                                  f"Query Language: {query_lang}\n"
                                  f"Query Group: {query_group}\n"
                                  f"Query Level: {query_level}\n"
                                  f"Query Path: {query_path}\n"
                                  f"______________________________________________________________________\n\n")

                    # Add the query identifier to the set of existing queries
                    existing_queries.add(query_identifier)

    print("File find_all_language_query_info_" + query_name + ".txt created in " + file_path + " folder")
    return None


def same_query_in_multi_languages_to_json(query_name):
    all_queries = get_all_queries()
    same_name_queries_json = []
    for query in all_queries:
        if query.get('name') == query_name:
            query_id = get_query_id(query_name)
            query_data = get_query_to_json(query_id)
            query_json = json.dumps(query_data)
            same_name_queries_json.append(json.loads(query_json))
    return same_name_queries_json


def get_all_corp_overrides():
    logger = configure_logger(log_path + "get_all_corp_overrides_" + account_name + ".log")
    all_queries = get_all_queries()
    corp_queries = []
    with open(file_path + "/all_corp_queries.json", "w") as outfile:
        # check for existing override in corp
        for query in all_queries:
            query_level = query.get('level')
            if query_level == "Corp":
                corp_queries.append(query)
        logger.info(f"File all_corp_queries.json created in {file_path}.")
        print(f"File all_corp_queries.json created in {file_path}.")
        json.dump(corp_queries, outfile)
        return corp_queries


def get_all_corp_overrides_by_name(query_name):
    logger = configure_logger(log_path + "get_all_corp_overrides_by_name_" + account_name + ".log")
    all_queries = get_all_queries()
    corp_queries = []
    # check for existing override in corp
    for query in all_queries:
        query_level = query.get('level')
        if query_level == "Corp":
            if query.get('name') == query_name:
                corp_queries.append(query)
                logger.info(f"Corp Queries List: \n {corp_queries}")
    return corp_queries


def get_all_corp_queries_by_severity(severity):
    logger = configure_logger(log_path + "get_all_corp_queries_by_severity_" + account_name + ".log")
    all_corp_queries = get_all_corp_overrides()
    corp_queries = []
    # check for existing override in corp
    for query in all_corp_queries:
        query_path = query.get('path')
        query_details = get_corp_query_details_from_path(query_path)
        query_level = query.get('level')
        if query_level == "Corp":
            if query_details.get('severity') == severity:
                corp_queries.append(query)
                logger.info(f"Corp Queries with severity {severity}\n"
                            f"List: \n {corp_queries}")
                print(f"Corp Queries with severity {severity}\nList: \n {corp_queries}")

    return corp_queries


def get_all_query_info_from_preset():
    url = server_url + "/api/presets/queries"
    response = requests.get(url, headers=auth_headers)
    response.raise_for_status()  # Check for HTTP errors
    print(response.json())
    return response.json()


def main():

    #get_all_queries()
    #get_all_queries_to_json()
    #get_project_queries_to_json("79a84680-2cdc-45b3-b65a-55af30c9b80a")
    #get_proj_queries("79a84680-2cdc-45b3-b65a-55af30c9b80a")
    #get_corp_query_details("Log_Forging")
    #get_query_to_json("8563796974311953488")
    #same_query_in_multi_languages_to_json("Use_Of_Hardcoded_Password")
    #print(get_corp_query_details("Log_Forging"))
    #get_all_corp_overrides_by_name("Log_Forging")
    #get_all_corp_queries_by_severity(3)
    #find_all_language_query_info("Log_Forging")
    #get_all_query_info_from_preset()
    get_all_corp_overrides()

    pass


if __name__ == '__main__':

    main()
    exit(0)

