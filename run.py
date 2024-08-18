#!/usr/bin/env python3
"""Entry point for running the Flask application."""

from flask_ambrosial import create_app, socketio

app = create_app(use_socketio=True)

if __name__ == '__main__':
    # Run the Flask application with SocketIO in production mode
    if socketio:
        socketio.run(app, host="0.0.0.0", port=5000)
    else:
        app.run(host="0.0.0.0", port=5000)
