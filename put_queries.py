import requests
import json

from authentication import Config, account_name, auth_headers
from logging_config import configure_logger, log_path
from get_queries import same_query_in_multi_languages_to_json, get_corp_query_details, get_all_corp_overrides_by_name


account = Config.get_account_config(account_name)
server_url = account.get('server_url')
file_path = account.get('file_path')

relative_url = "/api/cx-audit/queries"


# def check_existent_corp_override(query_name):
#     all_queries = get_all_queries()
#     corp_queries = []
#     # check for existing override in corp
#     for query in all_queries:
#         if query.get('name') == query_name:
#             query_level = query.get('level')
#             if query_level == "Corp":
#                 # print(f"Query {query_name} already exists in Corp level")
#                 corp_queries.append(query)
#                 # print(f"existent corp queries: {corp_queries}")
#                 return corp_queries


def change_query_severity_corp_all_languages(query_name, new_severity):
    logger = configure_logger(log_path + 'change_query_severity_corp_all_languages_' + account_name + '.log')
    same_name_queries = same_query_in_multi_languages_to_json(query_name)
    existent_corp_overrides = get_all_corp_overrides_by_name(query_name)
    existent_queries_paths = []
    # handling existing overrides in Corp level
    for existent_query in existent_corp_overrides:
        existent_query_path = existent_query.get('path')
        existent_queries_paths.append(existent_query_path)

    for query in same_name_queries:
        existent_queries_paths = []
        query_json = json.loads(query)
        query_data = get_corp_query_details(query_json.get('name'))
        query_path = query_json.get('path')

        if query_data is not None and query_path not in existent_queries_paths:
            query_severity = query_data.get('Severity')

            if query_severity != new_severity:
                url = server_url + relative_url + "/Corp"
                query_path = query_data.get('Path')
                query_data = [{
                    'name': query_name,
                    'path': query_data.get('Path'),
                    'metadata': {
                        'severity': new_severity
                    },
                    'source': 'result = base.' + query_name + '();'
                }]

                try:
                    print(f"query data: \n{query_data}\n\n")
                    response = requests.put(url, headers=auth_headers, json=query_data)
                    print(f"response status code: {response.status_code}")
                    response.raise_for_status()

                    logger.info(f'Query {query_name} severity changed to {new_severity}')
                    print(f"Query {query_path} severity changed to {new_severity}")
                    return response.json()
                except requests.exceptions.RequestException as req_err:
                    print(f"Request error: {req_err}")

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {str(e)}")

                except ValueError as json_err:
                    print(f"Error parsing response JSON: {json_err}")
            else:
                print(f"Query {query_path} severity is already {new_severity}")
                continue

def main():
    # find_all_language_query_info("Use_Of_Hardcoded_Password")
    #check_existent_corp_override("Log_Forging")
    change_query_severity_corp_all_languages("Privacy_Violation", 3)
    pass


if __name__ == '__main__':

    main()
    exit(0)