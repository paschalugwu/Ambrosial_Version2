#!/usr/bin/env python3

import os

class Config:
    """Configuration class for the Flask application."""
    
    # Secret key for protecting against CSRF attacks
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # URI for connecting to the database
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    
    # SMTP server configuration for sending emails
    MAIL_SERVER = 'smtp.googlemail.com'  # Google Mail SMTP server
    MAIL_PORT = 587  # SMTP port number
    MAIL_USE_TLS = True  # Enable TLS encryption for email
    MAIL_USERNAME = os.environ.get('EMAIL_USER')  # Email username from environment variable
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')  # Email password from environment variable

    # Internationalization (i18n) settings
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'  # Default locale
    BABEL_TRANSLATION_DIRECTORIES = './translations'
    
    # Enable debug mode
    DEBUG = True
