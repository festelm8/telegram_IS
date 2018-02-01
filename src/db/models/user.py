"""User model."""
from flask import current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID

from src.lib.access import generate_token, verify_token, login_manager
from src.db import db


# from src.lib.push import push_message

class User(db.Model):
    """Base user model class."""

    __tablename__ = 'users'

    # identification
    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    tid = db.Column(db.INTEGER)
    email = db.Column(db.VARCHAR(120))
    password = db.Column(db.VARCHAR(256))
    course_group_id = db.Column(UUID, db.ForeignKey('course_groups.id'))
    course_group = db.relationship('CourseGroup')

    is_admin = db.Column(db.BOOLEAN, default=False)
    is_banned = db.Column(db.BOOLEAN, default=False)
    banned_at = db.Column(db.TIMESTAMP(timezone=True))
    is_deleted = db.Column(db.BOOLEAN, default=False)
    deleted_at = db.Column(db.TIMESTAMP(timezone=True))

    # Tech info
    created_at = db.Column(db.TIMESTAMP(timezone=True),
                           server_default=db.text('now()::timestamp(0)'))

    # password functions
    def hash_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=15)

    def verify_password(self, recieved_password):
        return check_password_hash(self.password, recieved_password)

    # token finctions
    def generate_auth_token(self):
        return generate_token(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return not self.is_banned

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @staticmethod
    def verify_auth_token(token):
        token_claimset = verify_token(token)
        if not token_claimset:
            return None
        current_user = User.query.get(token_claimset['id'])

        return current_user

    # ban function
    def ban(self):
        self.is_banned = True
        self.banned_at = db.text('now()::timestamp(0)')
        db.session.commit()

    def ban_recovery(self):
        self.is_banned = False
        self.banned_at = None
        db.session.commit()

    # delete function
    def delete(self):
        self.is_deleted = True
        self.deleted_at = db.text('now()::timestamp(0)')
        db.session.commit()

    def recovery(self):
        self.is_deleted = False
        self.deleted_at = None
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id, is_deleted=False).first()