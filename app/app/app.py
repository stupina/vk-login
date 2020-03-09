from flask import Flask

from app.db import db
from app.login_manager import login_manager
from app.resources import add_resources


def create_app(configuration):
    app = Flask(__name__)
    app.config.from_object(configuration)
    db.init_app(app)
    login_manager.init_app(app)
    add_resources(app)
    return app
