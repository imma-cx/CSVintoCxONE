from typing import Dict
from auth.credentials import Credentials
from logging_config import configure_logger, log_path

#security issue
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
disable_warnings(InsecureRequestWarning)

logger = configure_logger(log_path + 'get_account.log')

class Config:
    get_account_config = Credentials.get_account_config

    logger = configure_logger(log_path + 'get_account.log')

    @classmethod
    def get_account(cls, account_name: str) -> Dict:
        try:
            account_config = Credentials.get_account_config(account_name)
            server_url = account_config.get('server_url')
            iam_url = account_config.get('iam_url')
            tenant = account_config.get('tenant')

            return cls.ACCOUNTS.get(account_name, {}), server_url, iam_url, tenant

        except Exception as e:
            logger.exception(f"Error getting token for account {account_name}: {e}")
        raise

