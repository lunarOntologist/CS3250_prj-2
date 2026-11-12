import bcrypt
from datetime import datetime, timedelta, timezone
from app import db
from app.models import User, Listing

def seed():
    if User.query.first():
        return  # already has data

    pw = bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt())
    vendor = User(name='Tivoli Cafe', email='vendor@test.com', passwd=pw, role='vendor')
    student = User(name='Test Student', email='student@test.com', passwd=pw, role='student')
    db.session.add_all([vendor, student])
    db.session.commit()

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    food = [
        ('Cheese Pizza', 'Leftover large pizzas', 8, 'Tivoli Cafe', ['vegetarian']),
        ('Veggie Wraps', 'Wraps from lunch', 5, 'Student Union', ['vegan']),
        ('Chicken Rice Bowls', 'Rice bowls from the dinner line', 6, 'Tivoli Cafe', ['halal', 'gluten-free']),
    ]
    for title, desc, portions, place, tags in food:
        db.session.add(Listing(vendor_id=vendor.id, title=title, description=desc,
                               portions_total=portions, pickup_location=place, dietary_tags=tags,
                               pickup_start=now, pickup_end=now + timedelta(days=7)))
    db.session.commit()
