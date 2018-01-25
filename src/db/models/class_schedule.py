from flask import current_app, g
from sqlalchemy.dialects.postgresql import UUID

from src.db import db


class ClassSchedule(db.Model):
    __tablename__ = 'class_schedule'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    dow = db.Column(db.VARCHAR(5))
    classroom = db.Column(db.VARCHAR(30))
    course_number = db.Column(UUID, db.ForeignKey('course_numbers.id'))
    subject = db.Column(UUID, db.ForeignKey('subjects.id'))