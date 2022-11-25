#website pages

from flask import Blueprint, render_template
from . import db
from .models import ItemsListed
pages = Blueprint('pages',__name__)

@pages.route('/',methods=['GET','POST'])
def home():
    
    itemsList = ItemsListed.query.order_by(ItemsListed.time)
    return render_template("home.html",items=itemsList)