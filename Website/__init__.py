#Settings: configure the website from here 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

app = Flask(__name__)
db = SQLAlchemy(app)

DB_NAME= "database.db"

def create_app():
    app.config['SECRET_KEY'] = 'devPassword'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .directory import pages
    from .auth import verify_page
    
    app.register_blueprint(pages,url_prefix = '/')
    app.register_blueprint(verify_page,url_prefix = '/')
    
    from .models import Users,UserApplication,ItemsListed
    
    if not path.exists('Website/'+DB_NAME):
        db.create_all()
    
    return app
    
        