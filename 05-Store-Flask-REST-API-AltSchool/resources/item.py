from flask.views import MethodView  # the MethodView is used to assign a multiple method to a route. 
from flask_smorest import Blueprint, abort  # flask-smorest is the Flask API framework used.
from db import db
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

# Blueprint are used to register info in the API documentation for routes.
blueprint = Blueprint("Item", __name__, description="Operations on Items")

"""
@blueprint.arguments decorator for passing the request schema used to pass in the JSON data. Used mostly in "post" and "update" method.

@blueprint.response decorator for passing the response schema used to retrieve the JSON data. Used mostly in "get" method.

@jwt_required decorator is used to authenticate or restrict access to only logged in users. This checks for a JWT access token created when the user logged in. This can be passed into the Auth tab/section in apps used for API test such as in Insomnia, Postman etc.
"""


@blueprint.route("/item")
class ItemList(MethodView):
    # Create Item
    @jwt_required()  # to check authentication token before access
    @blueprint.arguments(ItemSchema) 
    @blueprint.response(200, ItemSchema) 
    def post(self, item_data):
        item = ItemModel(**item_data)  # create an instance of the Model and pass in the item data.

        # save item data to database
        try:
            db.session.add(item)  # add item to DB
            db.session.commit()  # save or commit changes to DB
        except IntegrityError:
            abort(400, message="Item with that name already exist.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating item.")

        return item, 201

    # Retrieve All Item
    @blueprint.response(200, ItemSchema(many=True))
    def get(self):
        items = ItemModel.query.all()  # queries and return all item from the DB
        return items


@blueprint.route("/item/<int:item_id>")
class Item(MethodView):
    # Retrieve Item Data by item_id
    @jwt_required()  # to check authentication token before access
    @blueprint.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)  # query for item by id from the DB Model
        return item

    # Delete Item by item_id
    @jwt_required()  # to check authentication token before access
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)  # query for item by id from the DB Model
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    # Update Item Data
    @jwt_required()  # to check authentication token before access
    @blueprint.arguments(ItemUpdateSchema)
    @blueprint.response(200, ItemSchema)
    def put(self, item_data, item_id): # NB: the data collection should be first, then the id.
        item = ItemModel.query.get(item_id)  # query for item by id from the DB Model
        if item:
            item = ItemModel(**item_data)  # create an instance of the Model and pass in all the updated item_data.

            # # OR unpack the updated item_data one by one.
            # item.name = item_data["name"]
            # item.price = item_data["price"]
            # item.store_id = item_data["store_id"]
        else:
            item = ItemModel(id=item_id, **item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating item.")

        return item
