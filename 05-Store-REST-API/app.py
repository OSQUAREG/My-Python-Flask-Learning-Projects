from flask import Flask
from flask_smorest import Api
from resources import store_blueprint, item_blueprint, user_blueprint
from db import db
import os


def create_app(db_url=None):
    # db_url: for when your db is located elsewhere, you enter the db url.
    # Init app
    app = Flask(__name__)
    # OPenAPI Config for API URL
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Store REST API"
    # assert isinstance(app.config, app)
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # SQLAlchemy Config for db
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Init db
    db.init_app(app)

    # @app.before_first_request
    # def create_tables():
    with app.app_context():
        db.create_all()

    # Init API Blueprint
    api = Api(app)
    api.register_blueprint(store_blueprint)
    api.register_blueprint(item_blueprint)
    api.register_blueprint(user_blueprint)

    return app
