#!/usr/bin/env python3

"""
Routes for handling post-related operations in the Flask application.
"""

import os
import secrets
from flask import (
    Blueprint, current_app, render_template, url_for, flash, redirect, 
    request, abort, jsonify
)
from flask_login import current_user, login_required
from flask_ambrosial import db
from flask_ambrosial.models import Post, Comment
from flask_ambrosial.posts.forms import PostForm, CommentForm, ReplyForm

# Blueprint for handling post-related routes
posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """
    Create a new post.
    """
    form = PostForm()
    if form.validate_on_submit():
        image_file = form.image_filename.data
        if image_file:
            image_filename = (
                secrets.token_hex(8) + 
                os.path.splitext(image_file.filename)[1]
            )
            image_path = os.path.join(
                current_app.root_path, 'static/post_pics', image_filename
            )
            image_file.save(image_path)
        else:
            flash('Image is required for the post.', 'danger')
            return render_template(
                'create_post.html', title='New Post', form=form, 
                legend='New Post'
            )
        post = Post(
            title=form.title.data, content=form.content.data, 
            image_filename=image_filename, author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('posts.home'))
    else:
        print("Form validation failed")
        print(form.errors)
    return render_template(
        'create_post.html', title='New Post', form=form, legend='New Post'
    )

@posts.route("/post/<int:post_id>", methods=['GET', 'POST'], endpoint='post')
def post(post_id):
    """
    View a specific post and handle comments.
    """
    post = Post.query.get_or_404(post_id)
    comment_form = CommentForm()
    reply_form = ReplyForm()
    if comment_form.validate_on_submit():
        comment = Comment(
            content=comment_form.content.data, author=current_user, post=post
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    return render_template(
        'post.html', title=post.title, post=post, 
        comment_form=comment_form, reply_form=reply_form
    )

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """
    Update an existing post.
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if form.image_filename.data:
            image_file = form.image_filename.data
            image_filename = (
                secrets.token_hex(8) + 
                os.path.splitext(image_file.filename)[1]
            )
            image_path = os.path.join(
                current_app.root_path, 'static/post_pics', image_filename
            )
            image_file.save(image_path)
            post.image_filename = image_filename
        else:
            flash('Image is required for the post.', 'danger')
            return render_template(
                'create_post.html', title='Update Post', form=form, 
                legend='Update Post'
            )
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template(
        'create_post.html', title='Update Post', form=form, 
        legend='Update Post'
    )

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """
    Delete an existing post.
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('posts.home'))

@posts.route("/comments", methods=['POST'])
@login_required
def add_comment():
    """
    Add a new comment to a post.
    """
    data = request.form
    content = data.get('content')
    post_id = data.get('post_id')
    parent_comment_id = data.get('parent_comment_id')

    if not content or not post_id:
        return jsonify({'success': False, 'message': 'Invalid data'}), 400

    comment = Comment(
        content=content, author=current_user, post_id=post_id, 
        parent_id=parent_comment_id
    )
    db.session.add(comment)
    db.session.commit()

    flash('Your comment has been posted!', 'success')
    return redirect(url_for('posts.post', post_id=post_id))

@posts.route("/comments", methods=['GET'])
def get_comments():
    """
    Retrieve comments for a specific post.
    """
    post_id = request.args.get('post_id')
    if not post_id:
        return jsonify({'success': False, 'message': 'Invalid post ID'}), 400

    comments = Comment.query.filter_by(
        post_id=post_id, parent_id=None
    ).all()
    comments_data = []
    for comment in comments:
        comments_data.append({
            'id': comment.id,
            'content': comment.content,
            'timestamp': comment.date_posted,
            'author': {
                'name': comment.author.username,
                'profile_picture': url_for(
                    'static', filename='profile_pics/' + 
                    comment.author.image_file
                )
            }
        })

    return jsonify({'success': True, 'comments': comments_data}), 200

def get_replies(comment_id):
    """
    Retrieve replies for a specific comment.
    """
    replies = Comment.query.filter_by(parent_id=comment_id).all()
    replies_data = []
    for reply in replies:
        replies_data.append({
            'id': reply.id,
            'content': reply.content,
            'timestamp': reply.date_posted,
            'author': {
                'name': reply.author.username,
                'profile_picture': url_for(
                    'static', filename='profile_pics/' + 
                    reply.author.image_file
                )
            }
        })
    return replies_data

