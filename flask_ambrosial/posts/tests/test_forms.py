#!/usr/bin/env python3

import unittest
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_ambrosial.posts.forms import PostForm, CommentForm, ReplyForm

class TestPostForm(unittest.TestCase):
    def setUp(self):
        self.form = PostForm()

    def test_fields_exist(self):
        self.assertTrue(hasattr(self.form, 'title'))
        self.assertTrue(hasattr(self.form, 'content'))
        self.assertTrue(hasattr(self.form, 'image_filename'))
        self.assertTrue(hasattr(self.form, 'submit'))

    def test_valid_data(self):
        form = PostForm(title="Test Title", content="Test Content")
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        form = PostForm(title="", content="")
        self.assertFalse(form.validate())

class TestCommentForm(unittest.TestCase):
    def setUp(self):
        self.form = CommentForm()

    def test_fields_exist(self):
        self.assertTrue(hasattr(self.form, 'content'))
        self.assertTrue(hasattr(self.form, 'submit'))

    def test_valid_data(self):
        form = CommentForm(content="Test Comment")
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        form = CommentForm(content="")
        self.assertFalse(form.validate())

class TestReplyForm(unittest.TestCase):
    def setUp(self):
        self.form = ReplyForm()

    def test_fields_exist(self):
        self.assertTrue(hasattr(self.form, 'content'))
        self.assertTrue(hasattr(self.form, 'submit'))

    def test_valid_data(self):
        form = ReplyForm(content="Test Reply")
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        form = ReplyForm(content="")
        self.assertFalse(form.validate())

if __name__ == '__main__':
    unittest.main()
