from smtplib import SMTP_SSL
from email.message import Message
# from xhtml2pdf import pisa
# from StringIO import StringIO
# from bs4 import Beautifulsoup

import urllib
from datetime import datetime
import os
from flask import Flask,render_template,request,redirect,url_for,send_file,jsonify,session
from flask_login import current_user,login_user,LoginManager
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename

connection             = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username='xxxxxxxx',
    password='xxxxxxxx',
    hostname='thehosttodatabase.com',
    databasename='bank',
    )
    

app.config["SQLALCHEMY_DATABASE_URI"]       = connection
app.config["DEBUG"]                         = True
app.config["UPLOAD_FOLDER"]                 = "/path/to/store/static/files"
app.config["SQLALCHEMY_POOL_RECYCLE"]       = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True
#db                                          = sqlalchemy.create_engine(connection)
db                                          = SQLAlchemy(app)
secret                                      = os.urandom(682)
app.secret_key                              = secret

lmanager                                    = LoginManager()
lmanager.init_app(app)
