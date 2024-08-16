#!/usr/bin/env python3

import unittest
from flask_testing import TestCase
from flask_ambrosial import create_app
from flask_ambrosial.users.forms import (RegistrationForm, LoginForm, 
                                         UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from flask_ambrosial.models import User
from flask_sqlalchemy import SQLAlchemy
from flask_ambrosial.config import TestingConfig

# Initialize SQLAlchemy
db = SQLAlchemy()

class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app('TestingConfig')
        db.init_app(app)
        return app

    def setUp(self):
        # Create the database tables
        with self.app.app_context():
            db.create_all()
            # Create a sample user
            user = User(username='existing_user', email='existing@example.com', password='password')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        # Drop the database tables
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

class TestRegistrationForm(BaseTestCase):
    def test_valid_data(self):
        form = RegistrationForm(username='newuser', email='new@example.com', password='password', confirm_password='password')
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        form = RegistrationForm(username='existing_user', email='existing@example.com', password='password', confirm_password='password')
        self.assertFalse(form.validate())

class TestLoginForm(BaseTestCase):
    def test_valid_data(self):
        form = LoginForm(email='existing@example.com', password='password')
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        form = LoginForm(email='nonexistent@example.com', password='wrongpassword')
        self.assertFalse(form.validate())

class TestUpdateAccountForm(BaseTestCase):
    def test_valid_data(self):
        form = UpdateAccountForm(username='updateduser', email='updated@example.com')
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        form = UpdateAccountForm(username='existing_user', email='existing@example.com')
        self.assertFalse(form.validate())

class TestRequestResetForm(BaseTestCase):
    def test_valid_data(self):
        form = RequestResetForm(email='existing@example.com')
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        form = RequestResetForm(email='nonexistent@example.com')
        self.assertFalse(form.validate())

class TestResetPasswordForm(BaseTestCase):
    def test_valid_data(self):
        form = ResetPasswordForm(password='newpassword', confirm_password='newpassword')
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        form = ResetPasswordForm(password='newpassword', confirm_password='mismatch')
        self.assertFalse(form.validate())

if __name__ == '__main__':
    unittest.main()
