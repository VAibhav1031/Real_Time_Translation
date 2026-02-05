import os
from dotenv import load_dotenv

load_dotenv()


class DevConfig:
    ###################################
    # DB_configs (taken from env file)
    ###################################

    DB_USER = os.environ.get("DEV_DB_USER")
    DB_PASSWORD = os.environ.get("DEV_DB_PASSWORD")
    DB_HOST = os.environ.get("DEV_DB_HOST","localhost")
    DB_PORT = os.environ.get("DEV_DB_PORT")
    DB_NAME = os.environ.get("DEV_DB_NAME")

    ###################################
    # SQLAlchemy config
    ##################################

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")

    DEBUG = True

class ProdConfig:
    ###################################
    # DB_configs (taken from env file)
    ###################################

    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("DB_NAME")

    ###################################
    # SQLAlchemy config
    ##################################

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")

    DEBUG = False



config = {
    "development": DevConfig,
    "production": ProdConfig,
    "default": DevConfig,
}

print(os.environ.get("DEV_DB_USER"))
print(os.environ.get("DEV_DB_HOST"))

def get_config(config_name=None):
    # it will first go and check the .env  if it has the FLASK_ENV or not
    # then it will proceed to the  to return
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    return config.get(config_name, DevConfig)
