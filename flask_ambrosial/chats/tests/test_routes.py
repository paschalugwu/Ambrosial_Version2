#!/usr/bin/env python3

import unittest
from flask import current_app
from flask_ambrosial import create_app, db, socketio
from flask_ambrosial.models import User, ChatMessage
from flask_socketio import SocketIOTestClient
from flask_login import login_user

class ChatRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.socketio_client = SocketIOTestClient(current_app, socketio)
        
        # Create a test user
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('password')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self):
        with self.client:
            self.client.post('/login', data=dict(
                email='test@example.com',
                password='password'
            ))

    def test_chat_room(self):
        self.login()
        response = self.client.get('/chat')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'chat.html', response.data)

    def test_get_messages(self):
        self.login()
        response = self.client.get('/api/messages')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_post_message(self):
        self.login()
        response = self.client.post('/api/messages', json={'msg': 'Hello, world!'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['content'], 'Hello, world!')

    def test_update_message(self):
        self.login()
        chat_message = ChatMessage(content='Old message', user_id=self.user.id)
        db.session.add(chat_message)
        db.session.commit()
        response = self.client.put(f'/api/messages/{chat_message.id}', json={'msg': 'Updated message'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['content'], 'Updated message')

    def test_delete_message(self):
        self.login()
        chat_message = ChatMessage(content='Message to delete', user_id=self.user.id)
        db.session.add(chat_message)
        db.session.commit()
        response = self.client.delete(f'/api/messages/{chat_message.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 'Message deleted')

    def test_handle_join(self):
        self.login()
        self.socketio_client.emit('join', {'room': 'testroom', 'username': 'testuser'})
        received = self.socketio_client.get_received()
        self.assertEqual(received[0]['name'], 'message')
        self.assertIn('testuser has entered the room.', received[0]['args'][0]['msg'])

    def test_handle_leave(self):
        self.login()
        self.socketio_client.emit('leave', {'room': 'testroom', 'username': 'testuser'})
        received = self.socketio_client.get_received()
        self.assertEqual(received[0]['name'], 'message')
        self.assertIn('testuser has left the room.', received[0]['args'][0]['msg'])

    def test_handle_message(self):
        self.login()
        self.socketio_client.emit('message', {'room': 'testroom', 'msg': 'Hello, room!', 'username': 'testuser'})
        received = self.socketio_client.get_received()
        self.assertEqual(received[0]['name'], 'message')
        self.assertIn('testuser: Hello, room!', received[0]['args'][0]['msg'])

if __name__ == '__main__':
    unittest.main()
