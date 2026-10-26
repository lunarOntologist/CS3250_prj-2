from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length

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
