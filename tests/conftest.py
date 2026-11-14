"""Shared pytest fixtures.

The application reads ``SECRET_KEY`` and ``DATABASE_URL`` from the environment
when it is imported, so both are configured here before ``app`` is imported.
Tests always run against an in-memory SQLite database and never touch the
application's real ``instance/app.db``.
"""

import os
import sys

import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
SRC_DIR = os.path.join(REPO_ROOT, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

os.environ['SECRET_KEY'] = 'test-secret-key'
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

import bcrypt

from app import app as flask_app, db
from app.models import Listing, Reservation, User

TEST_PASSWORD = 'password123'


@pytest.fixture()
def app():
    """A Flask app wired to a fresh in-memory database for each test."""
    flask_app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """Flask test client."""
    return app.test_client()


def _hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


@pytest.fixture()
def create_user(app):
    """Factory that stores a user with a hashed password."""

    def _create_user(email, role='vendor', name='Test User', password=TEST_PASSWORD):
        user = User(
            name=name,
            email=email,
            passwd=_hash(password),
            role=role,
        )
        db.session.add(user)
        db.session.commit()
        return user

    return _create_user


@pytest.fixture()
def login(client):
    """Log a user in through the real login form."""

    def _login(email, password=TEST_PASSWORD):
        return client.post(
            '/login',
            data={'email': email, 'passwd': password},
            follow_redirects=False,
        )

    return _login


@pytest.fixture()
def make_listing(app):
    """Factory that stores a listing for a vendor."""

    def _make_listing(vendor, created_at, portions_total=5, title='Surplus Food'):
        listing = Listing(
            vendor_id=vendor.id,
            title=title,
            description='Leftovers',
            portions_total=portions_total,
            pickup_location='Campus Cafe',
            dietary_tags=[],
            pickup_start=created_at,
            pickup_end=created_at,
            created_at=created_at,
        )
        db.session.add(listing)
        db.session.commit()
        return listing

    return _make_listing


@pytest.fixture()
def make_reservation(app):
    """Factory that stores a reservation with a given status."""

    def _make_reservation(listing, student, portions=1, status='active'):
        reservation = Reservation(
            student_id=student.id,
            listing_id=listing.id,
            portions=portions,
            pickup_code=Reservation.generate_pickup_code(),
            status=status,
        )
        db.session.add(reservation)
        db.session.commit()
        return reservation

    return _make_reservation
