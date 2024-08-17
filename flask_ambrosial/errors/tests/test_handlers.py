#!/usr/bin/env python3

"""
Unit tests for error handlers in the Flask application.
"""

import unittest
from flask import Flask
from flask.testing import FlaskClient
from flask_ambrosial.errors.handlers import errors

class TestErrorHandlers(unittest.TestCase):
    """
    Test case for custom error handlers.
    """

    def setUp(self):
        """
        Set up a Flask application for testing.
        """
        self.app = Flask(__name__)
        self.app.register_blueprint(errors)
        self.client = self.app.test_client()

    def test_error_404(self):
        """
        Test the 404 error handler.
        """
        @self.app.route('/nonexistent')
        def nonexistent_route():
            return "Oops. Page Not Found (404)", 404

        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Oops. Page Not Found (404)', response.data)

    def test_error_403(self):
        """
        Test the 403 error handler.
        """
        @self.app.route('/forbidden')
        def forbidden_route():
            return "You don't have permission to do that (403)", 403

        response = self.client.get('/forbidden')
        self.assertEqual(response.status_code, 403)
        self.assertIn(
            b"You don't have permission to do that (403)", response.data
        )

    def test_error_500(self):
        """
        Test the 500 error handler.
        """
        @self.app.route('/error')
        def error_route():
            return (
                "We are experiencing some trouble on our end. "
                "Please try again in the near future", 500
            )

        response = self.client.get('/error')
        self.assertEqual(response.status_code, 500)
        self.assertIn(
            b'We are experiencing some trouble on our end. '
            b'Please try again in the near future', response.data
        )

if __name__ == '__main__':
    unittest.main()
