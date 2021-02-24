# models.py

from flask_login import UserMixin
from . import db

#this is the information that will be placed into the sqlAlchemy
#turns the class into a column in a data set

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    #email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    Address_1=db.Column(db.String(1000))
    Address_2 = db.Column(db.String(1000))
    City= db.Column(db.String(1000))
    State=db.Column(db.String(2))
    Zip = db.Column(db.String(9))