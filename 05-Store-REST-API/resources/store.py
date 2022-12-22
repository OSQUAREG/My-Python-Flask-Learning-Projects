from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from schemas import StoreSchema, StoreUpdateSchema
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

# Blueprint are used to register info in the API documentation for routes.
blueprint = Blueprint("Store", __name__, description="Operations on Stores")

"""
@blueprint.arguments decorator for passing the request schema used to pass in the JSON data. Used mostly in "post" and "update" method.

@blueprint.response decorator for passing the response schema used to retrieve the JSON data. Used mostly in "get" method.

@jwt_required decorator is used to authenticate or restrict access to only logged in users. This checks for a JWT access token created when the user logged in. This can be passed into the Auth tab/section in apps used for API test such as in Insomnia, Postman etc.
"""

@blueprint.route("/store")
class StoreList(MethodView):
    # Create Store Data
    @jwt_required()  # to check authentication token before access
    @blueprint.arguments(StoreSchema)
    @blueprint.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)  # create an instance of the Model and pass in the store data.

        # save store data to database
        try:
            db.session.add(store)  # add store to DB
            db.session.commit()  # save or commit changes to DB
        except IntegrityError:
            abort(400, message="Store with that name already exist.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating store.")

        return store, 201

    # Retrieve All Store Data
    @jwt_required()  # to check authentication token before access
    @blueprint.response(200, StoreSchema(many=True))
    def get(self):
        stores = StoreModel.query.all()  # queries and return all store from the DB
        return stores


@blueprint.route("/store/<string:store_id>")
class Store(MethodView):
    # Retrieve Store Data by store_id
    @jwt_required()  # to check authentication token before access
    @blueprint.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)  # query for store by id from the DB Model
        return store

    # Delete Store Data by store_id
    @jwt_required()  # to check authentication token before access
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)  # query for store by id from the DB Model
        db.session.delete(store)  # delete the store from DB
        db.session.commit()  # save or commit changes to DB
        return {"message": "Store deleted."}

    # Update Store Data
    @jwt_required()  # to check authentication token before access
    @blueprint.arguments(StoreUpdateSchema)
    @blueprint.response(200, StoreSchema)
    def put(self, store_data, store_id):  # NB: the data collection should be first, then the id.
        store = StoreModel.query.get(store_id)  # query for store by id from the DB Model
        if store:
            store = StoreModel(**store_data)  # create an instance of the Model and pass in all the updated store_data.
            
            # # OR unpack the updated store_data one by one.
            # store.name = store_data["name"]
            # store.user_id = store_data["user_id"]
        else:
            store = StoreModel(id=store_id, **store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating store.")

        return store
