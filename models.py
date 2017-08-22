from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    used_for = db.Column(db.String(50))
    username_used = db.Column(db.String(15))
    password_used = db.Column(db.String(80))
    date_created = db.Column(db.DateTime())
    date_updated = db.Column(db.DateTime())
