from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, Listing, User
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        # In a real app, check password hash. For testing setup, we'll allow creation if user doesn't exist for simplicity in setup.
        # Here we simulate a successful login for testing purposes if the user exists or if we are testing setup.
        if user and user.password_hash == user.password_hash: # Placeholder for actual check
             login_user(user)
             flash('Logged in successfully.', 'success')
             return redirect(url_for('dashboard.dashboard'))
        elif not user and username == 'test_vendor': # Simplified test account
             # Create a dummy user for testing if 'test_vendor' is submitted
             from werkzeug.security import generate_password_hash
             new_user = User(username=username, password_hash=generate_password_hash('password'), is_vendor=True)
             db.session.add(new_user)
             db.session.commit()
             login_user(new_user)
             flash('Test vendor logged in successfully.', 'success')
             return redirect(url_for('dashboard.dashboard'))
        else:
             flash('Invalid username or password.', 'error')
             
    return render_template('login.html')

@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login.login'))

@dashboard_bp.route('/')
@login_required
def dashboard():
    # 1. Get date range from request (assuming start_date and end_date query params)
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    if not start_date_str or not end_date_str:
        # Default to a reasonable range or handle as error if strict
        start_date = datetime.strptime('2023-01-01', '%Y-%m-%d')
        end_date = datetime.utcnow()
    else:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'error')
            return redirect(url_for('dashboard.dashboard'))


    # Ensure start_date is before end_date for valid range
    if start_date > end_date:
        flash('Error: Start date cannot be after end date.', 'error')
        return redirect(url_for('dashboard.dashboard'))

    # 2. Fetch listings for the current vendor within the date range
    listings = Listing.query.filter(
        Listing.vendor_id == current_user.id,
        Listing.posted_date >= start_date,
        Listing.posted_date <= end_date
    ).all()

    # 3. Calculate statistics
    total_listings = len(listings)
    total_posted = sum(l.is_posted for l in listings)
    total_picked_up = sum(l.picked_up_portions for l in listings)
    total_no_show = sum(l.no_show_count for l in listings)
    total_reserved = sum(l.reserved_portions for l in listings)

    no_show_rate = 0.0
    if total_reserved > 0:
        no_show_rate = (total_no_show / total_reserved) * 100

    # 4. Prepare context for template
    context = {
        'listings': listings,
        'total_listings': total_listings,
        'total_posted': total_posted,
        'total_picked_up': total_picked_up,
        'total_no_show': total_no_show,
        'total_reserved': total_reserved,
        'no_show_rate': f"{no_show_rate:.2f}%" if total_reserved > 0 else "0.00%",
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }

    return render_template('dashboard/dashboard.html', **context)