from app import app, db
from app.models import User
from app.forms import SignUpForm, LoginForm
from flask import render_template, redirect, url_for
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

#TODO create an html page for food posting creation
