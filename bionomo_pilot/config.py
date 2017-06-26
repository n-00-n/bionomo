# encoding: utf8
import os
from constants import Constants as c
basedir = os.path.abspath(os.path.dirname(__file__))
basedir_parent = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


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


class DevelopmentConfig(Config):
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = '2000'
    # SQLALCHEMY_DATABASE_URI = 'mysql://ct5zpqnonuj4yzxt:oe4j63qqgbraembs@d6vscs19jtah8iwb.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/ihnk2l2rtodwc0un'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/bionomo_dev'


class TestConfig(Config):
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = '2222'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/bionomo_test'

config_by_name = {
    'dev': DevelopmentConfig,
    'test': TestConfig,
}

env = 'dev'
