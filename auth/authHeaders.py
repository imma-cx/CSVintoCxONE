import requests

from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)

#grant_type = input("Grant Type (client_credentials/refresh_token): ")
grant_type = "refresh_token"

server_url = "https://deu.ast.checkmarx.net"
iam_url = "https://deu.iam.checkmarx.net"
ast_url = "https://deu..checkmarx.net"

#OAuth
tenant= "emanuel_ribeiro_gst"
username = "emanuel.ribeiro@checkmarx.com"
password = "Cx123456!!"
client_id = "API2"
client_secret = "wcOEgJAOP18Q4hF3Nlgtlejn5qAvNByE"

#API Key
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI0ZTA4ODYxOC01ODI3LTQyNmItYThjOS1hNmU2YmNkMmY5YzEifQ.eyJpYXQiOjE2NzI3NjEzNDQsImp0aSI6IjEzY2Y0MzQ1LTk1NjEtNGFlYS04N2Q1LTU4MGFkZWJmZGRmMCIsImlzcyI6Imh0dHBzOi8vZGV1LmlhbS5jaGVja21hcngubmV0L2F1dGgvcmVhbG1zL2VtYW51ZWxfcmliZWlyb19nc3QiLCJhdWQiOiJodHRwczovL2RldS5pYW0uY2hlY2ttYXJ4Lm5ldC9hdXRoL3JlYWxtcy9lbWFudWVsX3JpYmVpcm9fZ3N0Iiwic3ViIjoiY2NiZGM2YzEtNjk0My00Nzk4LWFjNDEtOGQzNmIzN2YxMTJmIiwidHlwIjoiT2ZmbGluZSIsImF6cCI6ImFzdC1hcHAiLCJzZXNzaW9uX3N0YXRlIjoiYThlMTRkM2QtNGVhZi00YzgzLWJmNjQtZjIyZjc2MDA4MzY0Iiwic2NvcGUiOiIgb2ZmbGluZV9hY2Nlc3MiLCJzaWQiOiJhOGUxNGQzZC00ZWFmLTRjODMtYmY2NC1mMjJmNzYwMDgzNjQifQ.7288TGhBDCs1zZNdKvkN-BLbzk4zINTwMQGZXu7LGIE"
#api_key = input("API KEY: ")

__response = ""

def get_token():
    """
        Args:
        Returns:
            Bear Token (str)
    """
    url = iam_url + "/auth/realms/" + tenant + "/protocol/openid-connect/token"

    if grant_type == "refresh_token":
        req_data = {
            "grant_type": "refresh_token",
            "client_id": "ast-app",
            "refresh_token": api_key,
        }

    else:
        req_data = {
            "grant_type": "client_credentials",
            "username": username,
            "password": password,
            "client_id": client_id,
            "client_secret": client_secret,
        }


    response = requests.post(url=url, data=req_data, verify=False)

    if response.status_code != 200:
        __response = response.status_code
        raise ValueError(response.text, response.status_code)

    content = response.json()
    return content.get("token_type") + " " + content.get("access_token")


auth_headers = {
    "Authorization": get_token(),
    "Accept": "application/json",
    "Content-Type": "application/json",
}

def update_auth_headers():
    auth_headers.update({"Authorization": get_token()})
    return __response

# print(auth_headers)