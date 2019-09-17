# encoding: utf8
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from bionomo_pilot.config import config_by_name, os_path


class Components:
    db = None
    app = None
    babel = None


def create_app(environment):
    """This so I can dynamically change environments (dev, test,etc.)
     without too much hassle"""
    app = Flask(__name__)
    app.config.from_object(config_by_name[environment])

    Components.app = app
    Components.db = SQLAlchemy(Components.app)

    Components.babel = Babel(Components.app)
    if not Components.babel:
        pass

    # Components.babel.init_app(app)

    handler = RotatingFileHandler(os_path.join(app.config['LOGS_DIR'], 'bionomo.log'), maxBytes=50000, backupCount=10,
                              encoding='utf-8')
    handler.setLevel(logging.INFO)
    Components.app.logger.addHandler(handler)

    from . import view

    return Components.app
