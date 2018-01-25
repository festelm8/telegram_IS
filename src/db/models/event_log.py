from flask import current_app, g
from sqlalchemy.dialects.postgresql import UUID

from src.db import db


class EventLog(db.Model):
    __tablename__ = 'event_log'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    msg = db.Column(db.VARCHAR(255))
    course_number_id = db.Column(UUID, db.ForeignKey('course_numbers.id'))
    course_number = db.relationship('CourseNumber')
