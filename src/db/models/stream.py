from flask import current_app, g
from sqlalchemy.dialects.postgresql import UUID

from src.db import db


class Stream(db.Model):
    __tablename__ = 'streams'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    name = db.Column(db.VARCHAR(200))

    listeners = db.relationship('Listeners', lazy='dynamic')
    sources = db.relationship('Source', lazy='dynamic')

    cdn_id = db.Column(UUID, db.ForeignKey('cdns.id'))
    cdn = db.relationship('Cdn')

    created_at = db.Column(db.TIMESTAMP(timezone=True),
                           server_default=db.text('now()::timestamp(0)'))


    @property
    def main_source(self):
        return self.sources.filter_by(main=True).first()


    @property
    def source_list(self):
        return [source.name for source in self.sources.all()]
