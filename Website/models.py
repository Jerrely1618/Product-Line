from . import db 
from flask_login import UserMixin


class UserApplication(db.Model):
    name = db.Column(db.String(50))
    email = db.Column(db.String(50),unique=True,primary_key = True)
    password = db.Column(db.String(50))
    address = db.Column(db.String(50),unique=True)
    phone = db.Column(db.String(50),unique=True)
    credit_card = db.Column(db.String(50),unique=True)

class Users(db.Model,UserMixin):
    name = db.Column(db.String(50))
    email = db.Column(db.String(50),unique=True,primary_key = True)
    password = db.Column(db.String(50))
    address = db.Column(db.String(50),unique=True)
    phone = db.Column(db.String(50),unique=True)
    credit_card = db.Column(db.String(50),unique=True)
    itemsSelling = db.relationship('ItemsListed')
      

class ItemsListed(db.Model):
    title = db.Column(db.String(50),primary_key = True)
    userOwnder = db.column(db.String(50),db.ForeignKey('users.email'))
    keywords = db.Column(db.String(50),unique=True)
    time = db.Column(db.String(50))
    priceRange = db.Column(db.String(50),unique=True)
