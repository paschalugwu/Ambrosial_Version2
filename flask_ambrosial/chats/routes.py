#!/usr/bin/env python3

from flask import Blueprint, render_template, session, request, jsonify
from flask_login import login_required, current_user
from flask_socketio import emit, join_room, leave_room, send
from flask_ambrosial import socketio, db
from flask_ambrosial.models import ChatMessage
import logging

chat = Blueprint('chat', __name__)

@chat.route("/chat")
@login_required
def chat_room():
    return render_template('chat.html', username=current_user.username)

@chat.route("/api/messages", methods=['GET'])
@login_required
def get_messages():
    messages = ChatMessage.query.all()
    return jsonify([{'id': msg.id, 'username': msg.user.username, 'content': msg.content} for msg in messages])

@chat.route("/api/messages", methods=['POST'])
@login_required
def post_message():
    data = request.json
    chat_message = ChatMessage(content=data['msg'], user_id=current_user.id)
    db.session.add(chat_message)
    db.session.commit()
    return jsonify({'id': chat_message.id, 'username': current_user.username, 'content': data['msg']}), 201

@socketio.on('join')
def handle_join(data):
    room = data['room']
    username = data['username']
    join_room(room)
    emit('message', {'msg': f'{username} has entered the room.'}, room=room)
    print(f"Emitted join message for {username} to room {room}")  # Debugging statement

@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    username = data['username']
    print(f"User {username} is leaving room {room}")  # Debugging statement
    leave_room(room)
    emit('message', {'msg': f'{username} has left the room.'}, room=room)
    print(f"Emitted leave message for {username} from room {room}")  # Debugging statement

@socketio.on('message')
def handle_message(data):
    room = data['room']
    msg = data['msg']
    username = data['username']
    print(f"User {username} sent message to room {room}: {msg}")  # Debugging statement
    emit('message', {'msg': f'{username}: {msg}'}, room=room)
    print(f"Emitted message for {username} to room {room}: {msg}")  # Debugging statement
