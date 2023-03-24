from flask import request
from flask_restx import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from http import HTTPStatus
from ..models.users import User
from ..auth import auth_namespace
from ..auth.schemas import signup_model, login_model, user_model


@auth_namespace.route("/signup")
class SignUp(Resource):

    @auth_namespace.expect(signup_model)  # to get data using the schema
    @auth_namespace.marshal_with(user_model)  # to return the data using the schema
    @auth_namespace.doc(description="Register a User")
    def post(self):
        """
        Sign-up a User
        """
        # set data passed in JSON format using the signup_model schema
        data = request.get_json()
        # data = {"username": "user1", "email": "user1@gmail.com", "password": "password"}

        # gets each data and store in variables.
        username = data.get("username")
        email = data.get("email")
        password_hash = generate_password_hash(data.get("password"))

        # instantiate User model as new_user
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )

        # use the User class method .save() to save and commit to DB
        new_user.save()

        # to return the new user data.
        return new_user, HTTPStatus.CREATED

        # # to use this return statement, comment out the @auth_namespace.marshal_with()
        # return {"message": "User created successfully!"}, HTTPStatus.CREATED


@auth_namespace.route("/login")
class Login(Resource):

    @auth_namespace.expect(login_model)
    @auth_namespace.doc(description="Login to Generate JWT token")
    def post(self):
        """
        Generate JWT Token
        """
        # to get the data passed in JSON format using the login_model schema
        data = request.get_json()

        # gets each data and store in a variable
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if (user is not None) and (check_password_hash(pwhash=user.password_hash, password=password)):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)

            response = {
                "message": "Login successful!",
                "access_token": access_token,
                "refresh_token": refresh_token
            }

            return response, HTTPStatus.CREATED


@auth_namespace.route("/refresh")
class Refresh(Resource):

    @auth_namespace.doc(description="Create a Refresh Token")
    @jwt_required(refresh=True)
    def post(self):
        """
        Create Refresh Token
        """
        username = get_jwt_identity()

        access_token = create_access_token(identity=username)

        response = {
                "message": "Refresh successful!",
                "access_token": access_token,
            }

        return response, HTTPStatus.OK


@auth_namespace.route("/users")
class GetUsers(Resource):

    @auth_namespace.marshal_with(user_model)
    @auth_namespace.doc(description="Get all Users")
    @jwt_required()
    def get(self):
        """
        Get all Users
        """
        users = User.query.all()

        return users, HTTPStatus.OK


@auth_namespace.route("/user/<int:user_id>")
class GetUser(Resource):

    @auth_namespace.marshal_with(user_model)
    @auth_namespace.doc(description="Get a User by Id")
    @jwt_required()
    def get(self, user_id):
        """
        Get a User by Id
        :param user_id: id of a user
        :return: user with the id
        """
        user = User.get_by_id(user_id)

        return user, HTTPStatus.OK
