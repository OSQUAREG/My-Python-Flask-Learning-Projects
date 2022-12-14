from app import app, db
from flask import request
from models import Product
from schemas import product_schema, products_schema


# Create a Product
@app.route("/product/", methods=["POST"])
def add_product():
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    qty = request.json["qty"]

    # instantiating the Product class model
    new_product = Product(name, description, price, qty)

    # adding it to the database
    db.session.add(new_product)
    db.session.commit()

    # using the product_schema to return the product in json format
    return product_schema.jsonify(new_product)


# Retrieve All Products
@app.route("/product", methods=["GET"])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


# Retrieve a Product
@app.route("/product/<int:pdt_id>", methods=["GET"])
def get_product(pdt_id):
    product = Product.query.get_or_404(pdt_id)
    return product_schema.jsonify(product)


# Update a Product
@app.route("/product/<int:pdt_id>", methods=["PUT"])
def update_product(pdt_id):
    product = Product.query.get_or_404(pdt_id)

    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    qty = request.json["qty"]

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()
    
    return product_schema.jsonify(product)


# Retrieve a Product
@app.route("/product/<int:pdt_id>", methods=["DELETE"])
def delete_product(pdt_id):
    product = Product.query.get_or_404(pdt_id)
    db.session.delete(product)
    db.session.commit()
    
    return product_schema.jsonify(product)