from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os

db = SQLAlchemy()
DB_NAME = "postgresql://note_website_user:3tS4Ddk3nJUheYTGGtMCtxHO5EdrMvyg@dpg-crjuk2lds78s73eescfg-a.oregon-postgres.render.com/note_website"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'halleluja halleluja'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_NAME
    # postgresql://note_website_user:3tS4Ddk3nJUheYTGGtMCtxHO5EdrMvyg@dpg-crjuk2lds78s73eescfg-a.oregon-postgres.render.com/note_website
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Note
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
        
