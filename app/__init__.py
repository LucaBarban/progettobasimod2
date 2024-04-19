from flask import Flask

from .database import db

def create_app() -> Flask:
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
    db.init_app(app)

    with app.app_context():
        from . import routes
        from . import models
        db.create_all()

        return app
