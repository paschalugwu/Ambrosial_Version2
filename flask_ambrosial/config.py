#!/usr/bin/env python3

import os

class Config:
    """Configuration class for the Flask application."""
    
    # Secret key for protecting against CSRF attacks
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # URI for connecting to the database
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    
    # SMTP server configuration for sending emails
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    # Internationalization (i18n) settings
    LANGUAGES = ['en', 'zh', 'es', 'hi', 'ar', 'fr', 'bn', 'pt', 'ru', 'ja']  # List of supported languages
    BABEL_DEFAULT_LOCALE = 'en'  # Default locale
    BABEL_DEFAULT_TIMEZONE = 'UTC'  # Default timezone
