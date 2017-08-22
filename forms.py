from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(),
                                                   Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(),
                                                     Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegistrationForm(FlaskForm):
    email = EmailField('email', validators=[InputRequired(),
                                            Email(message='Invalid Email'),
                                            Length(max=50)])
    username = StringField('username', validators=[InputRequired(),
                                                   Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(),
                                                     Length(min=8, max=80)])


class AccountForm(FlaskForm):
    website = StringField('for website?', validators=[InputRequired()])
    username_used = StringField('your username used?',
                                validators=[InputRequired()])
    password_used = StringField('your password used?',
                                validators=[InputRequired()])
