#!/usr/bin/env python3

from flask import Flask, redirect, request, session, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_babel import Babel, lazy_gettext as _l, gettext

from flask_ambrosial.config import Config, TestingConfig

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins=["http://localhost:5000", "https://localhost:5000", "http://127.0.0.1:5000"], async_mode='eventlet')
babel = Babel()

def get_locale():
    if 'lang' in request.args:
        lang = request.args.get('lang')
        if lang in current_app.config['LANGUAGES']:
            session['lang'] = lang
            return lang
    return session.get('lang', request.accept_languages.best_match(current_app.config['LANGUAGES']))

def create_app(config_class=Config, use_socketio=False):
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app, locale_selector=get_locale)

    if use_socketio:
        socketio.init_app(app, async_mode='eventlet')

    from flask_ambrosial.users.routes import users
    from flask_ambrosial.posts.routes import posts
    from flask_ambrosial.main.routes import main
    from flask_ambrosial.errors.handlers import errors
    from flask_ambrosial.apis.api_routes import api_bp
    from flask_ambrosial.chats.routes import chat

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(api_bp)
    app.register_blueprint(chat)

    @app.route('/setlang')
    def setlang():
        lang = request.args.get('lang', 'en')
        session['lang'] = lang
        return redirect('/')

    @app.context_processor
    def inject_babel():
        return dict(_=gettext, get_locale=get_locale)

    return app
