from flask import Flask
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'the random string'
app.config['ADMIN_USERNAMES'] = ["admin"]

login_manager = LoginManager(app)
db = SQLAlchemy(app)
from simple_notes import models, routes
db.create_all()
moment = Moment(app)

from simple_notes.helpers import linebreaks, linebreaksbr

