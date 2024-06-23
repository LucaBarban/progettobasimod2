import os

from flask import Flask

from .database import db
from .safety import bcrypt, csrf


def create_app() -> Flask:
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
    app.secret_key = os.environ["SECRET_KEY"].encode()
    app.config["WTF_CSRF_CHECK_DEFAULT"] = False
    app.config["UPLOAD_FOLDER"] = "app/static/covers/"

    bcrypt.init_app(app)
    csrf.init_app(app)

    db.init_app(app)

    with app.app_context():
        from . import models, routes

        db.create_all()

        return app
