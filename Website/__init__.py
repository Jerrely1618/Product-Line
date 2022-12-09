#Settings: configure the website from here 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

DB_NAME= "database.db"
db = SQLAlchemy()



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'devPassword'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
    db.init_app(app)
    
    from .directory import pages
    from .auth import verify_page
    
    app.register_blueprint(pages,url_prefix = '/')
    app.register_blueprint(verify_page,url_prefix = '/')
    
    from .models import Users,UserApplication,Items as ItemsListed
    
    with app.app_context():
        db.create_all()
    
    return app
        