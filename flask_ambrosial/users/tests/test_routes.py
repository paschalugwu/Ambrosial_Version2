#!/usr/bin/env python3

import unittest
from flask_ambrosial import create_app, db
from flask_ambrosial.models import User
from flask_bcrypt import Bcrypt
from flask_ambrosial.config import TestingConfig
from flask import url_for, get_flashed_messages


class UsersRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app.config['SERVER_NAME'] = 'localhost'
        self.client = self.app.test_client()
        self.bcrypt = Bcrypt(self.app)
        with self.app.app_context():
            db.create_all()
            user = User(username='testuser', email='test@example.com',
                        password=self.bcrypt.generate_password_hash('password').decode('utf-8'))
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_register_get(self):
        with self.app.app_context():
            response = self.client.get(url_for('users.register'))
            self.assertEqual(response.status_code, 200)

    def test_register_post_valid(self):
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
        with self.app.app_context():
            response = self.client.get(url_for('users.login'))
            self.assertEqual(response.status_code, 200)

    def test_login_post_invalid(self):
        with self.app.app_context():
            response = self.client.post(url_for('users.login'), data={
                'email': 'test@example.com',
                'password': 'wrongpassword'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Login Unsuccessful', response.data)

    def test_logout(self):
        with self.app.app_context():
            # Log in the user first
            self.client.post(url_for('users.login'), data={
                'email': 'test@example.com',
                'password': 'password'
            })
            
            # Log out the user and follow redirects to capture the flash message
            response = self.client.get(url_for('users.logout'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            
            # Access flash messages from the response data
            self.assertIn(b'You have been logged out', response.data)


    def test_account_get(self):
        with self.app.app_context():
            self.client.post(url_for('users.login'), data={
                'email': 'test@example.com',
                'password': 'password'
            })
            response = self.client.get(url_for('users.account'))
            self.assertEqual(response.status_code, 200)

    def test_account_post_valid(self):
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
        with self.app.app_context():
            response = self.client.get(url_for('users.user_posts', username='testuser'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'testuser', response.data)

    def test_reset_request_get(self):
        with self.app.app_context():
            response = self.client.get(url_for('users.reset_request'))
            self.assertEqual(response.status_code, 200)

    def test_reset_request_post_valid(self):
        with self.app.app_context():
            response = self.client.post(url_for('users.reset_request'), data={
                'email': 'test@example.com'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'An email has been sent', response.data)

    def test_reset_token_get(self):
        with self.app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            token = user.get_reset_token()
            response = self.client.get(url_for('users.reset_token', token=token))
            self.assertEqual(response.status_code, 200)

    def test_reset_token_post_valid(self):
        with self.app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            token = user.get_reset_token()
            response = self.client.post(url_for('users.reset_token', token=token), data={
                'password': 'newpassword',
                'confirm_password': 'newpassword'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Your password has been updated!', response.data)


if __name__ == '__main__':
    unittest.main()
