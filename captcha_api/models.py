from datetime import datetime

from .db import db


class Captcha(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    answer = db.Column(db.String(120), nullable=False)
    creation_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return "<Captcha %r>" % self.id
