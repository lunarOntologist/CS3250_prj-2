from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    passwd = db.Column(db.LargeBinary, nullable=False)
    role = db.Column(db.String, nullable=False)  # student or vendor

class Posting(db.Model):
    __tablename__ = 'food postings'
    name = db.Column(db.String, nullable=False)
    portions = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    