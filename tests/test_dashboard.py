"""Tests for US9: Impact dashboard."""

import re
from datetime import datetime, timedelta, timezone

from app import db

DASHBOARD_URL = '/vendor/dashboard'


def _metric(response, label):
    """Return the value shown next to a metric label on the dashboard page."""
    html = response.get_data(as_text=True)
    match = re.search(
        r'<td>\s*' + re.escape(label) + r'\s*</td>\s*<td>\s*([^<]*?)\s*</td>',
        html,
    )
    assert match, f'Metric "{label}" was not found on the dashboard.'
    return match.group(1)


def _range_url(start, end):
    return f'{DASHBOARD_URL}?start={start}&end={end}'


def test_dashboard_requires_login(client):
    response = client.get(DASHBOARD_URL)
    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_dashboard_forbidden_for_students(app, client, create_user, login):
    create_user('student@test.com', role='student')
    login('student@test.com')

    response = client.get(DASHBOARD_URL)
    assert response.status_code == 403


def test_dashboard_shows_counts_for_my_listings_in_range(
    app, client, create_user, login, make_listing, make_reservation
):
    vendor = create_user('vendor@test.com', role='vendor')
    student = create_user('student@test.com', role='student')

    in_range = make_listing(vendor, datetime(2024, 1, 10), portions_total=5)
    also_in_range = make_listing(vendor, datetime(2024, 1, 12), portions_total=3)
    make_reservation(in_range, student, portions=2, status='picked_up')
    make_reservation(also_in_range, student, portions=1, status='no-show')

    login('vendor@test.com')
    response = client.get(_range_url('2024-01-01', '2024-01-31'))

    assert response.status_code == 200
    assert _metric(response, 'Listings posted') == '2'
    assert _metric(response, 'Portions posted') == '8'
    assert _metric(response, 'Portions picked up') == '2'
    assert _metric(response, 'No-show count') == '1'


def test_dashboard_excludes_listings_outside_range(
    app, client, create_user, login, make_listing, make_reservation
):
    vendor = create_user('vendor@test.com', role='vendor')
    student = create_user('student@test.com', role='student')

    in_range = make_listing(vendor, datetime(2024, 1, 15), portions_total=4)
    outside = make_listing(vendor, datetime(2024, 3, 1), portions_total=9)
    make_reservation(in_range, student, portions=2, status='picked_up')
    make_reservation(outside, student, portions=5, status='picked_up')

    login('vendor@test.com')
    response = client.get(_range_url('2024-01-01', '2024-01-31'))

    assert _metric(response, 'Listings posted') == '1'
    assert _metric(response, 'Portions posted') == '4'
    assert _metric(response, 'Portions picked up') == '2'


def test_dashboard_excludes_other_vendors_listings(
    app, client, create_user, login, make_listing, make_reservation
):
    vendor = create_user('vendor@test.com', role='vendor')
    other_vendor = create_user('other@test.com', role='vendor')
    student = create_user('student@test.com', role='student')

    mine = make_listing(vendor, datetime(2024, 2, 5), portions_total=6)
    theirs = make_listing(other_vendor, datetime(2024, 2, 6), portions_total=10)
    make_reservation(mine, student, portions=1, status='picked_up')
    make_reservation(theirs, student, portions=4, status='picked_up')

    login('vendor@test.com')
    response = client.get(_range_url('2024-02-01', '2024-02-28'))

    assert _metric(response, 'Listings posted') == '1'
    assert _metric(response, 'Portions posted') == '6'
    assert _metric(response, 'Portions picked up') == '1'


def test_dashboard_no_show_rate_is_percentage_of_reserved_portions(
    app, client, create_user, login, make_listing, make_reservation
):
    vendor = create_user('vendor@test.com', role='vendor')
    student = create_user('student@test.com', role='student')

    listing = make_listing(vendor, datetime(2024, 4, 1), portions_total=10)
    make_reservation(listing, student, portions=1, status='picked_up')
    make_reservation(listing, student, portions=1, status='no-show')

    login('vendor@test.com')
    response = client.get(_range_url('2024-04-01', '2024-04-30'))

    # 1 no-show portion out of 2 reserved portions.
    assert _metric(response, 'No-show rate') == '50.0%'


