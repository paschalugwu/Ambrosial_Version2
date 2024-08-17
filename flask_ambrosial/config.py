#!/usr/bin/env python3

"""
Configuration module for Flask application settings.
"""

import os

class Config:
    """
    Base configuration class with default settings.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    LANGUAGES = ['en', 'fr', 'ha', 'ig', 'yo']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_TRANSLATION_DIRECTORIES = './translations'

class TestingConfig(Config):
    """
    Configuration class for testing environment.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_USERNAME = 'test@example.com'
    MAIL_PASSWORD = 'password'
    WTF_CSRF_ENABLED = False
