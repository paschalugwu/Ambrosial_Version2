#!/usr/bin/env python3
"""
Unit tests for user forms in the flask_ambrosial module.
"""

import sys
import os
import unittest
from flask_testing import TestCase
from flask_ambrosial import create_app, db
from flask_ambrosial.users.forms import (RegistrationForm, LoginForm, 
                                         UpdateAccountForm, RequestResetForm, 
                                         ResetPasswordForm)
from flask_ambrosial.models import User
from flask_ambrosial.config import TestingConfig
from flask_login import current_user, AnonymousUserMixin
from unittest.mock import patch, MagicMock

# Add the application directory to the system path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../')))

class BaseTestCase(TestCase):
    """
    Base test case for setting up and tearing down the test environment.
    """
    def create_app(self):
        """
        Create the Flask application for testing.
        """
        app = create_app(TestingConfig)
        return app

    def setUp(self):
        """
        Set up the test environment before each test.
        """
        with self.app.app_context():
            db.create_all()
            # Create a sample user
            user = User(username='existing_user', 
                        email='existing@example.com', 
                        password='password')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        """
        Tear down the test environment after each test.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

class TestRegistrationForm(BaseTestCase):
    """
    Test cases for the RegistrationForm.
    """
    def test_valid_data(self):
        """
        Test form validation with valid data.
        """
        form = RegistrationForm(username='newuser', email='new@example.com', 
                                password='password', 
                                confirm_password='password')
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        """
        Test form validation with invalid data.
        """
        form = RegistrationForm(username='existing_user', 
                                email='existing@example.com', 
                                password='password', 
                                confirm_password='password')
        self.assertFalse(form.validate())

class TestLoginForm(BaseTestCase):
    """
    Test cases for the LoginForm.
    """
    def test_valid_data(self):
        """
        Test form validation with valid data.
        """
        form = LoginForm(email='existing@example.com', password='password')
        self.assertTrue(form.validate())

class TestRequestResetForm(BaseTestCase):
    """
    Test cases for the RequestResetForm.
    """
    def test_valid_data(self):
        """
        Test form validation with valid data.
        """
        form = RequestResetForm(email='existing@example.com')
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        """
        Test form validation with invalid data.
        """
        form = RequestResetForm(email='nonexistent@example.com')
        self.assertFalse(form.validate())

class TestResetPasswordForm(BaseTestCase):
    """
    Test cases for the ResetPasswordForm.
    """
    def test_valid_data(self):
        """
        Test form validation with valid data.
        """
        form = ResetPasswordForm(password='newpassword', 
                                 confirm_password='newpassword')
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        """
        Test form validation with invalid data.
        """
        form = ResetPasswordForm(password='newpassword', 
                                 confirm_password='mismatch')
        self.assertFalse(form.validate())

if __name__ == '__main__':
    unittest.main()
