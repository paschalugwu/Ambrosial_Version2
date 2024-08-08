#!/usr/bin/env python3

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    """Form for creating a new post.

    Attributes:
        title (StringField): Field for entering the post title.
        content (TextAreaField): Field for entering the post content.
        image_filename (FileField): Field for uploading an image file.
        submit (SubmitField): Button to submit the post form.
    """
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    image_filename = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Post')
