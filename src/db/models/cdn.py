from flask import current_app, g
from sqlalchemy.dialects.postgresql import UUID

from src.db import db


class Cdn(db.Model):
    __tablename__ = 'cdns'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    name = db.Column(db.VARCHAR(200))
    access_id = db.Column(db.VARCHAR(100))
    sources_domain = db.Column(db.VARCHAR(255))
    is_active = db.Column(db.BOOLEAN, default=True)

    streams = db.relationship('Stream', lazy='dynamic')

    created_at = db.Column(db.TIMESTAMP(timezone=True),
                           server_default=db.text('now()::timestamp(0)'))

