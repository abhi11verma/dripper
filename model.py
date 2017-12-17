from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, \
    logout_user, current_user, UserMixin
import datetime

db = SQLAlchemy()

""" DB Models """
class User(db.Model, UserMixin):
    __tablename__ = "user"
    userid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200))
    tokens = db.Column(db.Text)
    account_created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
