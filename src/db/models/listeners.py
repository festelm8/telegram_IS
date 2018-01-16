"""User model."""
from flask import current_app, g
from sqlalchemy.dialects.postgresql import UUID

from src.db import db


class Listeners(db.Model):
    __tablename__ = 'listeners'

    def __init__(self, song, connections):
        self.song = song
        self.connections = connections

    id = db.Column(db.INTEGER, primary_key=True)
    song = db.Column(db.VARCHAR(255), index=True)
    connections = db.Column(db.INTEGER, default=0)

    stream_id = db.Column(UUID, db.ForeignKey('streams.id'))
    stream = db.relationship('Stream')

    created_at = db.Column(db.TIMESTAMP(timezone=True),
                           server_default=db.text('now()::timestamp(0)'))
