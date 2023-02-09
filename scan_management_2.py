import requests
import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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


def get_scan_management_number(scan_number):
    logger = configure_logger(log_path + "get_scan_management_number_" + account_name + ".log")
    url = server_url + '/api/scans/?limit=' + str(scan_number) + '&offset=0'
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
        with open(file_path + "/scan_management_200.json", "w") as f:
            json.dump(scan_management, f, indent=4)
            logger.info("Successfully saved scan management to file.")
            return True
    else:
        logger.error("Failed to save scan management to file.")
        return False


def handle_status_details(data, filename):
    # Load the existing CSV file
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        df = pd.DataFrame()

    # Create a new DataFrame for the status details
    status_df = pd.DataFrame(data)

    # Append the status details DataFrame to the existing DataFrame
    df = pd.concat([df, status_df], ignore_index=True)

    # Save the combined DataFrame back to the CSV file
    df.to_csv(filename, index=False)

    print(f"Status details added to the CSV file '{filename}' successfully.")


def get_scan_management_to_csv():
    logger = configure_logger(log_path + "get_scan_management_to_csv_" + account_name + ".log")
    scan_management = get_scan_management()

    if "scans" in scan_management and isinstance(scan_management["scans"], list):
        scans = scan_management["scans"]
        filename = file_path + "/scan_management_200.csv"
        with open(filename, "w") as f:
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
                    # status_details_json = json.dumps(status_details) if status_details is not None else None
                    # print(status_details_json)
                    # handle_status_details(status_details_json, filename)
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
                        status_details[0]["name"] if status_details else None,
                        status_details[0]["status"] if status_details else None,
                        status_details[0]["details"] if status_details else None,
                        #status_details[0]["loc"] if status_details[0]["loc"] else None,
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


def analyze_scans_by_project(data, project_id):
    # Create a DataFrame from the scan_management_response
    df = pd.DataFrame(data["scans"])
    # print(df)
    # Count the number of scans with the same projectId
    scan_count = df[df["projectId"] == project_id].shape[0]
    if scan_count > 0:
        print("Project ID:", project_id)

        project_name = df[df["projectId"] == project_id]["projectName"].unique()[0]
        print("Project Name:", project_name)
        print("Number of scans:", scan_count)

        df["sourceType"] = df["sourceType"].astype(str)
        source_type_counts = df[df["projectId"] == project_id]["sourceType"].value_counts()
        source_type_counts_dict = source_type_counts.to_dict()
        for source_type, count in source_type_counts_dict.items():
            print(f"Source Type: {source_type}, Count: {count}")
        # engines = df[df["projectId"] == project_id]["engines"].unique()

        scan_status = df[df["projectId"] == project_id]["status"].value_counts()
        if scan_status.item() > 0:
            partial_scans_count = df[df["projectId"] == project_id]["status"].value_counts().get("Completed", 0)
            if partial_scans_count > 0:
                print("Completed Scans:", partial_scans_count)
            else:
                print("Completed Scans: 0")
            partial_scans_count = df[df["projectId"] == project_id]["status"].value_counts().get("Partial", 0)
            if partial_scans_count > 0:
                print("Partial Scans:", partial_scans_count)
            else:
                print("Partial Scans: 0")
            failed_scans_count = df[df["projectId"] == project_id]["status"].value_counts().get("Failed", 0)
            if failed_scans_count > 0:
                print("Failed Scans:", failed_scans_count)
            else:
                print("Failed Scans: 0")


        # print("Number of unique source types:", source_type_count)
        print("Source types:", source_type_counts)
    else:
        print("No scans found for this project.")
    return scan_count


def analyze_scan_statuses(status_details_json):
    # Load the JSON data
    data = json.loads(status_details_json)

    # Extract the scan statuses
    statuses = [status['status'] for status in data['statusDetails']]

    # Count the occurrences of each scan status
    status_counts = pd.Series(statuses).value_counts()

    # Plot a bar chart to visualize the scan statuses
    status_counts.plot(kind='bar')
    plt.xlabel('Scan Status')
    plt.ylabel('Count')
    plt.title('Scan Status Summary')
    plt.xticks(rotation=45)
    plt.show()

    # Print the count of each scan status
    print('Scan Status Summary:')
    print(status_counts)


def get_failed_by_error_code(data, error_code):
    error_count = 0

    for scan in data["scans"]:
        for status in scan["statusDetails"]:
            if status.get("status") == "Failed" and ("ErrCode=" + error_code) in status.get("details", ""):
                error_count += 1

    print("Number of scans failed with the specified error:", error_count)


def main():
    data = get_scan_management()
    # project_id = "b9a0a227-2dc2-4d2f-88dd-f098267e50a1"
    # analyze_scans_by_project(data, project_id)

    # analyze_scan_statuses(status_details_json)
    # get_scan_management_to_csv()
    # get_scan_management_to_json()
    # error_code = "3443"
    # get_failed_by_error_code(data, error_code)
    # print("\nDone!")


if __name__ == '__main__':
    main()
    exit(0)
