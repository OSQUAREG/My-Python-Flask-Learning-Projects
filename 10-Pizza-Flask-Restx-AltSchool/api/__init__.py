"""
NOTE: With Flask RestX, it automatically configures our swagger UI, unlike Flask REST.
"""

from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .orders.views import orders_namespace
from .config.config import config_dict
from .utils import db
from .models.users import User
from .models.orders import Order
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed, Unauthorized


def create_app(config=config_dict["dev"]):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    jwt = JWTManager(app)

    migrate = Migrate(app, db)

    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add a JWT token to the header with: <Bearer {JWT token}> to authorize.",
        }
    }

    api = Api(
        app=app,
        title="Pizza Delivery Service RESTX API",
        description="A simple Pizza delivery API service",
        version="1.0",
        authorizations=authorizations,
        security="Bearer Auth",
        errors=Flask.errorhandler,
    )

    jwt._set_error_handler_callbacks(api)

    # adding namespaces to API
    api.add_namespace(auth_namespace, path="/auth")
    api.add_namespace(orders_namespace, path="/orders")

    # error handlers
    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, 404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method Not Allowed"}, 405

    @api.errorhandler(Unauthorized)
    def unauthorized(error):
        return {"error": "Not Unauthorized"}, 401

    # adding shell context processor
    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "User": User,
            "Order": Order,
        }

    """
    this allows us run the database context in the shell (terminal) by running: 
    $ flask shell
    $ db -to check the db uri path
    $ User -to check the user model class
    $ Order -to check the order model class
    $ db.create_all() -to create the db.sqlite3 file in the uri path.   
    
    ...and because we set SQLALCHEMY_ECHO = True it displays all the logic that was used to create the db.
    """

    return app


"""
Exporting FLASK_APP in terminal...

For Bash (Linux, Mac, Windows [Git Bash]): export FLASK_APP=api/
For Command Prompt (Windows): set FLASK_APP=api/
For PowerShell (Windows): $env:FLASK_APP="api/"
"""
