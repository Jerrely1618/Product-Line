from . import db 
from flask_login import UserMixin
from datetime import datetime

class Transaction_buyer(db.Model):
    seller = db.Column(db.String)
    title = db.Column(db.String,primary_key=True)
    buyer = db.Column(db.String,db.ForeignKey('users.token'))
    time = db.Column(db.DateTime,default=datetime.utcnow)
    buyer_name = db.Column(db.String)
    seller_name = db.Column(db.String)
    
    
class Transaction_seller(db.Model):
    buyer = db.Column(db.String)
    title = db.Column(db.String,primary_key=True)
    seller = db.Column(db.String,db.ForeignKey('users.token'))
    time = db.Column(db.DateTime,default=datetime.utcnow)
    buyer_name = db.Column(db.String)
    seller_name = db.Column(db.String)
    
class UserApplication(db.Model):
    name = db.Column(db.String(50))
    email = db.Column(db.String(50),unique=True,primary_key = True)
    password = db.Column(db.String(50))
    address = db.Column(db.String(50))
    phone = db.Column(db.String(50),unique=True)
    time = db.Column(db.DateTime,default=datetime.utcnow)
    credit_card = db.Column(db.String(50))
    
class ItemsApplication(db.Model):
    title = db.Column(db.String(50),unique=True,primary_key = True)
    keywords = db.Column(db.String(50))
    time = db.Column(db.DateTime,default=datetime.utcnow)
    img = db.Column(db.Text)
    priceRange = db.Column(db.String(50))
    user = db.Column(db.String,db.ForeignKey('users.token'))

class Complaints(db.Model,UserMixin):
    user = db.Column(db.String(50),db.ForeignKey('users.token'))
    description = db.Column(db.String(50),primary_key=True)
    user_complainer = db.Column(db.String)
    
class Reports(db.Model,UserMixin):
    title = db.Column(db.String,db.ForeignKey('items.title'))
    description = db.Column(db.String,primary_key=True)
    user_complainer = db.Column(db.String)

class Items(db.Model):
    title = db.Column(db.String(50),unique=True,primary_key = True)
    img = db.Column(db.Text)
    keywords = db.Column(db.String(50))
    time = db.Column(db.DateTime,default=datetime.utcnow)
    price = db.Column(db.String)
    user_bidder = db.Column(db.String)
    reports = db.relationship('Reports')
    user = db.Column(db.String,db.ForeignKey('users.token'))
    
class Users(db.Model,UserMixin):
    token = db.Column(db.String,unique=True,primary_key=True)
    super = db.Column(db.Boolean,unique=False,default=False)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(50))
    address = db.Column(db.String(50))
    phone = db.Column(db.String(50),unique=True)
    credit_card = db.Column(db.String(50))
    rating = db.Column(db.Integer,default = 0)
    balance = db.Column(db.Integer,default = 0)
    sales = db.relationship("Transaction_seller")
    purchases = db.relationship("Transaction_buyer")
    items = db.relationship('Items')
    complaints = db.relationship('Complaints')
    

    

    
    
