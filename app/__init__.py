from flask import Flask
from app.extensions import db, bcrypt, marsh, jwt
from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    #Initialize extensions with app
    db.init_app(app)
    marsh.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from .auth import init_auth_module
    from .expenses import init_expense_module
    init_auth_module(app)
    init_expense_module(app)


    return app