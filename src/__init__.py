"""Initialization of all codebase."""
from flask import Flask, request

from src.api import bp_app
from src.views import bp_web
from src.telehandler import bp_tele
from src.lib.access import login_manager
from src.db import db, rq


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    login_manager.init_app(app)
    db.init_app(app)
    rq.init_app(app)

    if app.config['DEBUG']:
        @app.after_request
        def after(resp):
            if resp.status_code >= 400:
                print(resp.get_data().decode())
            return resp


    app.register_blueprint(bp_app, url_prefix='/api')
    app.register_blueprint(bp_tele)
    app.register_blueprint(bp_web)


    return app
