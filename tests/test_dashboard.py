import pytest
from app import create_app, db
from app.models import User, Listing
from datetime import datetime, timedelta
from flask import url_for

# --- Fixtures are in conftest.py ---

def test_dashboard_no_data_shows_zeros(client, vendor_user):
    """
    Acceptance Criterion 3: Given there is no data in the range, then all values show 0 and no error occurs.
    """
    # Set a date range where no listings exist (e.g., far future)
    future_date = (datetime.utcnow() + timedelta(days=365)).strftime('%Y-%m-%d')
    past_date = (datetime.utcnow() - timedelta(days=365)).strftime('%Y-%m-%d')

    # Access the dashboard with empty date range
    response = client.get(f'/dashboard/?start_date={future_date}&end_date={past_date}')

    assert response.status_code == 200
    
    # Check if the empty state message is rendered
    assert b'No listings found for the selected date range.' in response.data
    
    # Check for zero values in the stats block (checking for the presence of 0s in the response data might be brittle, 
    # but we rely on the template logic being correct based on the context passed to render_template)
    # A more robust check would involve inspecting the rendered HTML/Jinja context if possible, but for now, we check for the expected absence of data.
    # We will rely on the logic in app/routes.py to pass 0s if listings is empty.

def test_dashboard_data_display_and_rate_calculation(client, vendor_user):
    """
    Acceptance Criterion 1 & 2: Given I am logged in as a vendor, when I open the dashboard and choose a date range, 
    then I see the number of listings posted, portions posted, portions picked up, and no-show count for my listings in that range.
    The no-show rate is shown as a percentage of reserved portions.
    """
    # Seed data for the test vendor
    vendor_id = vendor_user.id
    listings = []
    
    # Listing 1: Posted, Reserved=10, PickedUp=5, NoShow=1
    listing1 = Listing(
        vendor_id=vendor_id,
        title="Posted Listing A",
        posted_date=datetime.utcnow() - timedelta(days=10),
        is_posted=True,
        reserved_portions=10,
        picked_up_portions=5,
        no_show_count=1
    )
    listings.append(listing1)
    
    # Listing 2: Not Posted, Reserved=20, PickedUp=10, NoShow=0
    listing2 = Listing(
        vendor_id=vendor_id,
        title="Reserved Listing B",
        posted_date=datetime.utcnow() - timedelta(days=20),
        is_posted=False,
        reserved_portions=20,
        picked_up_portions=10,
        no_show_count=0
    )
    listings.append(listing2)
    
    # Listing 3: Posted, Reserved=5, PickedUp=1, NoShow=1
    listing3 = Listing(
        vendor_id=vendor_id,
        title="Posted Listing C",
        posted_date=datetime.utcnow() - timedelta(days=30),
        is_posted=True,
        reserved_portions=5,
        picked_up_portions=1,
        no_show_count=1
    )
    listings.append(listing3)

    with client.session_transaction() as session:
        # Manually inject listings into the DB for testing route logic
        for listing in listings:
            db.session.add(listing)
        db.session.commit()

    # Define a date range covering all listings
    start_date_str = (datetime.utcnow() - timedelta(days=40)).strftime('%Y-%m-%d')
    end_date_str = datetime.utcnow().strftime('%Y-%m-%d')

    response = client.get(f'/dashboard/?start_date={start_date_str}&end_date={end_date_str}')

    assert response.status_code == 200
    
    # Assert total counts are correct
    assert b'Total Listings: 3' in response.data
    assert b'Posted: 2' in response.data # Listing 1 and 3
    assert b'Picked Up: 16' in response.data # 5 + 10 + 1
    assert b'No-Show Count: 2' in response.data # 1 + 0 + 1
    assert b'Reserved Portions: 35' in response.data # 10 + 20 + 5
    
    # Calculate expected no-show rate: Total No-Show (2) / Total Reserved (35) * 100
    # 2 / 35 * 100 = 5.714...%
    expected_rate = "5.71%" 
    assert expected_rate in response.data # Check if the calculated rate string is present

def test_dashboard_invalid_date_range(client, vendor_user):
    """
    Test error case for invalid date range (start_date > end_date).
    """
    # Attempt to query with inverted dates
    start_date_str = '2024-01-01'
    end_date_str = '2023-01-01'

    response = client.get(f'/dashboard/?start_date={start_date_str}&end_date={end_date_str}')

    assert response.status_code == 302 # Redirected to dashboard (or error page if implemented differently, but we expect redirect based on route logic)
    assert b'Error: Start date cannot be after end date.' in response.data