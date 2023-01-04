import csv
import json
import login
import os

import get_groups

customer = login.customer
file_path = login.file_path_customer

file = login.csv_data_customer

f = open(file, 'r')

#skipt the first line of csv file
next(f)

# Change each fieldname to the appropriate field name.
reader = csv.DictReader( 
    f, 
    delimiter=';', 
    fieldnames = (
        "LeanixId",
        "Profile(ProjectName)",
        "ProductDomain",
        "ProductArea",
        "Assignee",
        "SecurityChampion",
        "isMostCritical",
        "isInternetExposed",
        "SPE",
        "Migrated(Y/N)",
        "Groups(TeamList)"
        ))

def __readCSVtoJSON(reader):
   
    #read from csv and create json body for API POST
    out = []
    for row in reader:
        item =  {}
        item['name'] = row['Profile(ProjectName)']

        #use for groups from csv
        #item['groups'] = row['Groups(TeamList)'].split(',')
        #use for import id directly from API Response in get_groups.py
        item['groups'] = {}
        groups = row['Groups(TeamList)'].split(',')
        for group in groups:
            item['groups'] = [get_groups.__get_group_id(group) for group in groups]

        item['origin'] = 'API'
        item['tags'] = {}
        if row['LeanixId']:
            item['tags']['LeanixId'] = row['LeanixId']
        if row['ProductDomain']:
            item['tags']['ProductDomain'] = row['ProductDomain']
        if row['ProductArea']:
            item['tags']['ProductArea'] = row['ProductArea']
        if row['isMostCritical']:
            item['tags']['isMostCritical'] = row['isMostCritical']
        if row['isInternetExposed']:
            item['tags']['isInternetExposed'] = row['isInternetExposed']

        out.append(item)

    # Parse the CSV into JSON
    outjson = json.dumps(out)

    # Save the JSON
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    f = open(file_path + 'fromCSV_withGroupID_' + customer + '.json', 'w')
    f.write(outjson)

__readCSVtoJSON(reader)

def __getGroupsToJSON(reader):

    out = []
    for row in reader:
        item =  {}
        item['name'] = row['Groups(TeamList)']

        out.append(item)

    outjson = json.dumps(out)

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    f = open(file_path + 'all_groups.json','w')
    f.write(outjson)

    data = json.loads(outjson)

    groups = []
    for d in data:
        for group in d['name'].split(','):
            groups.append(group.strip())
            unique_groups = set(groups)

    groupout = [{'name': item} for item in unique_groups]
    group_out = json.dumps(groupout)

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    f = open(file_path + 'groups.json', 'w')
    f.write(group_out)

#__getGroupsToJSON(reader)