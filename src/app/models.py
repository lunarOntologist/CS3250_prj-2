import string
import secrets
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    passwd = db.Column(db.LargeBinary, nullable=False)
    role = db.Column(db.String, nullable=False)  # student or vendor
    listings = db.relationship('Listing', back_populates='vendor', lazy=True)
    reservations = db.relationship('Reservation', back_populates='student', lazy=True)

class Listing(db.Model):
    __tablename__ = 'listings'
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    portions_total = db.Column(db.Integer, nullable=False)
    portions_reserved = db.Column(db.Integer, nullable=False, default=0)
    pickup_location = db.Column(db.String, nullable=False)
    dietary_tags = db.Column(db.JSON, nullable=False, default=list)
    pickup_start = db.Column(db.DateTime, nullable=False)
    pickup_end = db.Column(db.DateTime, nullable=False)
    cancelled = db.Column(db.Boolean, nullable=False, default=False)

    vendor = db.relationship('User', back_populates='listings')
    reservations = db.relationship('Reservation', back_populates='listing', lazy=True)


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable=False)
    portions = db.Column(db.Integer, nullable=False)
    pickup_code = db.Column(db.String(6), unique=True, nullable=False)
    status = db.Column(db.String, nullable=False, default='active')  # active, picked_up, cancelled, no-show
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    student = db.relationship('User', back_populates='reservations')
    listing = db.relationship('Listing', back_populates='reservations')

    @classmethod
    def generate_pickup_code(cls):
        alphabet = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(secrets.choice(alphabet) for _ in range(6))
            if not cls.query.filter_by(pickup_code=code).first():
                return code
