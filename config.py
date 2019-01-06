import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SECRET = 'SecretKey01'


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SERVER_NAME = 'localhost:5000'
    USD_URL = 'https://private-anon-8cfc1d7f36-piastrix.apiary-mock.com/bill/create'
    RUB_URL = 'https://private-anon-8cfc1d7f36-piastrix.apiary-mock.com/invoice/create'