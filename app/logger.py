import logging
import traceback
from functools import wraps
from logging.handlers import RotatingFileHandler

from app import db
from app.models import LogTable


def function_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = None
        args_str = ', '.join(map(str, args))
        kwargs_str = ';\n'.join('%s = %s' % (k, v) for k, v in kwargs.items()) or ''
        try:
            res = func(*args, **kwargs)
        except Exception as error:
            LOGGER.exception(f"Error: {error}")

        LOGGER.info(f"function: {func.__name__} runs with:\n\targs: {args_str}\n\tkwargs: {kwargs_str}")
        return res
    return wrapper


class SQLAlchemyHandler(logging.Handler):
    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc(exc)

        log = LogTable(
            logger=record.__dict__['name'],
            level=record.__dict__['levelname'],
            trace=trace,
            msg=record.__dict__['msg'],)
        db.session.add(log)
        db.session.commit()


file_handler = RotatingFileHandler('logs.log', maxBytes=10000, backupCount=1)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

sql_handler = SQLAlchemyHandler()
sql_handler.setLevel(logging.INFO)
sql_handler.setFormatter(formatter)

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(file_handler)
LOGGER.addHandler(sql_handler)
LOGGER.setLevel(logging.INFO)

