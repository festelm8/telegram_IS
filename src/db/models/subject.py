from flask import current_app, g
from sqlalchemy.dialects.postgresql import UUID

from src.db import db


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    name = db.Column(db.VARCHAR(255))
    teacher = db.Column(UUID, db.ForeignKey('teachers.id'))
