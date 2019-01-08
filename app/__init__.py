from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import DevelopmentConfig


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
db.create_all()
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

from app import models, routes, forms