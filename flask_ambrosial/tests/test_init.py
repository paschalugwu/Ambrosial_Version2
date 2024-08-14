#!/usr/bin/env python3

import unittest
from flask import Flask, session, request
from flask_ambrosial import create_app, db, bcrypt, login_manager, mail, migrate, socketio, babel
from flask_ambrosial.config import Config

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        """Set up a test client before each test."""
        self.app = create_app(Config)
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Clean up after each test."""
        self.app_context.pop()

    def test_app_creation(self):
        """Test if the Flask app is created correctly."""
        self.assertIsInstance(self.app, Flask)

    def test_config_loading(self):
        """Test if the configurations are loaded properly."""
        self.assertEqual(self.app.config['SQLALCHEMY_DATABASE_URI'], Config.SQLALCHEMY_DATABASE_URI)

    def test_extensions_initialization(self):
        """Test if each extension is initialized correctly."""
        self.assertIsNotNone(db)
        self.assertIsNotNone(bcrypt)
        self.assertIsNotNone(login_manager)
        self.assertIsNotNone(mail)
        self.assertIsNotNone(migrate)
        self.assertIsNotNone(socketio)
        self.assertIsNotNone(babel)

    def test_blueprints_registration(self):
        """Test if each blueprint is registered correctly."""
        self.assertIn('users', self.app.blueprints)
        self.assertIn('posts', self.app.blueprints)
        self.assertIn('main', self.app.blueprints)
        self.assertIn('errors', self.app.blueprints)
        self.assertIn('api_bp', self.app.blueprints)
        self.assertIn('chat', self.app.blueprints)

    def test_setlang_route(self):
        """Test if the /setlang route works as expected."""
        with self.client as c:
            response = c.get('/setlang?lang=es', follow_redirects=True)
            self.assertEqual(session['lang'], 'es')
            self.assertEqual(response.status_code, 200)

    def test_context_processor(self):
        """Test if the context processor injects the correct functions."""
        with self.app.test_request_context('/'):
            context = self.app.process_response(self.app.response_class())
            self.assertIn('_', context.context)
            self.assertIn('get_locale', context.context)

if __name__ == '__main__':
    unittest.main()
