from src.db import db
from sqlalchemy.dialects.postgresql import UUID

course_number_subjects = db.Table(
    'course_number_subjects',
    db.Column('course_number_id', UUID, db.ForeignKey('course_numbers.id')),
    db.Column('subject_id', UUID, db.ForeignKey('subjects.id'))
)