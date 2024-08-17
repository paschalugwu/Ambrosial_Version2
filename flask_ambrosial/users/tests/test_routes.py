#!/usr/bin/env python3
"""
Unit tests for user routes in the flask_ambrosial module.
"""

import unittest
from flask_ambrosial import create_app, db
from flask_ambrosial.models import User
from flask_bcrypt import Bcrypt
from flask_ambrosial.config import TestingConfig
from flask import url_for, get_flashed_messages


class UsersRoutesTestCase(unittest.TestCase):
    """
    Test cases for user-related routes.
    """
    def setUp(self):
        """
        Set up the test environment before each test.
        """
        self.app = create_app(TestingConfig)
        self.app.config['SERVER_NAME'] = 'localhost'
        self.client = self.app.test_client()
        self.bcrypt = Bcrypt(self.app)
        with self.app.app_context():
            db.create_all()
            # Create a sample user
            user = User(username='testuser', email='test@example.com',
                        password=self.bcrypt.generate_password_hash(
                            'password').decode('utf-8'))
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        """
        Tear down the test environment after each test.
        """
        with self.app.app_context():
            db.drop_all()

    def test_register_get(self):
        """
        Test GET request to the register route.
        """
        with self.app.app_context():
            response = self.client.get(url_for('users.register'))
            self.assertEqual(response.status_code, 200)

    def test_register_post_valid(self):
        """
        Test POST request to the register route with valid data.
        """
        with self.app.app_context():
            response = self.client.post(url_for('users.register'), data={
                'username': 'newuser',
                'email': 'new@example.com',
                'password': 'password',
                'confirm_password': 'password'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Your account has been created!', response.data)

    def test_register_post_invalid(self):
        """
        Test POST request to the register route with invalid data.
        """
        with self.app.app_context():
            response = self.client.post(url_for('users.register'), data={
                'username': '',
                'email': 'new@example.com',
                'password': 'password',
                'confirm_password': 'password'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'This field is required.', response.data)

    def test_login_get(self):
        """
        Test GET request to the login route.
        """
        with self.app.app_context():
            response = self.client.get(url_for('users.login'))
            self.assertEqual(response.status_code, 200)

    def test_login_post_invalid(self):
        """
        Test POST request to the login route with invalid data.
        """
        with self.app.app_context():
            response = self.client.post(url_for('users.login'), data={
                'email': 'test@example.com',
                'password': 'wrongpassword'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Login Unsuccessful', response.data)

    def test_logout(self):
        """
        Test the logout route.
        """
        with self.app.app_context():
            # Log in the user first
            self.client.post(url_for('users.login'), data={
                'email': 'test@example.com',
                'password': 'password'
            })
            # Log out the user and follow redirects to capture the flash msg
            response = self.client.get(url_for('users.logout'), 
                                       follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You have been logged out', response.data)

    def test_account_get(self):
        """
        Test GET request to the account route.
        """
        with self.app.app_context():
            self.client.post(url_for('users.login'), data={
                'email': 'test@example.com',
                'password': 'password'
            })
            response = self.client.get(url_for('users.account'))
            self.assertEqual(response.status_code, 200)

    def test_account_post_valid(self):
        """
        Test POST request to the account route with valid data.
        """
        with self.app.app_context():
            self.client.post(url_for('users.login'), data={
                'email': 'test@example.com',
                'password': 'password'
            })
            response = self.client.post(url_for('users.account'), data={
                'username': 'updateduser',
                'email': 'updated@example.com'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Your account has been updated!', response.data)

    def test_user_posts(self):
        """
        Test GET request to the user posts route.
        """
        with self.app.app_context():
            response = self.client.get(url_for('users.user_posts', 
                                               username='testuser'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'testuser', response.data)

    def test_reset_request_get(self):
        """
        Test GET request to the reset request route.
        """
        with self.app.app_context():
            response = self.client.get(url_for('users.reset_request'))
            self.assertEqual(response.status_code, 200)

    def test_reset_request_post_valid(self):
        """
        Test POST request to the reset request route with valid data.
        """
        with self.app.app_context():
            response = self.client.post(url_for('users.reset_request'), data={
                'email': 'test@example.com'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'An email has been sent', response.data)

    def test_reset_token_get(self):
        """
        Test GET request to the reset token route.
        """
        with self.app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            token = user.get_reset_token()
            response = self.client.get(url_for('users.reset_token', 
                                               token=token))
            self.assertEqual(response.status_code, 200)

    def test_reset_token_post_valid(self):
        """
        Test POST request to the reset token route with valid data.
        """
        with self.app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            token = user.get_reset_token()
            response = self.client.post(url_for('users.reset_token', 
                                                token=token), data={
                'password': 'newpassword',
                'confirm_password': 'newpassword'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Your password has been updated!', response.data)


if __name__ == '__main__':
    unittest.main()
