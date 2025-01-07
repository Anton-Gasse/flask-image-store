from db import db
from datetime import datetime


class Image(db.Model):
    filename = db.Column(db.String(64), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now())
