from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask("CampusEats")
app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

db = SQLAlchemy()
db.init_app(app)

# creates tables for any models we add
with app.app_context():
    db.create_all()

from app import routes
