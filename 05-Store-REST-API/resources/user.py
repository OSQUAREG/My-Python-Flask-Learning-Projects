from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from schemas import UserSchema, UserUpdateSchema, UserStoreItemSchema
from models import UserModel
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from passlib.hash import pbkdf2_sha256


# Blueprint are used to register info in the API documentation for routes.
blueprint = Blueprint("User", __name__, description="Operations on Users")

"""
@blueprint.arguments for passing the request arguments using schema used to pass in the JSON data. Used mostly in "post" and "update" method.
@blueprint.response for passing the response schema used to retrieve the JSON data. Used mostly in "get" method.
"""


@blueprint.route("/register")
class UserRegister(MethodView):
    # Create/Register User
    @blueprint.arguments(UserSchema)
    # @blueprint.response(201, UserSchema)
    def post(self, user_data):
        # checking if username exist
        user_exist = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        if user_exist:
            abort(409, message = f"User with this username: {user_exist.username} already exist")

        # create an instance of the Model and pass in the user data.
        new_user = UserModel(
            name = user_data["name"],
            username = user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"])  # hashing the password
            )

        # save collected user data to database
        try:
            db.session.add(new_user)  # add user to DB
            db.session.commit()  # save or commit changes to DB
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating user.")

        """
        NB: to return user data created as below in JSON format, you need to pass in a reposnse Schema into the decorator @blueprint.response() which will be used to return the user data created. 
        Hence, to use below return statement, uncomment @blueprint.response above.
        """
        # return new_user, 201
        
        """
        NB: to return just a message as below, there will be no need for the decorator @blueprint.response for returning the message. 
        Hence, to use below return statement, comment out @blueprint.response() above.
        """
        return {"message": f"User: {new_user.username} created successfully."}, 201


@blueprint.route("/login")
class UserLogin(MethodView):
    @blueprint.arguments(UserSchema(only=("username","password")))
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        # check if user exist, and if entered password in same as the saved hashed password using .verify method
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.username, fresh=True)
            refresh_token = create_refresh_token(identity=user.username)
            return {
                "message": f"User: {user.username} login successfully.",
                "access_token": access_token, 
                "refresh_token": refresh_token
                    }
        
        abort(401, message="Invalid credentials.")


"""
Once a user successfully logs in, the JWT create_access_token creates an access token which the user uses to be able to access routes where the decorator @jwt_required() is added.
"""

"""
Once the access token is expired, the refresh token is used to refresh and set another instance of the token instead of login in again. Also note that, the refresh token usually takes longer time to expire than the access token it self.
"""

@blueprint.route("/refresh")        
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"refresh_token": new_token}


@blueprint.route("/user")
class UserList(MethodView):
    # Retrieve All User
    @blueprint.response(200, UserSchema(many=True))
    def get(self):
        users = UserModel.query.all()  # queries and return all users from the DB
        return users


@blueprint.route("/user/<string:user_id>")
class User(MethodView):
    # Retrieve User by user_id
    @blueprint.response(200, UserStoreItemSchema(exclude=("password",)))
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)  # query for user by id from the DB Model
        return user

    # Delete user Data by user_id
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)  # query for user by id from the DB Model
        db.session.delete(user)  # delete the user from DB
        db.session.commit()  # save or commit changes to DB
        return {"message": f"User: {user.username} deleted."}, 200

    # Update user Data
    @blueprint.arguments(UserUpdateSchema)
    @blueprint.response(200, UserSchema)
    def put(
        self, user_data, user_id
    ):  # NB: the data collection should be first, then the id.
        user = UserModel.query.get(user_id)  # query for user by id from the DB Model
        if user:
            # user = UserModel(**user_data)  # create an instance of the Model and pass in all the updated user_data.
            
            # # OR unpack the updated user_data one by one.
            password_hash = pbkdf2_sha256.hash(user_data["password"])
            user.name = user_data["name"]
            user.username = user_data["username"]
            user.password = password_hash
        else:
            user = UserModel(id=user_id, **user_data)

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating user.")

        return user
