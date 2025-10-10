from os import getenv

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

env_dict = {
    'DB_USER': getenv('DB_USER'),
    'DB_PASSWORD': getenv('DB_PASSWORD'),
    'DB_HOST': getenv('DB_HOST'),
    'DB_NAME': getenv('DB_NAME')
}

missing_envs = [k for k,v in env_dict.items() if v is None]

if missing_envs:
    raise EnvironmentError(f"Missing environment variables: [{', '.join(missing_envs)}]")

DB_CONNSTR = f'postgresql+psycopg2://{env_dict['DB_USER']}:{env_dict['DB_PASSWORD']}@{env_dict['DB_HOST']}/{env_dict['DB_NAME']}'

db = SQLAlchemy()
