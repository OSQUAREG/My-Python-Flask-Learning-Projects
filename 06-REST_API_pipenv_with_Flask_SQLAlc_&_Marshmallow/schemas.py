from flask_marshmallow import Marshmallow
from app import app


# Init marshmallow
ma = Marshmallow(app)

# Product Schema
class ProductSchema(ma.Schema): #using marshmallow schema
    class Meta:
        fields = ("id", "name", "description", "price", "qty")

# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)