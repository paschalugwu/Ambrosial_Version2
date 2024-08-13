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

@chat.route("/api/messages/<int:message_id>", methods=['PUT'])
@login_required
def update_message(message_id):
    data = request.json
    chat_message = ChatMessage.query.get_or_404(message_id)
    if chat_message.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    chat_message.content = data['msg']
    db.session.commit()
    return jsonify({'id': chat_message.id, 'username': current_user.username, 'content': data['msg']}), 200

@chat.route("/api/messages/<int:message_id>", methods=['DELETE'])
@login_required
def delete_message(message_id):
    chat_message = ChatMessage.query.get_or_404(message_id)
    if chat_message.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(chat_message)
    db.session.commit()
    return jsonify({'result': 'Message deleted'}), 200

@socketio.on('join')
def handle_join(data):
    room = data['room']
    logging.debug(f"{data['username']} is joining room {room}")
    join_room(room)
    emit('message', {'msg': f"{data['username']} has entered the room."}, room=room)

@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    logging.debug(f"{data['username']} is leaving room {room}")
    leave_room(room)
    emit('message', {'msg': f"{data['username']} has left the room."}, room=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    msg = data['msg']
    username = data['username']
    logging.debug(f"Message from {username} in room {room}: {msg}")
    if current_user.is_authenticated:
        chat_message = ChatMessage(content=msg, user_id=current_user.id)
        db.session.add(chat_message)
        db.session.commit()
        logging.debug(f"Message stored in database: {msg}")
        send({'msg': f"{username}: {msg}"}, room=room)
    else:
        logging.debug("User not authenticated")
        send({'msg': 'User not authenticated'}, room=room)
