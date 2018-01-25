from flask import current_app, g
from sqlalchemy.dialects.postgresql import UUID

from src.db import db
from src.db.models.m2m import course_number_subjects

class CourseNumber(db.Model):
    __tablename__ = 'course_numbers'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    number = db.Column(db.INTEGER, default=0)
    course_theme = db.Column(UUID, db.ForeignKey('course_themes.id'))
    subjects = db.relationship('Game', secondary=course_number_subjects, lazy='dynamic')
