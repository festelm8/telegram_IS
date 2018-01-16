"""Initialization API."""
from flask import Blueprint, request, g
from flask_restful import Api
from flask_login import current_user as web_current_user

from src.db.models import User
from src.api import (
    ping,
    login,
    statistic,
)

bp_app = Blueprint('bp_app', __name__)
api = Api(bp_app)


@bp_app.before_request
def current_user():
    """get current user by token"""

    req_token = request.headers.get('Authorization')
    _current_user = False
    if req_token:
        user = User.verify_auth_token(req_token)
        if user:
            _current_user = user
    if web_current_user:
        _current_user = web_current_user
    with request:
        g.current_user = _current_user
        g.host = request.headers.get('Host')


api.add_resource(ping.PingAPI, '/ping')
api.add_resource(login.LoginAPI, '/auth/login')
api.add_resource(statistic.StatisticAPI, '/statistic/<stream_id>')

