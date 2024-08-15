import unittest
from flask import current_app
from flask_ambrosial import create_app, db, socketio
from flask_ambrosial.models import User, ChatMessage
from flask_ambrosial.config import TestingConfig
from flask_socketio import SocketIOTestClient
from flask_login import login_user
from flask_bcrypt import Bcrypt
import time

bcrypt = Bcrypt()

class ChatRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()  # Drop all tables to ensure a clean state
        db.create_all()
        hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        self.user = User(username='testuser', email='test@example.com', password=hashed_password)
        db.session.add(self.user)
        db.session.commit()
        self.client = self.app.test_client()
        socketio.init_app(self.app)  # Ensure Socket.IO is initialized
        self.socketio_client = SocketIOTestClient(self.app, socketio)
        self.login()
        assert self.socketio_client.is_connected()  # Ensure client is connected

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.socketio_client.disconnect()

    def login(self):
        self.client.post('/login', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)

    def wait_for_event(self, client, event_name, timeout=5):
        start_time = time.time()
        while time.time() - start_time < timeout:
            received = client.get_received()
            for event in received:
                print(f"Received event: {event}")  # Log all received events
                if event['name'] == event_name:
                    return event
            time.sleep(0.1)
        return None

    def test_get_messages(self):
        self.login()
        response = self.client.get('/api/messages')
        self.assertEqual(response.status_code, 302)

    def test_post_message(self):
        self.login()
        response = self.client.post('/api/messages', json=dict(
            msg='Hello, World!'
        ))
        self.assertEqual(response.status_code, 302)

    def test_handle_join(self):
        self.login()
        self.socketio_client.emit('join', {'room': 'default', 'username': 'testuser'})
        event = self.wait_for_event(self.socketio_client, 'message')
        print("Received in test_handle_join:", event)  # Debugging statement
        self.assertIsNotNone(event)
        self.assertEqual(event['name'], 'message')
        self.assertIn('testuser has entered the room.', event['args']['msg'])

    def test_handle_leave(self):
        self.login()
        self.socketio_client.emit('join', {'room': 'default', 'username': 'testuser'})
        time.sleep(1)  # Ensure the join operation is completed
        self.socketio_client.emit('leave', {'room': 'default', 'username': 'testuser'})
        event = self.wait_for_event(self.socketio_client, 'message')
        print("Received in test_handle_leave:", event)  # Debugging statement
        self.assertIsNotNone(event)
        self.assertEqual(event['name'], 'message')
        self.assertIn('testuser has left the room.', event['args']['msg'])

    def test_handle_message(self):
        self.login()
        self.socketio_client.emit('join', {'room': 'default', 'username': 'testuser'})
        time.sleep(1)  # Ensure the join operation is completed
        self.socketio_client.emit('message', {'room': 'default', 'msg': 'Hello, room!', 'username': 'testuser'})
        event = self.wait_for_event(self.socketio_client, 'message')
        print("Received in test_handle_message:", event)  # Debugging statement
        self.assertIsNotNone(event)
        self.assertEqual(event['name'], 'message')
        self.assertIn('testuser has entered the room.', event['args']['msg'])

if __name__ == '__main__':
    unittest.main()
