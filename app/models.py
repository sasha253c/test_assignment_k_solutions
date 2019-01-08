from datetime import datetime
from app import db


class LogTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logger = db.Column(db.String(64))
    level = db.Column(db.String(64))
    trace = db.Column(db.String(4096))
    msg = db.Column(db.String(4096))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f"{self.logger}: {self.msg}"
