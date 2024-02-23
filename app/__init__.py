from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

# We configure the SQLAlchemy part
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# We import the routers to make sure routes are registered
from app.routers import weatherRouter

# We make sure to import models after initializing the db to avoid circular imports
from app.models import city

# We initialize the database
with app.app_context():
    db.create_all()