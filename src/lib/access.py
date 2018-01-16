from flask import current_app, g
from uuid import UUID
from flask_login import LoginManager
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired,
)


login_manager = LoginManager()

def validate_uuid(uuid_string):
    try:
        val = UUID(uuid_string)
    except ValueError:
        return False
    return True

def generate_token(uid):
    """declaring token couple"""

    token_serializer = Serializer(current_app.config['SECRET_KEY'], expires_in=current_app.config['TOKEN_EXPIRATION'])
    token = token_serializer.dumps({
        'id': uid,
    }).decode('ascii')

    return token


def verify_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        token_claimset = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid

    return token_claimset

def user_only():
    """Verification of access to the resource"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            if not g.current_user:
                return {
                           "message": ["Access not allowed"],
                       }, 403
            return func(*args, **kwargs)
        return wrapper
    return decorator