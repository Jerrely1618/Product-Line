#Login/Sign_up pages

from flask import Blueprint

verify_page = Blueprint('verify_page',__name__)

@verify_page.route('/login')
def login():
    return "<p>Login<p>"

@verify_page.route('/sign-up')
def sign_up():
    return "<p> sign up <p>"