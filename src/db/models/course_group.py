from flask import current_app, g
from sqlalchemy.dialects.postgresql import UUID

from src.db import db


class CourseGroup(db.Model):
    __tablename__ = 'course_groups'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    gid = db.Column(db.VARCHAR(30))
    course_number_id = db.Column(UUID, db.ForeignKey('course_numbers.id'))
    course_number = db.relationship('CourseNumber')
    students = db.relationship('User')
    class_schedule = db.relationship('ClassSchedule', lazy='dynamic')
