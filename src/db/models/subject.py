from flask import current_app, g
from sqlalchemy.dialects.postgresql import UUID

from src.db import db
from src.db.models.m2m import course_number_subjects


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    name = db.Column(db.VARCHAR(255))
    desc = db.Column(db.TEXT)
    teacher_id = db.Column(UUID, db.ForeignKey('teachers.id'))
    teacher = db.relationship('Teacher')
    lessons = db.relationship('ClassSchedule')
    course_subscribed = db.relationship('CourseNumber', secondary=course_number_subjects, lazy='dynamic')

