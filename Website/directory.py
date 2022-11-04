#website pages

from flask import Blueprint

pages = Blueprint('pages',__name__)

@pages.route('/')
def home():
    return "<a href=\"/login\" target=\"_blank\">This is a link</a>"