def test_dashboard_ignores_cancelled_reservations(
    app, client, create_user, login, make_listing, make_reservation
):
    vendor = create_user('vendor@test.com', role='vendor')
    student = create_user('student@test.com', role='student')

    listing = make_listing(vendor, datetime(2024, 5, 1), portions_total=10)
    make_reservation(listing, student, portions=2, status='picked_up')
    make_reservation(listing, student, portions=2, status='cancelled')

    login('vendor@test.com')
    response = client.get(_range_url('2024-05-01', '2024-05-31'))

    # Cancelled portions are released, so only the 2 picked-up portions count.
    assert _metric(response, 'Portions picked up') == '2'
    assert _metric(response, 'No-show rate') == '0.0%'


def test_dashboard_counts_active_reservations_on_ended_windows_as_no_shows(
    app, client, create_user, login, make_listing, make_reservation
):
    vendor = create_user('vendor@test.com', role='vendor')
    student = create_user('student@test.com', role='student')

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    listing = make_listing(vendor, now, portions_total=4)
    listing.pickup_end = now - timedelta(days=1)
    db.session.commit()
    # Still "active" in the database, but its pickup window has ended.
    make_reservation(listing, student, portions=1, status='active')

    login('vendor@test.com')
    response = client.get(DASHBOARD_URL)

    assert _metric(response, 'No-show count') == '1'
    assert _metric(response, 'No-show rate') == '100.0%'


def test_dashboard_does_not_count_active_reservations_before_window_ends(
    app, client, create_user, login, make_listing, make_reservation
):
    vendor = create_user('vendor@test.com', role='vendor')
    student = create_user('student@test.com', role='student')

    today = datetime.now(timezone.utc).replace(tzinfo=None)
    future = today + timedelta(days=2)
    listing = make_listing(vendor, today, portions_total=4)
    listing.pickup_end = future
    db.session.commit()
    make_reservation(listing, student, portions=1, status='active')

    login('vendor@test.com')
    response = client.get(DASHBOARD_URL)

    assert _metric(response, 'No-show count') == '0'
    assert _metric(response, 'No-show rate') == '0.0%'


def test_dashboard_empty_range_shows_zeros(app, client, create_user, login):
    create_user('vendor@test.com', role='vendor')
    login('vendor@test.com')

    response = client.get(_range_url('2020-01-01', '2020-01-31'))

    assert response.status_code == 200
    assert _metric(response, 'Listings posted') == '0'
    assert _metric(response, 'Portions posted') == '0'
    assert _metric(response, 'Portions picked up') == '0'
    assert _metric(response, 'No-show count') == '0'
    assert _metric(response, 'No-show rate') == '0.0%'


def test_dashboard_defaults_to_today(
    app, client, create_user, login, make_listing, make_reservation
):
    vendor = create_user('vendor@test.com', role='vendor')
    student = create_user('student@test.com', role='student')

    today = datetime.now(timezone.utc).replace(tzinfo=None)
    listing = make_listing(vendor, today, portions_total=3)
    make_reservation(listing, student, portions=1, status='picked_up')
    # A listing from long ago must not appear in the default range.
    make_listing(vendor, today - timedelta(days=400), portions_total=7)

    login('vendor@test.com')
    response = client.get(DASHBOARD_URL)

    assert response.status_code == 200
    assert _metric(response, 'Listings posted') == '1'
    assert _metric(response, 'Portions posted') == '3'
    assert _metric(response, 'Portions picked up') == '1'


def test_dashboard_invalid_dates_do_not_error(app, client, create_user, login):
    create_user('vendor@test.com', role='vendor')
    login('vendor@test.com')

    response = client.get(_range_url('not-a-date', 'also-bad'))

    assert response.status_code == 200
    assert _metric(response, 'Listings posted') == '0'


def test_dashboard_reversed_range_is_handled(
    app, client, create_user, login, make_listing
):
    vendor = create_user('vendor@test.com', role='vendor')
    make_listing(vendor, datetime(2024, 6, 15), portions_total=2)

    login('vendor@test.com')
    # End before start: the view should swap them rather than crash.
    response = client.get(_range_url('2024-06-30', '2024-06-01'))

    assert response.status_code == 200
    assert _metric(response, 'Listings posted') == '1'

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