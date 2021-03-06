# encoding: utf8
import os
from bionomo_pilot.constants import Constants as c
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
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:admin@localhost/bionomo_pilot_dev' # change to 'bionomo_dev' for the data.
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
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_by_name = {
    'dev': DevelopmentConfig,
    'test': TestConfig,
    'prod': ProductionConfig,
}


env = 'prod'

