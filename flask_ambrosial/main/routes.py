#!/usr/bin/env python3

from flask import Blueprint, render_template, url_for, request, session, redirect
from flask_ambrosial.models import Post
from flask_babel import refresh
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create a Blueprint for the main routes
main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    """Render the home page.

    Returns:
        str: Rendered template with posts and associated image files.
    """
    # Get the page number from the request arguments, default is 1
    page = request.args.get('page', 1, type=int)
    # Query posts ordered by date posted in descending order, paginated
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    # Generate URLs for associated image files
    image_files = [url_for('static', filename='post_pics/' + post.image_filename) for post in posts.items]
    # Render the home template with posts and image files
    return render_template('home.html', posts=posts, image_files=image_files)


@main.route("/about")
def about():
    """Render the about page.

    Returns:
        str: Rendered template for the about page.
    """
    return render_template('about.html', title='About')


@main.route('/setlang')
def setlang():
    """Set the language for the session and redirect to the previous page.

    Returns:
        werkzeug.wrappers.Response: Redirect response to the previous page or home.
    """
    lang = request.args.get('lang', 'en')
    logging.debug(f"Requested language: {lang}")
    if lang in ['en', 'fr']:
        session['lang'] = lang
        logging.debug(f"Session language set to: {session['lang']}")
        refresh()  # Refresh Babel translations
    else:
        logging.debug(f"Invalid language requested: {lang}")
    logging.debug(f"Redirecting to: {request.referrer or url_for('main.home')}")
    return redirect(request.referrer or url_for('main.home'))
