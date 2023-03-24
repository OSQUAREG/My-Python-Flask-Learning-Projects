from flask_jwt_extended import create_access_token
from . import UnitTestCase
from ..models.orders import Order, OrderSizes


def get_auth_token_headers(identity):
    token = create_access_token(identity=identity)
    headers = {"Authorization": f"Bearer {token}"}
    return headers


class OrderTestCase(UnitTestCase):
    # testing get all order route
    def test_gel_all_orders(self):
        response = self.client.get(
            "/orders/", headers=get_auth_token_headers("testuser")
        )
        assert response.status_code == 200

        # to assert that returned data is empty coz we have not created any order yet
        assert response.json == []

    # testing create order route
    def test_create_order(self):
        data = {
            "size": "MEDIUM",
            "quantity": 2,
            "flavour": "Chicken Suya",
        }

        response = self.client.post(
            "/orders/", headers=get_auth_token_headers("testuser"), json=data
        )
        # to assert the response code
        assert response.status_code == 201

        # to assert the order details created
        orders = Order.query.all()
        assert len(orders) == 1
        assert response.json["size"] == "OrderSizes.MEDIUM"
        assert response.json["quantity"] == 2
        assert response.json["flavour"] == "Chicken Suya"

    # testing get one order route
    def test_get_order_by_id(self):
        # to create a test order in the test database
        order = Order(
            size="MEDIUM",
            quantity=2,
            flavour="Chicken Suya",
        )
        order.save()

        # to get the order id
        order_id = order.id

        response = self.client.get(
            f"/orders/{order_id}", headers=get_auth_token_headers("testuser")
        )
        # to assert the response code
        assert response.status_code == 200
        # to asert number of orders
        orders = Order.query.all()
        assert len(orders) == 1
        # to assert order details
        assert response.json["size"] == "OrderSizes.MEDIUM"
        assert response.json["quantity"] == 2
        assert response.json["flavour"] == "Chicken Suya"
        assert response.json["status"] == "OrderStatus.PENDING"

    def test_order_not_found(self):
        order_id = 2

        response = self.client.get(
            f"/orders/{order_id}", headers=get_auth_token_headers("testuser")
        )
        # to assert the response code
        assert response.status_code == 404
        assert (
            response.json["error"] == "Not Found"
        )  # the customized error in the error handler for 404.
