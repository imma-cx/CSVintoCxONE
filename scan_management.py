import requests
import json
import csv
import os

from authentication import Config, account_name, auth_headers
from logging_config import configure_logger, log_path


account = Config.get_account_config(account_name)
server_url = account.get('server_url')
file_path = account.get('file_path')


def get_scan_management():
    logger = configure_logger(log_path + "get_scan_management_" + account_name + ".log")
    url = server_url + '/api/scans/?limit=200&offset=0'
    response = requests.get(url, headers=auth_headers)
    if response.status_code == 200:
        logger.info("Successfully retrieved scan management.")
        return response.json()
    else:
        logger.error("Failed to retrieve scan management.")
        return None


def get_scan_management_to_json():
    logger = configure_logger(log_path + "get_scan_management_to_file_" + account_name + ".log")
    scan_management = get_scan_management()
    if scan_management:
        with open(file_path + "/scan_management_100.json", "w") as f:
            json.dump(scan_management, f, indent=4)
            logger.info("Successfully saved scan management to file.")
            return True
    else:
        logger.error("Failed to save scan management to file.")
        return False


def get_scan_management_to_csv():
    logger = configure_logger(log_path + "get_scan_management_to_csv_" + account_name + ".log")
    scan_management = get_scan_management()

    if "scans" in scan_management and isinstance(scan_management["scans"], list):
        scans = scan_management["scans"]

        # Create folder if it doesn't exist
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file_name = file_path + "/scan_management_" + account_name + "_200.csv"

        # Create file if it doesn't exist
        if not os.path.exists(file_name):
            open(file_name, 'w').close()

        with open(file_name, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["id",
                             "status",
                             "branch",
                             "createdAt",
                             "updatedAt",
                             "projectId",
                             "projectName",
                             "userAgent",
                             "initiator",
                             "tags",
                             "metadata",
                             "engines",
                             "statusDetails",
                             "sourceType",
                             "sourceOrigin"])

            for scan in scans:
                if isinstance(scan, dict):
                    metadata = scan.get("metadata")
                    metadata_json = json.dumps(metadata) if metadata is not None else None
                    status_details = scan.get("statusDetails")
                    status_details_json = json.dumps(status_details) if status_details is not None else None
                    # handle_status_details(status_details_json)
                    engines = scan.get("engines")
                    engines_json = json.dumps(engines) if engines is not None else None
                    # engines_string = ', '.join(engines)

                    writer.writerow([
                        scan.get("id"),
                        scan.get("status"),
                        scan.get("branch"),
                        scan.get("createdAt"),
                        scan.get("updatedAt"),
                        scan.get("projectId"),
                        scan.get("projectName"),
                        scan.get("userAgent"),
                        scan.get("initiator"),
                        scan.get("tags"),
                        metadata_json,
                        engines_json,
                        status_details_json,
                        scan.get("sourceType"),
                        scan.get("sourceOrigin")
                    ])
                else:
                    logger.warning("Invalid scan entry: %s" % scan)

            logger.info("Successfully saved scan management to csv.")
            return True
    else:
        logger.error("Invalid scan_management format. Scans not found in the dictionary.")
        return False


def main():

    get_scan_management_to_csv()
    # get_scan_management_to_json()

    print("\nDone!")


if __name__ == '__main__':
    main()
    exit(0)
