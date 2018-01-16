"""User model."""
from flask import current_app, g
from sqlalchemy.dialects.postgresql import UUID

from src.db import db


class Source(db.Model):
    __tablename__ = 'sources'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    name = db.Column(db.VARCHAR(100))
    main = db.Column(db.BOOLEAN, default=False)

    stream_id = db.Column(UUID, db.ForeignKey('streams.id'))
    stream = db.relationship('Stream')

    created_at = db.Column(db.TIMESTAMP(timezone=True),
                           server_default=db.text('now()::timestamp(0)'))
