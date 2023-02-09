import matplotlib.pyplot as plt
import json

json_data = ""
def process_json_data(json_data):
    data = json.loads(json_data)
    scans = data['scans']

    # Extract the status of each scan
    scan_statuses = [scan['status'] for scan in scans]

    # Count the occurrences of each status
    status_counts = {}
    for status in scan_statuses:
        status_counts[status] = status_counts.get(status, 0) + 1

    # Create a bar graph
    labels = list(status_counts.keys())
    values = list(status_counts.values())

    plt.bar(labels, values)
    plt.xlabel('Status')
    plt.ylabel('Count')
    plt.title('Scan Statuses')
    plt.show()

