"""Initialization of database."""
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from flask_rq2 import RQ
from src.lib.utils import get_config

db = SQLAlchemy()
session = db.session
redis = Redis( get_config('REDIS_HOST'), db=0 )
rq = RQ()

from src.db import models
