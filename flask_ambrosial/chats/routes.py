#!/usr/bin/env python3

"""
This module defines the chat routes and socket events for the Flask 
application.
"""

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from flask_socketio import emit, join_room
from flask_ambrosial import socketio, db
from flask_ambrosial.models import ChatMessage
import logging

# Create a Blueprint for chat routes
chat = Blueprint('chat', __name__)

@chat.route("/chat")
@login_required
def chat_room():
    """
    Render the chat room template.

    Returns:
        str: Rendered HTML template for the chat room.
    """
    return render_template('chat.html', username=current_user.username)

@chat.route("/api/messages", methods=['GET'])
@login_required
def get_messages():
    """
    Fetch all chat messages from the database.

    Returns:
        jsonify: JSON response containing all chat messages.
    """
    messages = ChatMessage.query.all()
    return jsonify([
        {
            'id': msg.id,
            'username': msg.user.username,
            'content': msg.content
        } for msg in messages
    ])

@chat.route("/api/messages", methods=['POST'])
@login_required
def post_message():
    """
    Post a new chat message to the database.

    Returns:
        jsonify: JSON response containing the posted message.
    """
    data = request.json
    chat_message = ChatMessage(
        content=data['msg'], user_id=current_user.id
    )
    db.session.add(chat_message)
    db.session.commit()
    return jsonify({
        'id': chat_message.id,
        'username': current_user.username,
        'content': data['msg']
    }), 201

@socketio.on('join')
def handle_join(data):
    """
    Handle a user joining a chat room.

    Args:
        data (dict): Data containing room and username information.
    """
    room = data['room']
    username = data['username']
    join_room(room)
    emit('message', {'msg': f'{username} has entered the room.'}, room=room)
    print(f"Emitted join message for {username} to room {room}")  # Debugging

@socketio.on('message')
def handle_message(data):
    """
    Handle a new chat message.

    Args:
        data (dict): Data containing room, message, and username information.
    """
    room = data['room']
    msg = data['msg']
    username = data['username']
    print(f"User {username} sent message to room {room}: {msg}")  # Debugging
    emit('message', {'msg': f'{username}: {msg}'}, room=room)
    print(f"Emitted message for {username} to room {room}: {msg}")  # Debugging
