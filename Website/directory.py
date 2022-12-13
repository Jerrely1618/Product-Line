#website pages

from flask import Blueprint, render_template,request
from . import db
from .models import Items as ItemsListed


pages = Blueprint('pages',__name__)

@pages.route('/',methods=['GET','POST'])
def home():
    if request.method=="POST":
        if "searchItem" in request.form.keys():
            searchItem = request.form["searchItem"]
            itemsList = ItemsListed.query.filter_by(title=searchItem).order_by(ItemsListed.time)
            if itemsList.count()==0:
                itemsList = ItemsListed.query.filter_by(price=searchItem).order_by(ItemsListed.time)
            if itemsList.count()==0:
                itemsList = ItemsListed.query.filter_by(keywords=searchItem).order_by(ItemsListed.time)
            return render_template("home.html",items=itemsList,inputSearch=searchItem)
    itemsList = ItemsListed.query.order_by(ItemsListed.time)
    return render_template("home.html",items=itemsList)