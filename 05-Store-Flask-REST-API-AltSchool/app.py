from flask import Flask
from flask_smorest import Api
from resources import store_blueprint, item_blueprint, user_blueprint
from db import db
import os
from flask_jwt_extended import JWTManager  # for managing user authentication/access
from datetime import timedelta


def create_app(db_url=None):
    # db_url: for when your db is located elsewhere, you enter the db url.
    
    # Init app
    app = Flask(__name__)
    
    # OPenAPI Config for API URL
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Store REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # SQLAlchemy Config for API db
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Init db
    db.init_app(app)

    # JWT Config for API Authentication
    app.config["JWT_SECRET_KEY"] = "my-super-secret-key-1234567890"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)    
    jwt = JWTManager(app)

    # @app.before_first_request
    # def create_tables():
    with app.app_context():
        db.create_all()
    
    # Init API Blueprint
    api = Api(app)

    # Registering Blueprints
    api.register_blueprint(store_blueprint)
    api.register_blueprint(item_blueprint)
    api.register_blueprint(user_blueprint)

    return app
