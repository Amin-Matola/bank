from datetime import datetime
#import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


#---------------------Connect SQLAlchemy with APP, Where this models will be imported-----------------
db                      = SQLAlchemy(app)                
#-------------------------------------------Users------------------------------------------------------
class User(UserMixin,db.Model):
    __tablename__       = 'Users'
    id                  = db.Column(db.Integer,primary_key=True)
    fname               = db.Column(db.String(50))
    lname               = db.Column(db.String(50))
    pnumber             = db.Column(db.Integer,unique=True)
    email               = db.Column(db.String(100),unique=True)
    pin                 = db.Column(db.Text)
    country             = db.Column(db.String(50))
    cur                 = db.Column(db.String(3))

    def get_id(self):
        return self.email



#-------------------------------------------Accounts----------------------------------------------------

class Account(db.Model):
    __tablename__       = 'Accounts'
    id                  = db.Column(db.Integer,primary_key=True)
    accNumber           = db.Column(db.Integer,unique=True)
    accName             = db.Column(db.String(50))
    openDate            = db.Column(db.DateTime,default=datetime.now())
    balance             = db.Column(db.Float,default=50.0)
    u_id                = db.Column(db.Integer,db.ForeignKey('Users.id'))
    accHolder           = db.relationship('User',foreign_keys=u_id,cascade='all,delete-orphan',single_parent=True)

#------------------------------------ Lets deposit some money------------------------------------------
class Deposit(db.Model):
    __tablename__       = 'Deposits'
    id                  = db.Column(db.Integer,primary_key=True)
    dname               = db.Column(db.String(50))
    dpnumber            = db.Column(db.Integer)
    demail              = db.Column(db.String(100))
    daddr               = db.Column(db.Text)
    accName             = db.Column(db.Text)
    accNum              = db.Column(db.Integer)
    ammount             = db.Column(db.Integer)
    dsignature          = db.Column(db.Text)
    ddate               = db.Column(db.DateTime,default=datetime.now())

#-----------------------------------Another transaction here, withdraws -------------------------------------------

class Withdraw(db.Model):
    __tablename__       = 'Withdraws'
    id                  = db.Column(db.Integer,primary_key=True)
    ac_id               = db.Column(db.Integer,db.ForeignKey('Accounts.id'))
    account             = db.relationship('Account',foreign_keys=ac_id)
    u_id                = db.Column(db.Integer,db.ForeignKey('Users.id'))
    withdrawer          = db.relationship('User',foreign_keys=u_id)
    ammount             = db.Column(db.Float)
