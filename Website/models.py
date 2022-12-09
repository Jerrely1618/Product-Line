from . import db 
from flask_login import UserMixin
from datetime import datetime


class UserApplication(db.Model):
    name = db.Column(db.String(50))
    email = db.Column(db.String(50),unique=True,primary_key = True)
    password = db.Column(db.String(50))
    address = db.Column(db.String(50))
    phone = db.Column(db.String(50),unique=True)
    credit_card = db.Column(db.String(50))
    
class ItemsApplication(db.Model):
    title = db.Column(db.String(50),unique=True,primary_key = True)
    keywords = db.Column(db.String(50))
    time = db.Column(db.String(50))
    priceRange = db.Column(db.String(50))

class Complaints(db.Model,UserMixin):
    user = db.Column(db.String(50),db.ForeignKey('users.email'))
    description = db.Column(db.String(50),primary_key=True)
    user_complainer = db.Column(db.String)
    
class Reports(db.Model,UserMixin):
    title = db.Column(db.String,db.ForeignKey('items.title'))
    description = db.Column(db.String,primary_key=True)
    user_complainer = db.Column(db.String)

class Items(db.Model):
    title = db.Column(db.String(50),unique=True,primary_key = True)
    keywords = db.Column(db.String(50))
    time = db.Column(db.DateTime,default=datetime.utcnow)
    price = db.Column(db.String)
    img = db.Column(db.Text)
    userBidder = db.Column(db.String)
    reports = db.relationship('Reports')
    user = db.Column(db.String,db.ForeignKey('users.email'))
    
class Users(db.Model,UserMixin):
    name = db.Column(db.String(50))
    email = db.Column(db.String(50),unique=True,primary_key=True)
    password = db.Column(db.String(50))
    address = db.Column(db.String(50))
    phone = db.Column(db.String(50),unique=True)
    credit_card = db.Column(db.String(50))
    items = db.relationship('Items')
    complaints = db.relationship('Complaints')
    

    

    
    
