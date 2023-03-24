from flask_restx import fields
from ..auth import auth_namespace


# SIGN-UP SCHEMA MODEL
signup_model = auth_namespace.model(
    name="Sign Up User",
    model={
        "username": fields.String(required=True, description="A username"),
        "email": fields.String(required=True, description="An email"),
        "password": fields.String(required=True, description="A password")
    }
)

# USER SCHEMA MODEL
user_model = auth_namespace.model(
    name="User Details",
    model={
        "id": fields.Integer(description="A user id"),
        "username": fields.String(description="A username"),
        "email": fields.String(description="An email"),
        "is_active": fields.Boolean(description="Shows if a user is active"),
        "is_staff": fields.Boolean(description="Shows if a user is a staff"),
    }
)

# LOGIN SCHEMA MODEL
login_model = auth_namespace.model(
    name="Login User",
    model={
        "email": fields.String(required=True, description="An email"),
        "password": fields.String(required=True, description="A password")
    }
)
