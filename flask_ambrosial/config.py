#!/usr/bin/env python3

import os

class Config:
    """Configuration class for the Flask application."""
    
    # Secret key for protecting against CSRF attacks
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # URI for connecting to the database
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    
    # SMTP server configuration for sending emails
<<<<<<< HEAD
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    # Internationalization (i18n) settings
    LANGUAGES = ['en', 'zh', 'es', 'hi', 'ar', 'fr', 'bn', 'pt', 'ru', 'ja']  # List of supported languages
    BABEL_DEFAULT_LOCALE = 'en'  # Default locale
    BABEL_DEFAULT_TIMEZONE = 'UTC'  # Default timezone
=======
    MAIL_SERVER = 'smtp.googlemail.com'  # Google Mail SMTP server
    MAIL_PORT = 587  # SMTP port number
    MAIL_USE_TLS = True  # Enable TLS encryption for email
    MAIL_USERNAME = os.environ.get('EMAIL_USER')  # Email username from environment variable
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')  # Email password from environment variable
    LANGUAGES = ['en', 'zh', 'es', 'hi', 'ar', 'fr', 'bn', 'pt', 'ru', 'ja']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
>>>>>>> f50ab4d (Update files)
