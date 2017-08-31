from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate(db)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    account = db.relationship('Account', backref='owner', lazy='dynamic')


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(50), unique=True)
    username_used = db.Column(db.String(15))
    password_used = db.Column(db.String(80))
    date_created = db.Column(db.DateTime())
    date_updated = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
