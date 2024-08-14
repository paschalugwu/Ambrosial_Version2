#!/usr/bin/env python3
"""Initialization of the Flask application and its extensions."""

from flask import Flask, redirect, request, session, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_babel import Babel, lazy_gettext as _l, gettext  # Correct import

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

# Initialize Flask-Migrate
migrate = Migrate()

# Initialize SocketIO
socketio = SocketIO(cors_allowed_origins=["http://localhost:5000", "https://localhost:5000"])

# Initialize Babel for i18n
babel = Babel()

def get_locale():
    """Determine the best match language from the request."""
    if 'lang' in request.args:
        lang = request.args.get('lang')
        if lang in current_app.config['LANGUAGES']:
            session['lang'] = lang
            return lang
    return session.get('lang', request.accept_languages.best_match(current_app.config['LANGUAGES']))

def create_app(config_class=Config):
    """Create and configure the Flask application.

    Args:
        config_class: The configuration class for the application.
                      Defaults to Config.

    Returns:
        Flask: The configured Flask application instance.
    """
    # Create the Flask application instance
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    # Load configuration from the provided Config class
    app.config.from_object(config_class)

    # Initialize extensions with the Flask application instance
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    # Import blueprints and register them with the app
    from flask_ambrosial.users.routes import users
    from flask_ambrosial.posts.routes import posts
    from flask_ambrosial.main.routes import main
    from flask_ambrosial.errors.handlers import errors
    from flask_ambrosial.apis.api_routes import api_bp
    from flask_ambrosial.chats.routes import chat
    app.register_blueprint(users)  # Register users blueprint
    app.register_blueprint(posts)  # Register posts blueprint
    app.register_blueprint(main)   # Register main blueprint
    app.register_blueprint(errors)  # Register errors blueprint
    app.register_blueprint(api_bp)  # Register API blueprint
    app.register_blueprint(chat)  # Register chat blueprint

    @app.route('/setlang')
    def setlang():
        lang = request.args.get('lang', 'en')
        session['lang'] = lang
        return redirect(request.referrer)

    @app.context_processor
    def inject_babel():
        return dict(_=gettext, get_locale=get_locale)  # Add get_locale here

    return app
