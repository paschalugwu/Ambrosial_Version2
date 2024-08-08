#!/usr/bin/env python3
"""Entry point for running the Flask application."""

from flask_ambrosial import create_app

app = create_app()

if __name__ == '__main__':
    # Run the Flask application
    # - debug=True enables debug mode for development
    # - This means the server will reload on code changes and
    #   provide more detailed error messages
    app.run(debug=True)
