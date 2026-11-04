from app import app, db
from app.models import Listing, User
from app.forms import PostListingForm, SignUpForm, LoginForm
from datetime import datetime, timezone
from flask import abort, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt

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
        elif form.pickup_end.data <= now.strftime('%Y-%m-%d %H:%M:%S'):
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
