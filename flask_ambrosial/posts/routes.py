#!/usr/bin/env python3

import os
import secrets
from flask import Blueprint, current_app, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from flask_ambrosial import db
from flask_ambrosial.models import Post
from flask_ambrosial.posts.forms import PostForm

# Blueprint for handling post-related routes
posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """
    Route for creating a new post.

    Renders the form for creating a new post. On form submission, validates the form data and creates
    a new post entry in the database. If an image is uploaded with the post, it is saved and processed.
    """
    form = PostForm()
    if form.validate_on_submit():
        image_file = form.image_filename.data
        if image_file:
            # Save and process the uploaded image if provided
            image_filename = secrets.token_hex(8)
            _, f_ext = os.path.splitext(image_file.filename)
            image_filename = image_filename + f_ext
            image_path = os.path.join(current_app.root_path, 'static/post_pics', image_filename)
            image_file.save(image_path)
        else:
            # Set image filename to an empty string if no image is uploaded
            image_filename = ''

        # Create a new post with the filename of the uploaded image
        post = Post(title=form.title.data, content=form.content.data, image_filename=image_filename, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    """
    Route for viewing a specific post.

    Retrieves the post with the given ID from the database and renders the post view template
    with the post data.
    """
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """
    Route for updating an existing post.

    Retrieves the post with the given ID from the database and renders the form for updating
    the post. On form submission, validates the form data and updates the post entry in the database.
    If an image is uploaded with the update, it is saved and processed.
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if form.image_filename.data:
            # Save and process the uploaded image if provided
            image_file = form.image_filename.data
            image_filename = secrets.token_hex(8)
            _, f_ext = os.path.splitext(image_file.filename)
            image_filename = image_filename + f_ext
            image_path = os.path.join(current_app.root_path, 'static/post_pics', image_filename)
            image_file.save(image_path)
            post.image_filename = image_filename
        else:
            post.image_filename = None  # Set image filename to None if no image is uploaded
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """
    Route for deleting an existing post.

    Retrieves the post with the given ID from the database and deletes it. Only the author of the post
    can delete it. After deletion, redirects to the home page with a success flash message.
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('main.home'))
