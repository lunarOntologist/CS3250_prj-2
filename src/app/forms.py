from flask_wtf import FlaskForm
from wtforms import (
    DateTimeLocalField,
    IntegerField,
    PasswordField,
    RadioField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from datetime import datetime

class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message='Name is required')])
    email = StringField('Email', validators=[DataRequired(message='Email is required')])
    passwd = PasswordField('Password', validators=[DataRequired(message='Password is required'), Length(min=8, message='Password must be at least 8 characters')])
    role = RadioField('Role', choices=[('student', 'Student'), ('vendor', 'Vendor')], validators=[DataRequired(message='Role is required')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Email is required')])
    passwd = PasswordField('Password', validators=[DataRequired(message='Password is required')])
    submit = SubmitField('Login')

class PostListingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message='Title is required')])
    description = TextAreaField('Description', validators=[DataRequired(message='Description is required')])
    portions_total = IntegerField(
        'Number of portions',
        validators=[
            DataRequired(message='Number of portions is required'),
            NumberRange(min=1, max=100, message='Portions must be between 1 and 100'),
        ],
    )
    pickup_location = StringField(
        'Pickup location',
        validators=[DataRequired(message='Pickup location is required')],
    )
    dietary_tags = SelectMultipleField(
        'Dietary tags',
        choices=[
            ('vegetarian', 'Vegetarian'),
            ('vegan', 'Vegan'),
            ('gluten-free', 'Gluten-free'),
            ('halal', 'Halal'),
            ('contains nuts', 'Contains nuts'),
        ],
    )
    pickup_start = DateTimeLocalField(
        'Pickup window start',
        format='%Y-%m-%dT%H:%M:%S',
        validators=[DataRequired(message='Pickup window start is required')],
    )
    pickup_end = DateTimeLocalField(
        'Pickup window end',
        format='%Y-%m-%dT%H:%M:%S',
        validators=[DataRequired(message='Pickup window end is required')],
    )
    submit = SubmitField('Post')
