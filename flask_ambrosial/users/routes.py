#!/usr/bin/env python3

from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_ambrosial import db, bcrypt
from flask_ambrosial.models import User, Post
from flask_ambrosial.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flask_ambrosial.users.utils import save_picture, send_reset_email

# Define a Blueprint for user-related routes
users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """Handle user registration.

    If the user is already authenticated, redirects to the home page.
    If the registration form is submitted, validates the form data, hashes
    the password, creates a new user, adds them to the database, and redirects
    to the login page.

    Returns:
        Response: Redirects to the login page if registration is successful.
        Template: Renders the register.html template with the registration form.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)\
            .decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! \
            You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    """Handle user login.

    If the user is already authenticated, redirects to the home page.
    If the login form is submitted, validates the form data, checks if the
    user exists and the password is correct, logs in the user, and redirects
    to the next page or home page.

    Returns:
        Response: Redirects to the next page if specified, else to the home page.
        Template: Renders the login.html template with the login form.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else \
                redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. \
                Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    """Handle user logout.

    Logs out the user and redirects to the home page.

    Returns:
        Response: Redirects to the home page.
    """
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """Handle user account settings and update.

    Renders the account page with the update account form. If the form is
    submitted and valid, updates the user's account information and picture.

    Returns:
        Response: Redirects to the account page after updating the account.
        Template: Renders the account.html template with the update account form.
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
    

@users.route("/user/<string:username>")
def user_posts(username):
    """Display posts by a specific user.

    Args:
        username (str): The username of the user whose posts are to be displayed.

    Returns:
        Template: Renders the user_posts.html template with the user's posts.
    """
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=3)
    image_files = []
    for post in posts:
        image_files.append(url_for('static', filename='post_pics/' + post.image_filename))
    return render_template('user_posts.html', posts=posts, image_files=image_files, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """Handle password reset request.

    If the user is already authenticated, redirects to the home page.
    If the reset password form is submitted, sends an email with instructions
    to reset the password.

    Returns:
        Response: Redirects to the login page after sending the reset email.
        Template: Renders the reset_request.html template with the reset password form.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """Handle password reset token verification.

    If the user is already authenticated, redirects to the home page.
    Verifies the password reset token and allows the user to reset their password.

    Args:
        token (str): The password reset token.

    Returns:
        Response: Redirects to the login page after successfully resetting the password.
        Template: Renders the reset_token.html template with the reset password form.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
