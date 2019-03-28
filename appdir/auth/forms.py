from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, InputRequired, Length
from appdir.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Please enter the username'),Length(min=5,max=12)])
    password = PasswordField('Password', validators=[DataRequired('Please enter the password'), Length(min=8,max=25)])
    submit = SubmitField('Sign in')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Please enter the username'),Length(min=5,max=12)])
    email = StringField('Email', validators=[DataRequired('Please enter the email'), Email('Not a valid Email')])
    first_name =  StringField('First name', validators=[DataRequired('Please enter your first name')])
    last_name =  StringField('Last name', validators=[DataRequired('Please enter your last name')])
    password = PasswordField('Password', validators=[DataRequired('Please enter the password'), Length(min=8,max=25)])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired('Please enter the password'), Length(min=8, max=25),
     EqualTo('password','Password Mismatch')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email is already taken')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.lower()).first()
        if user is not None:
            raise ValidationError('This username is already taken')