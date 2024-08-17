#!/usr/bin/env python3
"""
Unit tests for the models in the flask_ambrosial module.
"""

import unittest
from flask import current_app
from flask_ambrosial import create_app, db
from flask_ambrosial.models import User, Post, Comment, ChatMessage
from flask_ambrosial.config import TestingConfig
from datetime import datetime, timezone

class ModelTestCase(unittest.TestCase):
    """
    Test case for the models in the flask_ambrosial module.
    """

    def setUp(self):
        """
        Set up a test client and application context before each test.
        """
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
        Clean up after each test.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        """
        Test if a user can be created correctly.
        """
        user = User(
            username='testuser', email='test@example.com',
            password='password'
        )
        db.session.add(user)
        db.session.commit()
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')

    def test_get_reset_token(self):
        """
        Test if a reset token can be generated and verified.
        """
        user = User(
            username='testuser', email='test@example.com',
            password='password'
        )
        db.session.add(user)
        db.session.commit()
        token = user.get_reset_token()
        self.assertIsNotNone(token)
        verified_user = User.verify_reset_token(token)
        self.assertEqual(user, verified_user)

    def test_post_creation(self):
        """
        Test if a post can be created correctly.
        """
        user = User(
            username='testuser', email='test@example.com',
            password='password'
        )
        db.session.add(user)
        db.session.commit()
        post = Post(
            title='Test Post', content='This is a test post.',
            author=user, image_filename='test.jpg'
        )
        db.session.add(post)
        db.session.commit()
        self.assertEqual(Post.query.count(), 1)
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author, user)

    def test_comment_creation(self):
        """
        Test if a comment can be created correctly.
        """
        user = User(
            username='testuser', email='test@example.com',
            password='password'
        )
        db.session.add(user)
        db.session.commit()
        post = Post(
            title='Test Post', content='This is a test post.',
            author=user, image_filename='test.jpg'
        )
        db.session.add(post)
        db.session.commit()
        comment = Comment(
            content='This is a test comment.', author=user, post=post
        )
        db.session.add(comment)
        db.session.commit()
        self.assertEqual(Comment.query.count(), 1)
        self.assertEqual(comment.content, 'This is a test comment.')
        self.assertEqual(comment.author, user)
        self.assertEqual(comment.post, post)

    def test_comment_replies(self):
        """
        Test if replies to comments can be created correctly.
        """
        user = User(
            username='testuser', email='test@example.com',
            password='password'
        )
        db.session.add(user)
        db.session.commit()
        post = Post(
            title='Test Post', content='This is a test post.',
            author=user, image_filename='test.jpg'
        )
        db.session.add(post)
        db.session.commit()
        comment = Comment(
            content='This is a test comment.', author=user, post=post
        )
        db.session.add(comment)
        db.session.commit()
        reply = Comment(
            content='This is a test reply.', author=user, post=post,
            parent=comment
        )
        db.session.add(reply)
        db.session.commit()
        self.assertEqual(Comment.query.count(), 2)
        self.assertEqual(reply.parent, comment)
        self.assertIn(reply, comment.replies)

    def test_chat_message_creation(self):
        """
        Test if a chat message can be created correctly.
        """
        user = User(
            username='testuser', email='test@example.com',
            password='password'
        )
        db.session.add(user)
        db.session.commit()
        message = ChatMessage(
            content='This is a test message.', user=user
        )
        db.session.add(message)
        db.session.commit()
        self.assertEqual(ChatMessage.query.count(), 1)
        self.assertEqual(message.content, 'This is a test message.')
        self.assertEqual(message.user, user)

if __name__ == '__main__':
    unittest.main()
