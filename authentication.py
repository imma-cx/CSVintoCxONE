import requests
from config import Config
from logging_config import configure_logger, log_path

#set the account to use
account_name = "adidas"
#set to false if OAuth is to be used
use_api_key = "true"

logger = configure_logger(log_path + 'authentication.log')


auth_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

class AuthenticationError(Exception):
    pass

def get_token(account_name: str, use_api_key: bool):
    """
        Args:
        account_name: str
        use_api_key: bool
        Returns:
            Bear Token (str)
    """
    try:
        account_config = Config.get_account_config(account_name)
        iam_url = account_config.get('iam_url')
        tenant = account_config.get('tenant')
        url = iam_url + "/auth/realms/" + tenant + "/protocol/openid-connect/token"

        if use_api_key:
            req_data = {
                "grant_type": "refresh_token",
                "client_id": "ast-app",
                "refresh_token": account_config.get('api_key'),
            }
        else:
            req_data = {
                "grant_type": "client_credentials",
                "username": account_config.get('username'),
                "password": account_config.get('password'),
                "client_id": account_config.get('client_secret'),
                "client_secret": account_config.get('client_secret'),
            }

        response = requests.post(url=url, data=req_data, verify=False)

        if response.status_code != 200:
            raise AuthenticationError(f"Request failed with status code {response.status_code} and message: {response.text}")
        content = response.json()
        return content.get("token_type") + " " + content.get("access_token")
        
    except Exception as e:
        logger.exception(f"Error getting token for account {account_name}: {e}")
        raise

auth_headers["Authorization"] = get_token(account_name, use_api_key)


