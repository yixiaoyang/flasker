from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, Length

class LoginForm(FlaskForm):
    title = ''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',  validators=[DataRequired()])

class RegisterForm(FlaskForm):
    title = ''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Password must match')
    ])
    confirm = PasswordField('Repeat Password')
    email = StringField('Email Address', [Email(), Length(min=6, max=64)])
