import json

from get_projects import get_projects

tenant_json = get_projects()
file_json = json.load(open('output/adidas/new_data/fromCSV_withGroupID_adidas_latest.json'))


def projects_compare(tenant_json, file_json):
    tenant_projects = tenant_json['projects']
    file_projects = file_json

    tenant_projects_names = []
    for project in tenant_projects:
        tenant_projects_names.append(project['name'])

    file_projects_names = []
    for project in file_projects:
        file_projects_names.append(project['name'])

    for project in file_projects:
        if project['name'] not in tenant_projects_names:
            print(project['name'])

    for project in tenant_projects:
        if project['name'] not in file_projects_names:
            print(project['name'])


projects_compare(tenant_json,  file_json)