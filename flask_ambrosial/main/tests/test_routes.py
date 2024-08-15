#!/usr/bin/env python3

import unittest
from flask import Flask
from flask_ambrosial import create_app, db
from flask_ambrosial.config import TestingConfig

class MainRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ambrosial', response.data)  # Check for the title or any unique identifier

    def test_about_route(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About', response.data)

if __name__ == '__main__':
    unittest.main()
