#!/usr/bin/env python3

import unittest
from unittest.mock import patch
from flask_ambrosial.config import Config

class TestConfig(unittest.TestCase):

    @patch.dict(os.environ, {'SECRET_KEY': 'supersecretkey', 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db', 'EMAIL_USER': 'test@example.com', 'EMAIL_PASS': 'password'})
    def test_secret_key(self):
        self.assertEqual(Config.SECRET_KEY, 'supersecretkey')

    @patch.dict(os.environ, {'SECRET_KEY': 'supersecretkey', 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db', 'EMAIL_USER': 'test@example.com', 'EMAIL_PASS': 'password'})
    def test_sqlalchemy_database_uri(self):
        self.assertEqual(Config.SQLALCHEMY_DATABASE_URI, 'sqlite:///test.db')

    @patch.dict(os.environ, {'SECRET_KEY': 'supersecretkey', 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db', 'EMAIL_USER': 'test@example.com', 'EMAIL_PASS': 'password'})
    def test_mail_server(self):
        self.assertEqual(Config.MAIL_SERVER, 'smtp.googlemail.com')
        self.assertEqual(Config.MAIL_PORT, 587)
        self.assertTrue(Config.MAIL_USE_TLS)
        self.assertEqual(Config.MAIL_USERNAME, 'test@example.com')
        self.assertEqual(Config.MAIL_PASSWORD, 'password')

    def test_languages(self):
        self.assertEqual(Config.LANGUAGES, ['en', 'fr', 'ha', 'ig', 'yo'])
        self.assertEqual(Config.BABEL_DEFAULT_LOCALE, 'en')
        self.assertEqual(Config.BABEL_TRANSLATION_DIRECTORIES, './translations')

if __name__ == '__main__':
    unittest.main()
