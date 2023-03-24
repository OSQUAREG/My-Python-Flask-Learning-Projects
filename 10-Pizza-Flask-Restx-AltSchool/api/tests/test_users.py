from . import UnitTestCase
from ..models.users import User


class UserTestCase(UnitTestCase):
    # testing the sign-up route
    def test_user_registration(self):

        data = {
            "username": "testuser",
            "email": "testuser@test.com",
            "password": "password",
        }

        # assert the route response status
        response = self.client.post("/auth/signup", json=data)
        assert response.status_code == 201

        # to assert that username exist in the database
        user = User.query.filter_by(email="testuser@test.com").first()
        assert user.username == "testuser"

    # testing the login route
    def test_user_login(self):
        data = {"email": "testuser@test.com", "password": "password"}

        response = self.client.post("/auth/login", json=data)
        assert response.status_code == 200
