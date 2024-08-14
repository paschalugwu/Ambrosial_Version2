#!/usr/bin/env python3

import unittest
from flask import Flask
from flask.testing import FlaskClient
from flask_ambrosial.errors.handlers import errors

class TestErrorHandlers(unittest.TestCase):

    def setUp(self):
        """Set up a Flask application for testing."""
        self.app = Flask(__name__)
        self.app.register_blueprint(errors)
        self.client = self.app.test_client()

    def test_error_404(self):
        """Test the 404 error handler."""
        @self.app.route('/nonexistent')
        def nonexistent_route():
            return "This route does not exist", 404

        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404.html', response.data)

    def test_error_403(self):
        """Test the 403 error handler."""
        @self.app.route('/forbidden')
        def forbidden_route():
            return "Forbidden", 403

        response = self.client.get('/forbidden')
        self.assertEqual(response.status_code, 403)
        self.assertIn(b'403.html', response.data)

    def test_error_500(self):
        """Test the 500 error handler."""
        @self.app.route('/error')
        def error_route():
            raise Exception("Internal Server Error")

        response = self.client.get('/error')
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'500.html', response.data)

if __name__ == '__main__':
    unittest.main()
