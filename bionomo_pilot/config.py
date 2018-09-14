# encoding: utf8
import os
from constants import Constants as c
basedir = os.path.abspath(os.path.dirname(__file__))
basedir_parent = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
os_path = os.path


class Config(object):
    SECRET_KEY = '\x9e\x03G\x02\xed\x03\xde\x1c\xdag\xde\xbb\x0f\x15:Tc\xd4[1\x182,\xcf\xdf\x8a\xa9U\x85Q'
    DEBUG = False
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = '5000'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/bionomo_dev'
    MULTIMEDIA_DIR = os.path.join(basedir_parent, 'multimedia')
    MULTIMEDIA_ENDPOINT = '/mm'
    SUPPORTED_LANGUAGES = c.LOCALE_DICT
    SUPPORTED_LANGUAGES_PATH = ['/en/', '/pt/', '/fr/', '/it/']
    BABEL_DEFAULT_LOCALE = c.DEFAULT_LOCALE
    BABEL_DEFAULT_TIMEZONE = 'UTC+2'
    LOGS_DIR = os.path.join(basedir_parent, 'logs')


class DevelopmentConfig(Config):
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = '2000'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@localhost/b_t' # change to 'bionomo_dev' for the data.
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = False


class TestConfig(Config):
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = '2222'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/bionomo_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = '2222'
    SQLALCHEMY_DATABASE_URI = 'mysql://cagy8s69mz3xdj2x:d05065yh5lpry0kb@a7e4sgso2kxq2hsi.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/primary_app_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_by_name = {
    'dev': DevelopmentConfig,
    'test': TestConfig,
    'prod': ProductionConfig,
}

env = 'prod'
