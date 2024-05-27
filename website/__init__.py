from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)

    # импорт переменной views
    from .views import views
    from .auth import auth
    from .articles import articles

    # регистрация blueprint-ов
    app.register_blueprint(views, url_prefix='/') # '/' - no prefix
    app.register_blueprint(auth, url_prefix='/auth/')
    app.register_blueprint(articles, url_prefix='/articles/')

    return app