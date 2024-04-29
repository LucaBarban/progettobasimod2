from flask import Flask
from .database import db
from .safety import bcrypt, csrf

def create_app() -> Flask:
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user-name:strong-password@localhost/progetto"
    app.secret_key = b'test' # TODO: spostare la chiave in un luogo decente (e renderla più sicura di così)

    bcrypt.init_app(app)
    csrf.init_app(app)

    db.init_app(app)

    with app.app_context():
        from . import routes
        from . import models
        db.create_all()

        return app
