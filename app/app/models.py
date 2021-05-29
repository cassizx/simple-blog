import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash
import sqlalchemy_utils
from sqlalchemy import UniqueConstraint
from app import db


# from ..app import bcrypt

# db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    __table_args__ = (db.UniqueConstraint('username', 'email'),)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(128))
    email = db.Column(sqlalchemy_utils.EmailType, unique=True, nullable=False)
    is_email_confirmed = db.Column(db.Boolean(), default=False)
    avatar = db.Column(db.String(200), default='1.png')
    about = db.Column(db.String(200))
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    live_country = db.Column(db.String(60))
    live_city = db.Column(db.String(60))



    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        # self._password =  generate_password_hash(password)
        self._password =  generate_password_hash(password).decode('utf-8')
        # self.password = _set_password(password)


    # @hybrid_property
    # def password(self):
    #     return self._password


    # @password.setter
    # def _set_password(self, plaintext):
    #     self._password = bcrypt.generate_password_hash(plaintext)

    def is_authenticated(self):
        return True

    def is_correct_password(self, plaintext):
        return check_password_hash(self._password, plaintext)

    def __repr__(self):
        return f'<id {self.id}> <username {self.username}>'


class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner = db.Column(db.String(64), db.ForeignKey('user.username'))
    body = db.Column(db.String(900))
    image_url = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)



class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender = db.Column(db.String(64), db.ForeignKey('user.username'))
    message_text = db.Column(db.String(600))
    sending_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Direct_Messages(db.Model):
    __tablename__ = 'direct_messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender = db.Column(db.String(64), db.ForeignKey('user.username'))
    recipient = db.Column(db.String(64), db.ForeignKey('user.username'))
    text = db.Column(db.String(600))
    sending_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)