@posts.route("/")
@posts.route("/home")
def home():
    """
    Display the home page with paginated posts.
    """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()
    ).paginate(page=page, per_page=5)
    post_form = PostForm()
    comment_form = CommentForm()
    reply_form = ReplyForm()
    return render_template(
        'home.html', posts=posts, post_form=post_form, 
        comment_form=comment_form, reply_form=reply_form
    )

@posts.route("/comment/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    """
    Delete a specific comment.
    """
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted', 'success')
    return redirect(url_for('posts.home'))

@posts.route("/reply/<int:reply_id>/delete", methods=['POST'])
@login_required
def delete_reply(reply_id):
    """
    Delete a specific reply.
    """
    reply = Comment.query.get_or_404(reply_id)
    if reply.author != current_user:
        abort(403)
    db.session.delete(reply)
    db.session.commit()
    flash('Your reply has been deleted', 'success')
    return redirect(url_for('posts.home'))

@posts.route("/comment/<int:comment_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    """
    Edit a specific comment.
    """
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    form = CommentForm()
    if form.validate_on_submit():
        comment.content = form.content.data
        db.session.commit()
        flash('Your comment has been updated', 'success')
        return redirect(url_for('posts.post', post_id=comment.post_id))
    elif request.method == 'GET':
        form.content.data = comment.content
    return render_template(
        'edit_comment.html', title='Edit Comment', form=form, 
        legend='Edit Comment'
    )

@posts.route("/reply/<int:reply_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_reply(reply_id):
    """
    Edit a specific reply.
    """
    reply = Comment.query.get_or_404(reply_id)
    if reply.author != current_user:
        abort(403)
    form = ReplyForm()
    if form.validate_on_submit():
        reply.content = form.content.data
        db.session.commit()
        flash('Your reply has been updated', 'success')
        return redirect(url_for('posts.post', post_id=reply.post_id))
    elif request.method == 'GET':
        form.content.data = reply.content
    return render_template(
        'edit_comment.html', title='Edit Reply', form=form, 
        legend='Edit Reply'
    )

@posts.route(
    "/post/<int:post_id>/comment/<int:comment_id>/delete", 
    methods=['POST'], endpoint='delete_post_comment'
)
@login_required
def delete_post_comment(post_id, comment_id):
    """
    Delete a comment from a specific post.
    """
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted', 'success')
    return redirect(url_for('posts.post', post_id=post_id))

@posts.route(
    "/post/<int:post_id>/reply/<int:reply_id>/delete", 
    methods=['POST'], endpoint='delete_post_reply'
)
@login_required
def delete_post_reply(post_id, reply_id):
    """
    Delete a reply from a specific post.
    """
    reply = Comment.query.get_or_404(reply_id)
    if reply.author != current_user:
        abort(403)
    db.session.delete(reply)
    db.session.commit()
    flash('Your reply has been deleted', 'success')
    return redirect(url_for('posts.post', post_id=post_id))

@posts.route(
    "/post/<int:post_id>/comment/<int:comment_id>/edit", 
    methods=['GET', 'POST'], endpoint='edit_post_comment'
)
@login_required
def edit_post_comment(post_id, comment_id):
    """
    Edit a comment on a specific post.
    """
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    form = CommentForm()
    if form.validate_on_submit():
        comment.content = form.content.data
        db.session.commit()
        flash('Your comment has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.content.data = comment.content
    return render_template(
        'edit_comment.html', title='Edit Comment', form=form, 
        legend='Edit Comment'
    )

@posts.route(
    "/post/<int:post_id>/reply/<int:reply_id>/edit", 
    methods=['GET', 'POST'], endpoint='edit_post_reply'
)
@login_required
def edit_post_reply(post_id, reply_id):
    """
    Edit a reply on a specific post.
    """
    reply = Comment.query.get_or_404(reply_id)
    if reply.author != current_user:
        abort(403)
    form = ReplyForm()
    if form.validate_on_submit():
        reply.content = form.content.data
        db.session.commit()
        flash('Your reply has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.content.data = reply.content
    return render_template(
        'edit_comment.html', title='Edit Reply', form=form, 
        legend='Edit Reply'
    )
