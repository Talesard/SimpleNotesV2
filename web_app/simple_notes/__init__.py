from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'the random string'

login_manager = LoginManager(app)
db = SQLAlchemy(app)
db.create_all()

from simple_notes.helpers import linebreaks, linebreaksbr
from simple_notes import models, routes
