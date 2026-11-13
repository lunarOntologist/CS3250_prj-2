import pytest
from app import create_app, db
from app.models import User, Listing
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime, timedelta

@pytest.fixture(scope='function')
def app():
    # Use an in-memory SQLite database for testing
    app = create_app(config_object='testing') # Assuming a 'testing' config exists or default setup works for in-memory DB
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
    
    yield app

    # Teardown
    with app.app_context():
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    # Configure Flask-Login for testing
    from flask_login import TestClientMixin
    
    # Setup a test user
    with app.app_context():
        user = User(username='test_vendor', password_hash='dummy_hash', is_vendor=True)
        db.session.add(user)
        db.session.commit()
        
    client = app.test_client()
    
    # Manually log in the test user for authenticated tests
    with client.session_transaction() as session:
        user = User.query.filter_by(username='test_vendor').first()
        if user:
            from flask_login import login_user
            login_user(user)
            yield client
        else:
            pytest.fail("Test user setup failed.")

@pytest.fixture(scope='function')
def vendor_user(client):
    # Returns the ID of the logged-in vendor for use in tests
    with client.session_transaction() as session:
        user = User.query.filter_by(username='test_vendor').first()
        assert user is not None
        yield user

# Helper function to seed data
def seed_listings(db, vendor_id, num_listings=5):
    listings = []
    for i in range(num_listings):
        listing = Listing(
            vendor_id=vendor_id,
            title=f"Listing {i}",
            posted_date=datetime.utcnow() - timedelta(days=i*2),
            is_posted=(i % 2 == 0),
            reserved_portions=10 + i,
            picked_up_portions=i // 2,
            no_show_count=i // 3
        )
        db.session.add(listing)
        listings.append(listing)
    db.session.commit()
    return listings

def seed_no_data(db, vendor_id):
    # Ensure no listings exist for this vendor
    listings = Listing.query.filter_by(vendor_id=vendor_id).all()
    for listing in listings:
        db.session.delete(listing)
    db.session.commit()
