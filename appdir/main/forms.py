from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, InputRequired, Length

class ComposeForm(FlaskForm):
    username = SelectField('Send to:', coerce=int, validators=[InputRequired('Please select a username')])
    content = StringField('Message', widget=TextArea(), validators=[DataRequired('Please enter the message'), Length(max=50)])
    submit = SubmitField('Send Message')

class DbdumpForm(FlaskForm):
    submit = SubmitField('Download Database')

