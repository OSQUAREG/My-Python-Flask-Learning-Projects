from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# Blueprint are used to register info in the API for multiple routes in a class
blueprint = Blueprint("Item", __name__, description="Operations on Items")


@blueprint.route("/item")
class ItemList(MethodView):
    # Create Item Data
    @blueprint.arguments(ItemSchema)
    @blueprint.response(200, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        # save item data to database
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Item with that name already exist.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating item.")

        return item, 201

    # Retrieve All Item Data
    @blueprint.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()


@blueprint.route("/item/<int:item_id>")
class Item(MethodView):
    # Retrieve Item Data by item_id
    @blueprint.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    # Delete Item by item_id
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    # Update Item Data
    @blueprint.arguments(ItemUpdateSchema)
    @blueprint.response(200, ItemSchema)
    def put(self, item_data, item_id): # NB: the data collection should be first, then the id.
        item = ItemModel.query.get(item_id)
        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
            item.store_id = item_data["store_id"]
        else:
            item = ItemModel(id=item_id, **item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating item.")

        return item
