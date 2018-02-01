from flask import current_app, g
from sqlalchemy.dialects.postgresql import UUID

from src.db import db


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    name = db.Column(db.VARCHAR(255))
    email = db.Column(db.VARCHAR(255))
    subjects = db.relationship('Subject')
