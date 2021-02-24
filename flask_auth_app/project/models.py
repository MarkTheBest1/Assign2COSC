from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    #address1 = db.Column(db.String(100))
    #address2 = db.Column(db.String(100))
    #city = db.Column(db.String(100))
    #state = db.Column(db.String(100))
    #zipcode = db.Column(db.String(9))