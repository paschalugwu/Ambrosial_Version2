#!/usr/bin/env python3
"""Database models for User and Post entities."""

from time import time
from flask import current_app
from flask_ambrosial import db, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    """Load a user by ID for Flask-Login.

    Args:
        user_id (int): The ID of the user to load.

    Returns:
        User: The user corresponding to the given ID.
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User model for storing user information."""

    def __init__(self, username, email, image_file, password):
        """Initialize a User instance with username, email, image_file, and password."""
        self.username = username
        self.email = email
        self.image_file = image_file
        self.password = password

    # User attributes: id, username, email, image_file, password
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20),
                           nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    """ Relationship with Post model, one-to-many
    relationship (one user can have multiple posts) """
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        """Generate a token for resetting the user's password.

        Args:
            expires_sec (int, optional): Expiry time for the token in seconds. Defaults to 1800.

        Returns:
            str: The generated reset token.
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        expires_at = time() + expires_sec
        return s.dumps({'user_id': self.id, 'expires_at': expires_at}, salt='reset-password')

    @staticmethod
    def verify_reset_token(token):
        """Verify the reset token and return the user if valid.

        Args:
            token (str): The reset token to verify.

        Returns:
            User: The user associated with the token if valid, else None.
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, salt='reset-password')
            if 'expires_at' in data and data['expires_at'] >= time():
                user_id = data['user_id']
                return User.query.get(user_id)
        except:
            pass
        return None

    def __repr__(self):
        """Representation of the User object."""
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    """Post model for storing user posts."""

    def __init__(self, title, content, user_id, image_filename):
        """Initialize a Post instance with title, content, user_id, and image_filename."""
        self.title = title
        self.content = content
        self.user_id = user_id
        self.image_filename = image_filename

    # Post attributes: id, title, date_posted, content, user_id
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.now(timezone.utc))
    content = db.Column(db.Text, nullable=False)
    # Foreign key relationship with User model, each post belongs to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Filename of the uploaded image for the post
    image_filename = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Representation of the Post object."""
        return f"Post('{self.title}', '{self.date_posted}')"
