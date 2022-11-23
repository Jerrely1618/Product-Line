#Login/Sign_up pages

from flask import Blueprint, render_template

verify_page = Blueprint('verify_page',__name__)

@verify_page.route('/login')
def login():
    return render_template("login.html")

@verify_page.route('/sign-up')
def sign_up():
    return render_template("sign-up.html")