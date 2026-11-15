from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    posted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_posted = db.Column(db.Boolean, default=False)
    reserved_portions = db.Column(db.Integer, default=0)
    picked_up_portions = db.Column(db.Integer, default=0)
    no_show_count = db.Column(db.Integer, default=0)

    # Relationship to User (assuming a User model exists for vendor_id)
    vendor = db.relationship('User', backref='listings')

    def __repr__(self):
        return f'<Listing {self.id}: {self.title}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_vendor = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'