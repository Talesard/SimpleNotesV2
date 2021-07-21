from datetime import datetime

from flask_login import UserMixin

from simple_notes import db


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(0), unique=True)
    password = db.Column(db.String(500), nullable=False)
    date_reg = db.Column(db.DateTime, default=datetime.utcnow)
    date_upd = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User: id: {self.id}, email: {self.email}, username: {self.username}, date: {self.date_reg}"


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.Text, nullable=False)
    detail_text = db.Column(db.Text)
    date_creat = db.Column(db.DateTime, default=datetime.utcnow)
    date_upd = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Note: id: {self.id}, user_id: {self.user_id}, title: {self.title}, date: {self.date_creat}"
