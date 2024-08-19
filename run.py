#!/usr/bin/env python3
"""Entry point for running the Flask application."""

from flask_ambrosial import create_app

app = create_app()

# Vercel expects the app to be a module-level variable named `app`
if __name__ == '__main__':
    app.run(debug=True)
