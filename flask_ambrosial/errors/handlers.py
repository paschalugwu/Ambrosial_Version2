#!/usr/bin/env python3

"""
Error handlers module for Flask application.
"""

from flask import Blueprint, render_template

# Create a Blueprint for handling errors
errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """
    Render a custom 404 error page.

    Args:
        error: The error object.

    Returns:
        tuple: A tuple containing the rendered template and the HTTP 
        status code.
    """
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    """
    Render a custom 403 error page.

    Args:
        error: The error object.

    Returns:
        tuple: A tuple containing the rendered template and the HTTP 
        status code.
    """
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    """
    Render a custom 500 error page.

    Args:
        error: The error object.

    Returns:
        tuple: A tuple containing the rendered template and the HTTP 
        status code.
    """
    return render_template('errors/500.html'), 500
