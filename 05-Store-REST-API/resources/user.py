from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from schemas import UserSchema, UserUpdateSchema, UserStoreItemSchema
from models import UserModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# Blueprint are used to register info in the API for multiple routes in a class
blueprint = Blueprint("User", __name__, description="Operations on Users")


@blueprint.route("/user")
class UserList(MethodView):
    # Create User
    @blueprint.arguments(UserSchema)
    @blueprint.response(200, UserSchema)
    def post(self, user_data):
        user = UserModel(**user_data)

        # save user data to database
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message="User with that name already exist.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating user.")

        return user, 201

    # Retrieve All User
    @blueprint.response(200, UserSchema(many=True, exclude=("password",)))
    def get(self):
        return UserModel.query.all()


@blueprint.route("/user/<string:user_id>")
class User(MethodView):
    # Retrieve User by user_id
    @blueprint.response(200, UserStoreItemSchema(exclude=("password",)))
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    # Delete user Data by user_id
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "user deleted."}

    # Update user Data
    @blueprint.arguments(UserUpdateSchema)
    @blueprint.response(200, UserSchema)
    def put(self, user_data, user_id): # NB: the data collection should be first, then the id.
        user = UserModel.query.get(user_id)
        if user:
            user.name = user_data["name"]
            user.username = user_data["username"]
            user.password = user_data["password"]
        else:
            user = UserModel(id=user_id, **user_data)

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating user.")

        return user
