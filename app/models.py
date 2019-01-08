from datetime import datetime
from app import db


class LogTable(db.Model):
    id = db.Column(db.Integer, primary_key=True) # auto incrementing
    logger = db.Column(db.String(64)) # the name of the logger. (e.g. myapp.views)
    level = db.Column(db.String(64)) # info, debug, or error?
    trace = db.Column(db.String(4096)) # the full traceback printout
    msg = db.Column(db.String(4096)) # any custom log you may have included
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # the current timestamp

    # def __init__(self, logger=None, level=None, trace=None, msg=None):
    #     self.logger = logger
    #     self.level = level
    #     self.trace = trace
    #     self.msg = msg


    def __repr__(self):
        return f"{self.logger}: {self.msg}"
