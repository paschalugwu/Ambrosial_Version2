#!/usr/bin/env python3

"""
Unit tests for Flask forms in the Flask Ambrosial application.
"""

import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_ambrosial.users.forms import (
    RegistrationForm, LoginForm, UpdateAccountForm, 
    RequestResetForm, ResetPasswordForm
)
from flask_ambrosial.posts.forms import CommentForm, ReplyForm
from unittest.mock import patch, MagicMock
from flask_ambrosial.config import TestingConfig
from flask_ambrosial import create_app, db
from flask_ambrosial.models import User

class TestRegistrationForm(unittest.TestCase):
    """Test cases for the RegistrationForm."""

    def setUp(self):
        """Set up the test environment."""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.form = RegistrationForm()

    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_fields_exist(self):
        """Test if all fields exist in the form."""
        self.assertTrue(hasattr(self.form, 'username'))
        self.assertTrue(hasattr(self.form, 'email'))
        self.assertTrue(hasattr(self.form, 'password'))
        self.assertTrue(hasattr(self.form, 'confirm_password'))
        self.assertTrue(hasattr(self.form, 'submit'))

    def test_valid_data(self):
        """Test form validation with valid data."""
        form = RegistrationForm(
            username="TestUser", email="test@example.com", 
            password="password", confirm_password="password"
        )
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        """Test form validation with invalid data."""
        form = RegistrationForm(
            username="", email="invalid", password="pass", 
            confirm_password="different"
        )
        self.assertFalse(form.validate())

class TestLoginForm(unittest.TestCase):
    """Test cases for the LoginForm."""

    def setUp(self):
        """Set up the test environment."""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.form = LoginForm()

    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_fields_exist(self):
        """Test if all fields exist in the form."""
        self.assertTrue(hasattr(self.form, 'email'))
        self.assertTrue(hasattr(self.form, 'password'))
        self.assertTrue(hasattr(self.form, 'remember'))
        self.assertTrue(hasattr(self.form, 'submit'))

    def test_valid_data(self):
        """Test form validation with valid data."""
        form = LoginForm(email="test@example.com", password="password")
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        """Test form validation with invalid data."""
        form = LoginForm(email="invalid", password="")
        self.assertFalse(form.validate())

class TestUpdateAccountForm(unittest.TestCase):
    """Test cases for the UpdateAccountForm."""

    def setUp(self):
        """Set up the test environment."""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.form = UpdateAccountForm()

        # Mock current_user
        self.patcher = patch(
            'flask_ambrosial.users.forms.current_user', 
            MagicMock(username="TestUser")
        )
        self.mock_current_user = self.patcher.start()

    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.patcher.stop()

    def test_fields_exist(self):
        """Test if all fields exist in the form."""
        self.assertTrue(hasattr(self.form, 'username'))
        self.assertTrue(hasattr(self.form, 'email'))
        self.assertTrue(hasattr(self.form, 'picture'))
        self.assertTrue(hasattr(self.form, 'submit'))

    def test_valid_data(self):
        """Test form validation with valid data."""
        form = UpdateAccountForm(
            username="TestUser", email="test@example.com"
        )
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        """Test form validation with invalid data."""
        form = UpdateAccountForm(username="", email="invalid")
        self.assertFalse(form.validate())

class TestRequestResetForm(unittest.TestCase):
    """Test cases for the RequestResetForm."""

    def setUp(self):
        """Set up the test environment."""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a user with the email test@example.com
        user = User(
            username='testuser', email='test@example.com', 
            password='password'
        )
        db.session.add(user)
        db.session.commit()

        self.form = RequestResetForm()

    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_fields_exist(self):
        """Test if all fields exist in the form."""
        self.assertTrue(hasattr(self.form, 'email'))
        self.assertTrue(hasattr(self.form, 'submit'))

    def test_valid_data(self):
        """Test form validation with valid data."""
        form = RequestResetForm(email="test@example.com")
        if not form.validate():
            print(form.errors)
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        """Test form validation with invalid data."""
        form = RequestResetForm(email="invalid")
        self.assertFalse(form.validate())

class TestResetPasswordForm(unittest.TestCase):
    """Test cases for the ResetPasswordForm."""

    def setUp(self):
        """Set up the test environment."""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.form = ResetPasswordForm()

    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_fields_exist(self):
        """Test if all fields exist in the form."""
        self.assertTrue(hasattr(self.form, 'password'))
        self.assertTrue(hasattr(self.form, 'confirm_password'))
        self.assertTrue(hasattr(self.form, 'submit'))

    def test_valid_data(self):
        """Test form validation with valid data."""
        form = ResetPasswordForm(
            password="password", confirm_password="password"
        )
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        """Test form validation with invalid data."""
        form = ResetPasswordForm(
            password="password", confirm_password="different"
        )
        self.assertFalse(form.validate())

class TestCommentForm(unittest.TestCase):
    """Test cases for the CommentForm."""

    def setUp(self):
        """Set up the test environment."""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.form = CommentForm()

    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_fields_exist(self):
        """Test if all fields exist in the form."""
        self.assertTrue(hasattr(self.form, 'content'))
        self.assertTrue(hasattr(self.form, 'submit'))

    def test_valid_data(self):
        """Test form validation with valid data."""
        form = CommentForm(content="This is a comment")
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        """Test form validation with invalid data."""
        form = CommentForm(content="")
        self.assertFalse(form.validate())

class TestReplyForm(unittest.TestCase):
    """Test cases for the ReplyForm."""

    def setUp(self):
        """Set up the test environment."""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.form = ReplyForm()

    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_fields_exist(self):
        """Test if all fields exist in the form."""
        self.assertTrue(hasattr(self.form, 'content'))
        self.assertTrue(hasattr(self.form, 'submit'))

    def test_valid_data(self):
        """Test form validation with valid data."""
        form = ReplyForm(content="This is a reply")
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        """Test form validation with invalid data."""
        form = ReplyForm(content="")
        self.assertFalse(form.validate())

if __name__ == '__main__':
    unittest.main()
