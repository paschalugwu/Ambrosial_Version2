#!/usr/bin/env python3
"""Initialization of the Flask application and its extensions."""

<<<<<<< HEAD
from flask import Flask, request, current_app
=======
from flask import Flask, request, session
>>>>>>> f50ab4d (Update files)
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_babel import Babel
from flask_ambrosial.config import Config

# Initialize SQLAlchemy database object
db = SQLAlchemy()

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt()

# Initialize Flask-Login for user authentication
login_manager = LoginManager()
login_manager.login_view = 'users.login'  # Set the login page route
login_manager.login_message_category = 'info'  # Set login message category

# Initialize Flask-Mail for sending emails
mail = Mail()

<<<<<<< HEAD
# Initialize Flask-Babel for internationalization
=======
# Initialize Flask-Babel for internationalization (i18n)
>>>>>>> f50ab4d (Update files)
babel = Babel()

def create_app(config_class=Config):
    """Create and configure the Flask application.

    Args:
        config_class: The configuration class for the application.
                      Defaults to Config.

    Returns:
        Flask: The configured Flask application instance.
    """
    # Create the Flask application instance
    app = Flask(__name__)
    # Load configuration from the provided Config class
    app.config.from_object(config_class)

    # Initialize extensions with the Flask application instance
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
<<<<<<< HEAD
    babel.init_app(app, locale_selector=get_locale)
=======
    babel.init_app(app, locale_selector=get_locale)  # Updated initialization
>>>>>>> f50ab4d (Update files)

    # Import blueprints and register them with the app
    from flask_ambrosial.users.routes import users
    from flask_ambrosial.posts.routes import posts
    from flask_ambrosial.main.routes import main
    from flask_ambrosial.errors.handlers import errors
    from flask_ambrosial.apis.api_routes import api_bp
    app.register_blueprint(users)  # Register users blueprint
    app.register_blueprint(posts)  # Register posts blueprint
    app.register_blueprint(main)   # Register main blueprint
    app.register_blueprint(errors)  # Register errors blueprint
    app.register_blueprint(api_bp)  # Register API blueprint

    return app

def get_locale():
<<<<<<< HEAD
    """Determine the best match for the user's preferred language."""
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])
=======
    """Determine the best match with the supported languages.

    Returns:
        str: The language code of the selected language.
    """
    return session.get('language', request.accept_languages.best_match(current_app.config['LANGUAGES']))
>>>>>>> f50ab4d (Update files)
