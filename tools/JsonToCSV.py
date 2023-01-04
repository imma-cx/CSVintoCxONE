import json
import csv

file_name = 'all_projects_names.json'
file_path = 'output/production/'

# Load the JSON data from the file
with open(file_path + file_name, 'r') as f:
    data = json.load(f)

# Extract the 'name' values from the data
names = [item['name'] for item in data]

# Write the names to a CSV file
with open(file_path + 'project_names.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Name'])  # write the header row
    writer.writerows([[name] for name in names])  # write the name rows