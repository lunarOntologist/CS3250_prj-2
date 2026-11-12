from app import app, db
from app.models import Listing, User, Reservation
from app.forms import PostListingForm, SignUpForm, LoginForm, PickupForm
from datetime import datetime, timezone
from flask import abort, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt
from sqlalchemy import select

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignUpForm()
    error = None
    if form.validate_on_submit():
        # check if email is taken
        if User.query.filter_by(email=form.email.data).first():
            error = 'That email is already registered'
        else:
            hashed_passwd = bcrypt.hashpw(form.passwd.data.encode('utf-8'), bcrypt.gensalt())
            new_user = User(name=form.name.data, email=form.email.data, passwd=hashed_passwd, role=form.role.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html', form=form, error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd):
            login_user(user)
            return redirect(url_for('home'))
        error = 'Wrong email or password'
    return render_template('login.html', form=form, error=error)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/home')
@login_required
def home():
    # each role gets its own home page
    if current_user.role == 'vendor':
        return render_template('vendor_home.html')
    return render_template('student_home.html')

@app.route('/listings')
@login_required
def listings():
    if current_user.role != 'student':
        abort(403)

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    available_listings = (
        Listing.query
        .filter(
            Listing.pickup_end >= now,
            Listing.portions_total > Listing.portions_reserved,
            Listing.cancelled.is_(False),
        )
        .order_by(Listing.pickup_end.asc(), Listing.id.asc())
        .all()
    )
    return render_template('listings.html', listings=available_listings)

@app.route('/listings/new', methods=['GET', 'POST'])
@login_required
def new_listing():
    if current_user.role != 'vendor':
        abort(403)

    form = PostListingForm()
    if form.validate_on_submit():
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        if form.pickup_end.data < form.pickup_start.data:
            form.pickup_end.errors.append('Pickup window end must be after its start.')
        elif form.pickup_end.data <= now:
            form.pickup_end.errors.append('Pickup window end must be in the future.')
        else:
            listing = Listing(
                vendor_id=current_user.id,
                title=form.title.data,
                description=form.description.data,
                portions_total=form.portions_total.data,
                pickup_location=form.pickup_location.data,
                dietary_tags=form.dietary_tags.data,
                pickup_start=form.pickup_start.data,
                pickup_end=form.pickup_end.data,
            )
            db.session.add(listing)
            db.session.commit()
            return redirect(url_for('home'))

    return render_template('listing_form.html', form=form)


@app.route('/listings/<int:listing_id>/reserve', methods=['POST'])
@login_required
def reserve_portions(listing_id):
    if current_user.role != 'student':
        abort(403)

    listing = Listing.query.get_or_404(listing_id)

    # Check if student already holds an active reservation for this listing
    existing_reservation = Reservation.query.filter_by(
        student_id=current_user.id,
        listing_id=listing.id,
        status='active'
    ).first()

    if existing_reservation:
        flash("You already have an active reservation for this listing.", "danger")
        return redirect(url_for('listings'))

    # Get and validate requested portions (must be 1 or 2)
    try:
        requested_portions = int(request.form.get('portions', 1))
        if requested_portions not in (1, 2):
            raise ValueError
    except ValueError:
        flash("Invalid portion count requested. Please select 1 or 2 portions.", "danger")
        return redirect(url_for('listings'))

    # Handle race condition / capacity check atomically using row lock (with_for_update)
    listing = db.session.query(Listing).filter_by(id=listing_id).with_for_update().first()
    remaining_portions = listing.portions_total - listing.portions_reserved

    if requested_portions > remaining_portions:
        flash("Not enough portions remaining for this listing.", "danger")
        db.session.rollback()
        return redirect(url_for('listings'))

    # Create reservation and update listing portions
    code = Reservation.generate_pickup_code()
    new_reservation = Reservation(
        student_id=current_user.id,
        listing_id=listing.id,
        portions=requested_portions,
        pickup_code=code,
        status='active'
    )

    listing.portions_reserved += requested_portions
    db.session.add(new_reservation)
    db.session.commit()

    flash(f"Reservation successful! Your pickup code is: {code}", "success")
    return redirect(url_for('listings'))

@app.route('/vendor/listings')
@login_required
def manage_listings():
    if current_user.role != 'vendor':
        abort(403)

    vendor_listings = (
        Listing.query
        .filter_by(vendor_id=current_user.id)
        .order_by(Listing.pickup_end.asc())
        .all()
    )

    mark_no_shows()
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    return render_template(
        'vendor_listings.html',
        listings=vendor_listings,
        now=now
    )

@app.route('/vendor/listings/<int:listing_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_listing(listing_id):
    listing = Listing.query.filter_by(id=listing_id).first_or_404()
    # vendors can only edit their own listings
    if listing.vendor_id != current_user.id:
        abort(403)
    form = PostListingForm(obj=listing) if request.method == 'GET' else PostListingForm()
    if form.validate_on_submit():
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        if form.pickup_end.data < form.pickup_start.data:
            form.pickup_end.errors.append('Pickup window end must be after its start.')
        elif form.pickup_end.data <= now:
            form.pickup_end.errors.append('Pickup window end must be in the future.')
        elif form.portions_total.data < listing.portions_reserved:
            form.portions_total.errors.append('Total portions cannot be less than reserved portions.')
        else:
            
                listing.title = form.title.data
                listing.description = form.description.data
                listing.portions_total = form.portions_total.data
                listing.pickup_location = form.pickup_location.data
                listing.dietary_tags = form.dietary_tags.data
                listing.pickup_start = form.pickup_start.data
                listing.pickup_end = form.pickup_end.data
                
                db.session.add(listing)
                db.session.commit()
                return redirect(url_for('home'))
        
    return render_template('listing_form.html', form=form)

@app.route('/vendor/listings/<int:listing_id>/cancel', methods=['GET', 'POST'])
@login_required
def cancel_listing(listing_id):
    current_listing = Listing.query.filter_by(id=listing_id).first_or_404()
    # vendors can only cancel their own listings
    if current_listing.vendor_id != current_user.id:
        abort(403)
    rstmt = select(Reservation).where(Reservation.listing.has(Listing.id == listing_id))
    reservations = db.session.scalars(rstmt).all()
    # mark as cancelled instead of deleting so it still shows up for the vendor and students
    for reservation in reservations:
        if reservation.status == 'active':
            reservation.status = 'cancelled'
    current_listing.cancelled = True
    db.session.commit()
        
    return redirect(url_for('home'))


def mark_no_shows():
    # reservations still active after the pickup window ended become no-shows
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    late = Reservation.query.join(Listing).filter(
        Reservation.status == 'active',
        Listing.pickup_end < now,
    ).all()
    for r in late:
        r.status = 'no-show'
    if late:
        db.session.commit()

@app.route('/vendor/pickup', methods=['GET', 'POST'])
@login_required
def confirm_pickup():
    if current_user.role != 'vendor':
        abort(403)

    mark_no_shows()
    form = PickupForm()
    error = None
    picked_up = None
    if form.validate_on_submit():
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        code = form.code.data.strip().upper()
        r = Reservation.query.filter_by(pickup_code=code).first()
        if not r:
            error = 'No reservation has that code.'
        elif r.listing.vendor_id != current_user.id:
            error = "That code is for another vendor's listing."
        elif r.status == 'picked_up':
            error = 'That code was already used.'
        elif r.status == 'cancelled':
            error = 'That reservation was cancelled.'
        elif r.status == 'no-show':
            error = 'The pickup window for that reservation has ended.'
        elif now < r.listing.pickup_start:
            error = "The pickup window hasn't started yet."
        else:
            r.status = 'picked_up'
            db.session.commit()
            picked_up = r

    return render_template('confirm_pickup.html', form=form, error=error, picked_up=picked_up)

