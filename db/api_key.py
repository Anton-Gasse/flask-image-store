from db import db
from datetime import datetime
from sqlalchemy.sql import func


class APIKey(db.Model):
    api_key = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(32), server_default="anonymous")
    timestamp = db.Column(db.DateTime, nullable=False)
