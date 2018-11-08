# encoding=utf8
import os

class Config(object):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    CONFIG_MYSQL_USERNAME = "root"
    CONFIG_MYSQL_PASSWORD = "19940301"
    CONFIG_MYSQL_DATABASE = "soda_data_repo"


class Development(Config):

    CONFIG_MYSQL_USERNAME = os.environ.get("CONFIG_MYSQL_USERNAME", "root")
    CONFIG_MYSQL_PASSWORD = os.environ.get("CONFIG_MYSQL_PASSWORD", "19940301")
    CONFIG_MYSQL_DATABASE = os.environ.get("CONFIG_MYSQL_DATABASE", "soda_data_repo")

class Production(Config):

    DEBUG = False
    CONFIG_MYSQL_USERNAME = os.environ.get("CONFIG_MYSQL_USERNAME", "root")
    CONFIG_MYSQL_PASSWORD = os.environ.get("CONFIG_MYSQL_PASSWORD", "19940301")
    CONFIG_MYSQL_DATABASE = os.environ.get("CONFIG_MYSQL_DATABASE", "soda_data_repo")
