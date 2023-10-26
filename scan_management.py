import requests
import json
import csv
import os

from authentication import Config, account_name, auth_headers
from logging_config import configure_logger, log_path


account = Config.get_account_config(account_name)
server_url = account.get('server_url')
file_path = account.get('file_path')

scan_number = '10000'


def get_scan_management():
    logger = configure_logger(log_path + "get_scan_management_" + account_name + ".log")
    url = server_url + '/api/scans/?limit=' + scan_number + '&offset=0'
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
        with open(file_path + "/scan_management.json", "w") as f:
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

        file_name = file_path + "/scan_management_" + account_name + "_" + scan_number + ".csv"

        # Create file if it doesn't exist
        if not os.path.exists(file_name):
            open(file_name, 'w').close()

        with open(file_name, "w", newline='', encoding='utf-8') as f:
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


def find_failed_scans():
    logger = configure_logger(log_path + "find_failed_scans_" + account_name + ".log")
    scan_management = get_scan_management()
    if scan_management:
        scans = scan_management["scans"]
        failed_scans = []
        for scan in scans:
            try:
                if scan["statusDetails"] is not None:
                    scanners = scan["statusDetails"]
                    for scanner in scanners:
                        scanner_status = scanner["status"]
                        if scanner_status == "Failed":
                            failed_scans.append(scan)
                            break
                else:
                    logger.warning("No statusDetails found for scan: %s" % scan)
            except KeyError:
                # Handle the case where "statusDetails" key is not present in the scan dictionary
                pass  # You can replace 'pass' with code to handle this situation as needed

        return failed_scans
    else:
        logger.error("Failed to find failed scans.")
        return None


def get_scan_management_and_failures():
    logger = configure_logger(log_path + "get_scan_failures_to_csv_" + account_name + ".log")
    scan_management = get_scan_management()

    # Create folder if it doesn't exist
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    file_name = file_path + "/scan_management_and_failures_" + account_name + "_" + scan_number + ".csv"

    # Create file if it doesn't exist
    if not os.path.exists(file_name):
        open(file_name, 'w').close()

    with open(file_name, "w", newline='', encoding='utf-8') as f:
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
                         "sourceOrigin",
                         "general",
                         "sca",
                         "kics",
                         "sast",
                         "apisec",
                         "sastLoc"])

        # Collect unique scan IDs to avoid duplicates
        scanned_ids = set()

        if scan_management is not None and "scans" in scan_management and isinstance(scan_management["scans"], list):
            scans = scan_management["scans"]
            for scan in scans:
                if isinstance(scan, dict):
                    scan_id = scan.get("id")

                    # Skip if the scan ID has already been processed
                    if scan_id in scanned_ids:
                        continue

                    metadata = scan.get("metadata")
                    metadata_json = json.dumps(metadata) if metadata is not None else None
                    status_details = scan.get("statusDetails")
                    status_details_json = json.dumps(status_details) if status_details is not None else None
                    engines = scan.get("engines")
                    engines_json = json.dumps(engines) if engines is not None else None

                    general_scanner_details = None
                    kics_scanner_details = None
                    sast_scanner_details = None
                    sca_scanner_details = None
                    apisec_scanner_details = None
                    sast_scanner_loc = None

                    if isinstance(status_details, list):
                        for status_detail in status_details:
                            if isinstance(status_detail, dict):
                                scanner_name = status_detail.get("name")
                                details = status_detail.get("details")

                                if scanner_name == "general":
                                    general_scanner_details = details
                                elif scanner_name == "kics":
                                    kics_scanner_details = details
                                elif scanner_name == "sast":
                                    sast_scanner_details = details
                                    sast_scanner_loc = status_detail.get("loc")
                                elif scanner_name == "sca":
                                    sca_scanner_details = details
                                elif scanner_name == "apisec":
                                    apisec_scanner_details = details

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
                        scan.get("sourceOrigin"),
                        general_scanner_details,
                        sca_scanner_details,
                        kics_scanner_details,
                        sast_scanner_details,
                        apisec_scanner_details,
                        sast_scanner_loc
                    ])

                    # Add the scan ID to the set of scanned IDs
                    scanned_ids.add(scan_id)

    logger.info("Successfully saved scan management to csv.")
    return True


def main():

    # get_scan_management_to_csv()
    # get_scan_management_to_json()
    # find_failed_scans()
    get_scan_management_and_failures()
    print("\nDone!")


if __name__ == '__main__':
    main()
    exit(0)
