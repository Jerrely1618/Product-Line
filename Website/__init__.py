#Settings: configure the website from here 
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'devPassword'
    from .directory import pages
    from .auth import verify_page
    
    app.register_blueprint(pages,url_prefix = '/')
    app.register_blueprint(verify_page,url_prefix = '/')
    
    return app