import unittest

from flask import current_app
from .. import create_app
from ..config.config import config_dict
from ..utils import db


class UnitTestCase(unittest.TestCase):
    # called before each test
    def setUp(self):
        self.app = create_app(config=config_dict["test"])
        self.app_ctxt = self.app.app_context()
        self.app_ctxt.push()
        # using a test client
        self.client = self.app.test_client()
        db.create_all()

    # called after each test case
    def tearDown(self):
        db.drop_all
        self.app_ctxt.pop()
        self.app = None
        self.client = None

    # def test_app(self):
    #     assert self.app is not None
    #     assert current_app == self.app
