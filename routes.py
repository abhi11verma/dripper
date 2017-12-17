from flask import Flask , render_template

from flask import Flask, url_for, redirect, \
    render_template, session, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, \
    logout_user, current_user, UserMixin
    
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError
import os
from model import db


class Auth:
    """Google Project Credentials"""
    CLIENT_ID = ('277221696598-s7qbeuqfpj9u0ghkc0tqd2v3t23ksfcl.apps.googleusercontent.com')
    CLIENT_SECRET = 'TYrqMTwgCoH-1fJLRBFXAtix'
    REDIRECT_URI = 'https://127.0.0.1:5000/loginsuccess'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = ['profile', 'email']


def get_google_auth(state=None, token=None):
        if token:
            return OAuth2Session(Auth.CLIENT_ID, token=token)
        if state:
            return OAuth2Session(
                Auth.CLIENT_ID,
                state=state,
                redirect_uri=Auth.REDIRECT_URI)
        oauth = OAuth2Session(
            Auth.CLIENT_ID,
            redirect_uri=Auth.REDIRECT_URI,
            scope=Auth.SCOPE)
        return oauth

class Config:
    """Base config"""
    APP_NAME = "Test Google Login"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "somethingsecret"
class DevConfig(Config):
    """Dev config"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/drip'

config = {
    "dev": DevConfig,
    "default": DevConfig
}

app = Flask(__name__)

app.config.from_object(config['dev'])

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(
        Auth.AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    return render_template('login.html', auth_url=auth_url)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)


