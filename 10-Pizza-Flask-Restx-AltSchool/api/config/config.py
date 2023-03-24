# pip install python-decouple to help retrieve and store the variables in .env file.

import os
import re
from datetime import timedelta
from decouple import config

# base_dir = os.path.abspath(os.path.dirname(__file__))
base_dir = os.path.dirname(os.path.realpath(__file__))


class Config:
    SECRET_KEY = config("SECRET_KEY", "secret")

    SQLALCHEMY_TRACK_MODIFICATION = False
    SQLALCHEMY_ECHO = True

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=10)
    JWT_SECRET_KEY = config("JWT_SECRET_KEY")

    PROPAGATE_EXCEPTIONS = True


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base_dir, "db.sqlite3")
    DEBUG = True  


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"  # to use sqlite in-memory database for testing, use // (instead of /// which create a path and a file in the project directory).


class ProductionConfig(Config):
    uri = config("DATABASE_URL")  # or other relevant config var
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    # rest of connection code using the connection string `uri`

    SQLALCHEMY_DATABASE_URI = uri
    DEBUG = config("DEBUG", False, cast=bool)
    SQLALCHEMY_ECHO = False
    # pass
    

config_dict = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

# # OR
# config_name = {
#     "dev": DevelopmentConfig,
#     "prod": ProductionConfig,
#     "test": TestingConfig
# }
