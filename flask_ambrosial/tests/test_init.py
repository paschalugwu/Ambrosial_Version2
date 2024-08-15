#!/usr/bin/env python3

import unittest
from flask import Flask, session, request, render_template, template_rendered
from flask_ambrosial import create_app, db, bcrypt, login_manager, mail, migrate, socketio, babel
from flask_ambrosial.config import Config
from contextlib import contextmanager

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
        self.assertIn('api', self.app.blueprints)
        self.assertIn('chat', self.app.blueprints)

    def test_setlang_route(self):
        """Test if the /setlang route works as expected."""
        LANGUAGES = ['en', 'fr', 'ha', 'ig', 'yo']
        with self.client as c:
            for lang in LANGUAGES:
                response = c.get(f'/setlang?lang={lang}', follow_redirects=True)
                with c.session_transaction() as sess:
                    self.assertEqual(sess['lang'], lang)
                self.assertEqual(response.status_code, 200)

    @contextmanager
    def captured_templates(self, app):
        recorded = []

        def record(sender, template, context, **extra):
            recorded.append((template, context))

        template_rendered.connect(record, app)
        try:
            yield recorded
        finally:
            template_rendered.disconnect(record, app)

    def test_context_processor(self):
        """Test if the context processor injects the correct functions."""
        with self.captured_templates(self.app) as templates:
            with self.app.test_request_context('/'):
                render_template('chat.html')
                template, context = templates[0]

                # Check if the context processor injected the correct functions
                self.assertIn('_', context)
                self.assertIn('current_user', context)

if __name__ == '__main__':
    unittest.main()
