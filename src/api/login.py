"""login API."""
from flask_restful import Resource
from webargs.flaskparser import use_args

from src.db import db
from src.db.models import User
from src.schemas.login import login_post


class LoginAPI(Resource):
    @use_args(login_post)
    def post(self, data):
        """auth process using pbkdf2"""

        user = User.query.filter_by(email=data.get('email'), is_deleted=False).first()

        if not user:
            return {
                "message": ["authorization fail"]
            }, 401

        if user.is_banned:
            return {
                "message": ["account was banned"]
            }, 423

        if not user.verify_password(data.get('password')):
            return {
                "message": ["authorization fail"]
            }, 401

        access_token = user.generate_auth_token()

        return {
            'access_token': access_token
        }



