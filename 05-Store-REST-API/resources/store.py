from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from schemas import StoreSchema, StoreUpdateSchema
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# Blueprint are used to register info in the API for multiple routes in a class
blueprint = Blueprint("Store", __name__, description="Operations on Stores")


@blueprint.route("/store")
class StoreList(MethodView):
    # Create Store Data
    @blueprint.arguments(StoreSchema)
    @blueprint.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        # save store data to database
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Store with that name already exist.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating store.")

        return store, 201

    # Retrieve All Store Data
    @blueprint.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()


@blueprint.route("/store/<string:store_id>")
class Store(MethodView):
    # Retrieve Store Data by store_id
    @blueprint.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    # Delete Store Data by store_id
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted."}

    # Update Store Data
    @blueprint.arguments(StoreUpdateSchema)
    @blueprint.response(200, StoreSchema)
    def put(self, store_data, store_id): # NB: the data collection should be first, then the id.
        store = StoreModel.query.get(store_id)
        if store:
            store.name = store_data["name"]
            store.user_id = store_data["user_id"]
        else:
            store = StoreModel(id=store_id, **store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating store.")

        return store
