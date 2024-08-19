#!/usr/bin/env python3
"""Entry point for running the Flask application."""

import eventlet
eventlet.monkey_patch()

from flask_ambrosial import create_app, socketio

app = create_app(use_socketio=True)

if __name__ == '__main__':
    # Run the Flask application with SocketIO
    # - debug=True enables debug mode for development
    # - This means the server will reload on code changes and
    #   provide more detailed error messages
    if socketio:
        socketio.run(app, debug=True)
    else:
        app.run(debug=True)
