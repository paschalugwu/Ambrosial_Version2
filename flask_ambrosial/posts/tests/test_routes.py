#!/usr/bin/env python3

import unittest
from flask import url_for
from flask_ambrosial import create_app, db
from flask_ambrosial.models import User, Post, Comment
from flask_login import login_user
from flask_ambrosial.config import TestingConfig

class PostRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.create_test_user()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_test_user(self):
        user = User.query.filter_by(email='test@example.com').first()
        if not user:
            self.user = User(username='testuser', email='test@example.com', password='password')
            db.session.add(self.user)
            db.session.commit()
        else:
            self.user = user
        
        with self.client:
            with self.app.test_request_context():
                login_user(self.user)

    def test_new_post(self):
        with self.app.test_request_context():
            response = self.client.post(url_for('posts.new_post'), data={
                'title': 'Test Post',
                'content': 'This is a test post.',
                'image_filename': 'default.jpg'
            }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your post has been created!', response.data)

    def test_post(self):
        post = Post(title='Test Post', content='This is a test post.', author=self.user, image_filename='default.jpg')
        db.session.add(post)
        db.session.commit()
        with self.app.test_request_context():
            response = self.client.get(url_for('posts.post', post_id=post.id))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Post', response.data)

    def test_update_post(self):
        post = Post(title='Test Post', content='This is a test post.', author=self.user, image_filename='default.jpg')
        db.session.add(post)
        db.session.commit()
        with self.app.test_request_context():
            with open('flask_ambrosial/static/post_pics/f64d8aab113b14aa.jpg', 'rb') as img:
                response = self.client.post(url_for('posts.update_post', post_id=post.id), data={
                    'title': 'Updated Post',
                    'content': 'This is an updated test post.',
                    'image_filename': (img, 'test_image.jpg')
                }, content_type='multipart/form-data', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your post has been updated', response.data)

    def test_delete_post(self):
        post = Post(title='Test Post', content='This is a test post.', author=self.user, image_filename='default.jpg')
        db.session.add(post)
        db.session.commit()
        with self.app.test_request_context():
            response = self.client.post(url_for('posts.delete_post', post_id=post.id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your post has been deleted', response.data)

    def test_add_comment(self):
        post = Post(title='Test Post', content='This is a test post.', author=self.user, image_filename='default.jpg')
        db.session.add(post)
        db.session.commit()
        with self.app.test_request_context():
            response = self.client.post(url_for('posts.add_comment'), data={
                'content': 'This is a test comment.',
                'post_id': post.id
            }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your comment has been posted!', response.data)

    def test_get_comments(self):
        post = Post(title='Test Post', content='This is a test post.', author=self.user, image_filename='default.jpg')
        db.session.add(post)
        db.session.commit()
        comment = Comment(content='This is a test comment.', author=self.user, post=post)
        db.session.add(comment)
        db.session.commit()
        with self.app.test_request_context():
            response = self.client.get(url_for('posts.get_comments', post_id=post.id))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is a test comment.', response.data)

    def test_delete_comment(self):
        post = Post(title='Test Post', content='This is a test post.', author=self.user, image_filename='default.jpg')
        db.session.add(post)
        db.session.commit()
        comment = Comment(content='This is a test comment.', author=self.user, post=post)
        db.session.add(comment)
        db.session.commit()
        with self.app.test_request_context():
            response = self.client.post(url_for('posts.delete_comment', comment_id=comment.id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your comment has been deleted', response.data)

    def test_edit_comment(self):
        post = Post(title='Test Post', content='This is a test post.', author=self.user, image_filename='default.jpg')
        db.session.add(post)
        db.session.commit()
        comment = Comment(content='This is a test comment.', author=self.user, post=post)
        db.session.add(comment)
        db.session.commit()
        with self.app.test_request_context():
            response = self.client.post(url_for('posts.edit_comment', comment_id=comment.id), data={
                'content': 'This is an edited test comment.'
            }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your comment has been updated', response.data)

    def test_delete_reply(self):
        post = Post(title='Test Post', content='This is a test post.', author=self.user, image_filename='default.jpg')
        db.session.add(post)
        db.session.commit()
        comment = Comment(content='This is a test comment.', author=self.user, post=post)
        db.session.add(comment)
        db.session.commit()
        reply = Comment(content='This is a test reply.', author=self.user, post=post, parent=comment)
        db.session.add(reply)
        db.session.commit()
        with self.app.test_request_context():
            response = self.client.post(url_for('posts.delete_reply', reply_id=reply.id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your reply has been deleted', response.data)

    def test_edit_reply(self):
        post = Post(title='Test Post', content='This is a test post.', author=self.user, image_filename='default.jpg')
        db.session.add(post)
        db.session.commit()
        comment = Comment(content='This is a test comment.', author=self.user, post=post)
        db.session.add(comment)
        db.session.commit()
        reply = Comment(content='This is a test reply.', author=self.user, post=post, parent=comment)
        db.session.add(reply)
        db.session.commit()
        with self.app.test_request_context():
            response = self.client.post(url_for('posts.edit_reply', reply_id=reply.id), data={
                'content': 'This is an edited test reply.'
            }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your reply has been updated', response.data)

if __name__ == '__main__':
    unittest.main()
