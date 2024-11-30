# coding: utf-8

from __future__ import absolute_import

from safekeeper.tests import BaseTestCase


class BaseTestAliveController(BaseTestCase):
    def test_get_alive(self):
        response = self.client.open("/ping", method="GET")
        self.assertIsNotNone(response.status_code)


if __name__ == "__main__":
    import unittest

    unittest.main()
