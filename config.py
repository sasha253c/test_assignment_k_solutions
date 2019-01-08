import os
import pathlib

basedir = pathlib.Path().cwd()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SECRET = 'SecretKey01'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + str(basedir.joinpath('app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    USD_URL = 'https://private-anon-8cfc1d7f36-piastrix.apiary-mock.com/bill/create'
    RUB_URL = 'https://private-anon-8cfc1d7f36-piastrix.apiary-mock.com/invoice/create'