#website pages

from flask import Blueprint, render_template,request
from . import db
from .models import ItemsListed


pages = Blueprint('pages',__name__)

@pages.route('/',methods=['GET','POST'])
def home():
    if request.method=="POST":
        # image = request.files['img']
        # for i in range(10):
        #     title = "NewObj"+str(i)
        #     desc = "red beautiful"
        #     priceRange = "56-98"
        #     newItem = ItemsListed(title=title,keywords=desc,priceRange=priceRange,img=image.read())
        #     db.session.add(newItem)
        #     db.session.commit()
        searchItem = request.form["searchItem"]
        itemsList = ItemsListed.query.filter_by(title=searchItem).order_by(ItemsListed.time)
        if itemsList.count() == 0:
            itemsListWord = ItemsListed.query.order_by(ItemsListed.time)
            for item in itemsListWord:
                if searchItem in item.keywords:
                    return render_template("home.html",items=itemsListWord)
        return render_template("home.html",items=itemsList,inputSearch=searchItem)
    itemsList = ItemsListed.query.order_by(ItemsListed.time)
    return render_template("home.html",items=itemsList)