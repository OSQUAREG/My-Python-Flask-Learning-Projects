from flask import request
from flask_restx import Namespace, Resource, fields
from http import HTTPStatus
from ..models.users import User
from ..models.orders import Order
from flask_jwt_extended import jwt_required, get_jwt_identity, get_current_user
from ..orders.schemas import create_order_model, order_details_model, update_order_model, update_order_status_model
from ..orders import orders_namespace
from ..utils import db

"""
admin access
login user access restriction
"""


@orders_namespace.route("/")
class CreateGetOrders(Resource):

    # Creating an order
    @orders_namespace.expect(create_order_model)
    @orders_namespace.marshal_with(order_details_model)
    # @orders_namespace.marshal_with(order_model)
    @orders_namespace.doc(
        description="Create/place an order",
        params=dict()
    )
    @jwt_required()
    def post(self):
        """
        Create/Place an Order
        """
        data = orders_namespace.payload
        # payload (like the request.get_json) returns all the data entered by the user
        # but unlike get_json, it includes additional input not required in the schema.

        # get data and store in variables
        size = data["size"]
        flavour = data["flavour"]
        quantity = data["quantity"]

        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()

        new_order = Order(
            size=size,
            flavour=flavour,
            quantity=quantity,
            # # you can assign customer_id like this...
            # customer_id=current_user.id
        )

        # OR assign customer to current_user like this...
        new_order.customer = current_user

        new_order.save()

        return new_order, HTTPStatus.CREATED

    # Getting all orders
    @orders_namespace.marshal_with(order_details_model)
    @orders_namespace.doc(
        description="Get all orders from database.",
        responses={"body": "Order list details"},
    )
    @jwt_required()
    def get(self):
        """
        Get all Orders
        """
        orders = Order.query.all()

        return orders, HTTPStatus.OK


@orders_namespace.route("/<int:order_id>")
@orders_namespace.doc(
    params={"order_id": "An Id for an Order"},
)
class GetUpdateDeleteOrder(Resource):

    # Get Single Order Route
    @orders_namespace.marshal_with(order_details_model)
    @orders_namespace.doc(
        description="Get an order by giving an order Id",
        responses={"body": "Order details"},
    )
    @jwt_required()
    def get(self, order_id):
        """
        Get an Order by Id
        """
        order = Order.get_by_id(order_id)

        return order, HTTPStatus.OK

    # Put/Update Order Route
    @orders_namespace.expect(update_order_model)
    @orders_namespace.marshal_list_with(order_details_model)
    @orders_namespace.doc(
        description="Update an order by giving an order Id",
        responses={"body": "Updated Order details"},
    )
    @jwt_required()
    def put(self, order_id):
        """
        Update an Order by Id
        """
        order = Order.get_by_id(order_id)

        # to ensure customers only update their own order.
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()

        if user.id == order.customer_id:

            data = orders_namespace.payload

            order.size = data["size"]
            order.quantity = data["quantity"]
            order.flavour = data["flavour"]

            db.session.commit()
            return order, HTTPStatus.OK

        response = {"message": "You are not authorized to update this order"}
        return response, HTTPStatus.UNAUTHORIZED

    # Delete Order Route
    @orders_namespace.doc(description="Delete an order by giving an order Id")
    @jwt_required()
    def delete(self, order_id):
        """
        Delete an Order by Id
        """
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        order = Order.get_by_id(order_id)

        # to ensure customers only deletes their own order.
        if user.id == order.customer_id:
            order.delete()

            response = {"message": f"Order: {order.id}, deleted successfully"}
            return response, HTTPStatus.OK

        response = {"message": "You are not authorized to delete this order"}
        return response, HTTPStatus.UNAUTHORIZED


# Get Specific Order By User Route
@orders_namespace.route("/user/<int:user_id>/order/<int:order_id>/")
class GetSpecificOrderByUser(Resource):
    @orders_namespace.marshal_with(order_details_model)
    @orders_namespace.doc(
        description="Get a specific order by giving an user Id and an order Id",
        params={
            "order_id": "An Id for an order",
            "user_id": "An Id for a User",
        },
        responses={"body": "Order details"},
    )
    @jwt_required()
    def get(self, user_id, order_id):
        """
        Get a Specific Order by User
        """
        user = User.get_by_id(user_id)
        order = Order.query.filter_by(id=order_id).filter_by(customer=user).first()

        return order, HTTPStatus.OK


# Get All Orders By User Route
@orders_namespace.route("/user/<int:user_id>/orders")
class GetAllOrdersByUser(Resource):
    @orders_namespace.marshal_with(order_details_model)
    @orders_namespace.doc(
        description="Get all orders by giving an user Id",
        params={"user_id": "An Id for an User"},
        responses={"body": "User Orders list details"},
    )
    @jwt_required()
    def get(self, user_id):
        """
        Get all Orders by User
        """
        # list of user orders by Id
        user = User.get_by_id(user_id)

        user_orders = user.orders

        # # OR
        # user_orders = Order.query.filter_by(customer=user).all()

        # # OR
        # user_orders = Order.query.filter_by(customer_id=user.id).all()

        # # OR
        # user_orders = Order.query.filter(Order.customer==user).all()

        return user_orders, HTTPStatus.OK


# Patch/Update Order Route
@orders_namespace.route("/<int:order_id>/status")
class UpdateOrderStatus(Resource):
    @orders_namespace.expect(update_order_status_model)
    @orders_namespace.marshal_with(order_details_model)
    @orders_namespace.doc(
        description="Update an order status by giving an order Id",
        params={"order_id": "An Id for an Order"},
        responses={"body": "Order details with Updated Status"},
        enum=["PENDING", "IN_TRANSIT", "DELIVERED"],
    )
    @jwt_required()
    def patch(self, order_id):
        """
        Update an Order Status
        """
        order = Order.get_by_id(order_id)

        # to ensure customers only update their own order status.
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()

        if user.id == order.customer_id:

            data = orders_namespace.payload
            order.status = data["status"]
            order.update()

            # # OR

            # data = request.get_json()
            # order.status = data.get("status")
            # order.update()

            # # OR

            # data = request.get_json()
            # order.update_status_with_get_json(data)

            # # OR

            # data = orders_namespace.payload
            # order.update_status_with_payload(data)

            return order, HTTPStatus.OK

        response = {"message": "You are not authorized to update this order status"}
        return response, HTTPStatus.UNAUTHORIZED
