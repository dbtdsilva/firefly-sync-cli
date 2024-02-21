import argparse
from dotenv import dotenv_values
import sys
from datetime import datetime, timedelta

from firefly_api.api import FireflyApi
from firefly_api.models.account_type import AccountType

__version__ = "1.0.0"

MANDATORY_ENV_KEYS = ["FIREFLY_URL", "FIREFLY_TOKEN"]


def load_config():
    env_values = dotenv_values(".env")
    if not all(mandatory_key in env_values.keys() for mandatory_key in MANDATORY_ENV_KEYS):
        print('Values are missing from .env')
        sys.exit(1)
    return env_values


def main(args: argparse.Namespace):
    """ Main entry point of the app """
    env_values = load_config()

    api = FireflyApi(env_values["FIREFLY_URL"], env_values["FIREFLY_TOKEN"])
    accounts = api.accounts.get_accounts(AccountType.ASSET)
    print(len(accounts))

    api.transactions.get_transactions(start_date=datetime.now() - timedelta(days=1000), end_date=datetime.now())
    print(accounts[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="File to be imported")
    myargs = parser.parse_args()
    main(myargs)
