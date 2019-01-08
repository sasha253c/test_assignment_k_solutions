import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SECRET = 'SecretKey01'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    # SERVER_NAME = '0.0.0.0:5001'
    USD_URL = 'https://private-anon-8cfc1d7f36-piastrix.apiary-mock.com/bill/create'
    RUB_URL = 'https://private-anon-8cfc1d7f36-piastrix.apiary-mock.com/invoice/create'