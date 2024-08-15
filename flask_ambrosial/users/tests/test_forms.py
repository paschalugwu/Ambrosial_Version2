import unittest
from flask_ambrosial.users.forms import CommentForm, ReplyForm
from wtforms.validators import ValidationError

class TestCommentForm(unittest.TestCase):
    def setUp(self):
        self.form = CommentForm()

    def test_fields_exist(self):
        self.assertTrue(hasattr(self.form, 'content'))
        self.assertTrue(hasattr(self.form, 'submit'))

    def test_valid_data(self):
        form = CommentForm(content="This is a comment")
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
        form = ReplyForm(content="This is a reply")
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        form = ReplyForm(content="")
        self.assertFalse(form.validate())

if __name__ == '__main__':
    unittest.main()
