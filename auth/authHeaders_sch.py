import requests

from auth.creds import server_url_sch, api_key_sch, tenant_sch, iam_url_sch, username, password, client_id, client_secret
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)

#grant_type = input("Grant Type (client_credentials/refresh_token): ")
grant_type = "refresh_token"

def get_token():
    """
        Args:
        Returns:
            Bear Token (str)
    """
    url = iam_url_sch + "/auth/realms/" + tenant_sch + "/protocol/openid-connect/token"

    if grant_type == "refresh_token":
        req_data = {
            "grant_type": "refresh_token",
            "client_id": "ast-app",
            "refresh_token": api_key_sch,
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
        raise ValueError(response.text, response.status_code)

    content = response.json()
    return content.get("token_type") + " " + content.get("access_token")


auth_headers_sch = {
    "Authorization": get_token(),
    "Accept": "application/json",
    "Content-Type": "application/json",
}

def update_auth_headers():
    auth_headers_sch.update({"Authorization": get_token()})

if __name__ == "__main__":
    update_auth_headers()

# print(auth_headers)