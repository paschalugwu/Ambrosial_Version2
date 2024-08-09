#!/usr/bin/env python3

from flask import Blueprint, render_template, url_for, request, redirect, session, current_app
from flask_ambrosial.models import Post
from flask_babel import refresh
from flask_ambrosial import get_locale

# Create a Blueprint for the main routes
main = Blueprint('main', __name__)


@main.context_processor
def inject_locale():
    """Inject the get_locale function into the template context.

    Returns:
        dict: A dictionary containing the get_locale function.
    """
    return {'get_locale': get_locale}

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
    lang = request.args.get('lang', 'en')
    session['lang'] = lang
    return redirect(request.referrer or url_for('main.home'))

@main.context_processor
def inject_locale():
    return {'get_locale': get_locale}
