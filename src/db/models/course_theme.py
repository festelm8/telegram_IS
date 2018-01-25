from flask import current_app, g
from sqlalchemy.dialects.postgresql import UUID

from src.db import db


class CourseTheme(db.Model):
    __tablename__ = 'course_themes'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    name = db.Column(db.VARCHAR(255))
