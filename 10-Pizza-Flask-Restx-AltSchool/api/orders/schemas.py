from flask_restx import fields
from ..auth.schemas import user_model
from ..orders import orders_namespace  # Namespace instantiated in auth/__init__.py

# CREATE ORDER SCHEMA MODEL
create_order_model = orders_namespace.model(
    name="Create Order",
    model={
        "size": fields.String(
            required=True,
            description="Size of pizza to order",
            enum=["SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"],
        ),
        "flavour": fields.String(
            required=True, description="Flavour of pizza to order"
        ),
        "quantity": fields.Integer(
            required=False, description="Flavour of pizza to order"
        ),
    },
)

# ORDER DETAILS SCHEMA MODEL
order_details_model = orders_namespace.model(
    name="Order Details",
    model={
        "message": fields.String(description="Execution Message", default="Executed successfully!"),
        "id": fields.Integer(descriptoin="An Order Id"),
        "size": fields.String(
            description="Size of pizza ordered",
            enum=["SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"],
        ),
        "flavour": fields.String(description="Flavour of pizza ordered"),
        "quantity": fields.Integer(description="Flavour of pizza ordered"),
        "status": fields.String(
            description="Status of the order",
            enum=["PENDING", "IN_TRANSIT", "DELIVERED"],
        ),
        "date_created": fields.DateTime(description="Date of order creation"),
        # "customer": fields.Nested(user_model, description="Details of the customer"),
    },
)

# UPDATE ORDER DETAILS SCHEMA MODEL
update_order_model = orders_namespace.model(
    name="Update Order Details",
    model={
        "size": fields.String(
            description="Size of pizza ordered",
            enum=["SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"],
        ),
        "flavour": fields.String(description="Flavour of pizza ordered"),
        "quantity": fields.Integer(description="Flavour of pizza ordered"),
        "status": fields.String(
            description="Status of the order",
            enum=["PENDING", "IN_TRANSIT", "DELIVERED"],
        ),
    },
)

# UPDATE ORDER STATUS SCHEMA MODEL
update_order_status_model = orders_namespace.model(
    name="Update Order Status",
    model={
        "status": fields.String(
            required=True,
            description="Status of the order",
            enum=["PENDING", "IN_TRANSIT", "DELIVERED"],
        ),
    },
)
