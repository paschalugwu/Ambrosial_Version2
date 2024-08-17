#!/usr/bin/env python3

"""
This module contains unit tests for the API routes of the Flask application.
"""

import unittest
from flask import Flask
from flask_ambrosial.apis.api_routes import api_bp

class TestApiRoutes(unittest.TestCase):
    """
    Unit tests for the API routes.
    """

    def setUp(self):
        """
        Set up a Flask test client.
        """
        self.app = Flask(__name__)
        self.app.register_blueprint(api_bp)
        self.client = self.app.test_client()

    def test_get_organizer_data_status_code(self):
        """
        Test that the status code of the response is 200.
        """
        response = self.client.get('/api/organizer')
        self.assertEqual(response.status_code, 200)

    def test_get_organizer_data_structure(self):
        """
        Test that the JSON response has the correct structure.
        """
        response = self.client.get('/api/organizer')
        data = response.get_json()
        self.assertIn('event_calendar', data)
        self.assertIn('weather_forecast', data)
        self.assertIn('location_services', data)

    def test_get_organizer_data_content(self):
        """
        Test that the JSON response contains the expected content.
        """
        response = self.client.get('/api/organizer')
        data = response.get_json()
        self.assertEqual(data['event_calendar'], [])
        self.assertEqual(data['weather_forecast'], '')
        self.assertEqual(data['location_services'], '')

if __name__ == '__main__':
    unittest.main()
