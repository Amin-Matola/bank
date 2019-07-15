#---------------------------------------Bank Operations with Python-------------------------
#---------------------------------------LAST TOUCHED BY: AMIN MATOLA------------------------
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

#----------------------------------------Set Databse Connection ----------------------------------
connection             = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username='xxxxxxxx',
    password='xxxxxxxx',
    hostname='thehosttodatabase.com',
    databasename='bank',
    )
    
#-----------------------------------------Configure the app as I like ------------------------------
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

#----------------------------------- Now invite the models ---------------------------------------------
from models import *
#---------------------------------- Manage the users logins first ---------------------------------------
@lmanager.user_loader
def load_user(mail, target='user'):
    #--------In my usage, there are two systems running simultaneously, so I choose the target at time---
    if target == 'user':
        return User.query.filter_by(email=mail).first()
    elif target == 'other':
        return Other.query.filter_by(email=mail).first()
    else:
        return False
#---------------------------------- Now the core logic ------------------------------------------------










