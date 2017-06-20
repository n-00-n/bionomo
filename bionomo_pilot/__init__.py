# encoding: utf8
from flask import Flask
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from config import config_by_name


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

    from . import view

    return Components.app
