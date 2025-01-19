#! usr/bin/python3
# -*- coding: utf-8 -*-
import os
import json
from base64 import b64encode
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

load_dotenv()
config_file = 'config.json'
config_file = os.path.join(os.getcwd(), config_file)

class WriteConfigJson:

    @staticmethod
    def create_file():
        """
        Primarily used for set up purposes only.
        :return:
        """

        def random_string(bytes_=24):
            b = os.urandom(bytes_)
            return b64encode(b).decode('utf-8')

        db_username = os.getenv("DB_USERNAME", None)
        db_password = os.getenv("DB_PASSWORD", None)
        db_url = os.getenv("DB_URL", None)
        db_port = os.getenv("DB_PORT", None)
        db_name = os.getenv("DB_NAME", None)

        secret_key = random_string()
        notification_user_password = random_string()

        config_values = {
            'db_type': 3,
            'db_driver': "pymysql",
            'db_username': db_username,
            'db_password': db_password,
            'db_url': db_url,
            'db_port': db_port,
            'db_name': db_name,
            'SECRET_KEY': secret_key,
            'NOTIFICATION_USER_PASSWORD': notification_user_password
        }

        with open(config_file, 'w') as f:
            print('Writing config file to {}'.format(config_file))
            json.dump(config_values, f)

def check_db_connection(sqlalchemy_database_uri):
    """
    :param sqlalchemy_database_uri:
    :return:
    """

    base_error_message = f'There was a problem connecting to the database {sqlalchemy_database_uri}. Please check your config.json file.'

    try:
        engine = create_engine(sqlalchemy_database_uri)
        engine.connect()
    except ValueError:
        raise Exception(base_error_message)
    except OperationalError:
        raise Exception(base_error_message)

if __name__ == '__main__':
    WriteConfigJson.create_file()
