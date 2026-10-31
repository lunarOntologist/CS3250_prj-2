from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, ValidationError

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


class FoodForm(FlaskForm):
    name = StringField('Food Type', validators=[DataRequired](message='Type of food being posted is required') )
    description = StringField('Description')
    location =  StringField('Location', validators=[DataRequired](message='Location of food required.'))
    tags = StringField('Tags')
    portions = IntegerField('Number of Portions', validators=[DataRequired](message='Number of portions required')) 
    starttime = DateTimeField("Time window start", format='%H:%M', validators=[DataRequired](message = 'Please input a start time'))
    endtime = DateTimeField("Time window end", format='%H:%M', validators=[DataRequired](message = 'Please input an end time'))

    def validate_endtime(self, field):
        if self.starttime.data and field.data:
            if field.data <= self.starttime.data:
                raise ValidationError('End time must be after the start time.')
