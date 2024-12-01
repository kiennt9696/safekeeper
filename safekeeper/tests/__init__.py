import unittest

from flask import Flask

from safekeeper.controllers.healthz import is_alive


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the Flask app for testing
        self.app = Flask(__name__)
        self.app.testing = True
        self.client = self.app.test_client()

        # Register routes for testing with uniquely named view functions
        def is_alive_view():
            return is_alive()

        self.app.add_url_rule("/ping", view_func=is_alive_view, methods=["POST"])
