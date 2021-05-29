import os
from logging.config import dictConfig
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash, session, make_response, g, abort
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from pathlib import Path
from flask_migrate import Migrate
from flask_mail import Mail #, Message
from flask_socketio import SocketIO #, join_room, leave_room
import sqlalchemy_utils
# from werkzeug.utils import secure_filename
#from services.models import db #, User, Posts, Messages, Direct_Messages
# from sqlalchemy.exc import DataError, IntegrityError
# from functools import wraps
# from sqlalchemy import or_, and_, asc, desc, inspect, update
# from itsdangerous import URLSafeTimedSerializer
# from flaskext.mail import Mail
# from .email import send_email
# from utils.email_confirm_tokens import generate_confirmation_token, confirm_token
# import utils.email_sender


## CONFIG
# https://519102.selcdn.ru/flask-test/lp1srLzSrp
# d270wfGWqD
BASE_DIR = Path(__file__).resolve(strict=True).parent
UPLOAD_FOLDER = "images"
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'bmp', 'webp']
UPLOAD_AVATARS_FOLDER = "avatars"


app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8zwefew\wefe5#y2L"F4Q8z#2124189@wn#ef1234w1fwefxec]/'
app.config['SECURITY_PASSWORD_SALT'] = b'_5#y2L"F4Q8zwefeexampleefe5#y2L"F4Q8zexample$example'

# DB
DB_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
DB_HOST = os.getenv('DB_HOST')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:5432/{POSTGRES_DB}"
app.config['SQLALCHEMY_POOL_SIZE'] = 100
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 150
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)


# photo
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


# mail settings
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER']= os.getenv('MAIL_DEFAULT_SENDER')
mail = Mail(app)


socketio = SocketIO(app)

# bcrypt
app.config['BCRYPT_LOG_ROUNDS '] = 12
bcrypt = Bcrypt(app)

# users = {}

# logging

dictConfig({
    'version': 1,
    'formatters': {
        'myformatter': {
            'format': '{levelname} {asctime} {module}\
                      {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        # 'file': {
        #     'level':'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'filename': 'logs/log.log',
        # },
        'console':{
            'level':'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            # 'handlers': ['file'],
            'handlers': ['console'],
            'propagate': True,
            'formatter': 'myformatter'
        }
    }
})


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


from app import auth, chats, email_sender, feed, posts, profile, models, errors_handlers


