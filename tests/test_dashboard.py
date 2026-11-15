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
