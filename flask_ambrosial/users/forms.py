#!/usr/bin/env python3

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_ambrosial.models import User


class RegistrationForm(FlaskForm):
    """Form for user registration.
    
    Parameters:
        FlaskForm (class): Base class for forms in Flask-WTF.
    
    Attributes:
        username (StringField): Field for user's username.
        email (StringField): Field for user's email.
        password (PasswordField): Field for user's password.
        confirm_password (PasswordField): Field for confirming user's password.
        submit (SubmitField): Button for submitting the form.
    """
    
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Validate uniqueness of username.
        
        Parameters:
            username (StringField): Username entered in the registration form.
        
        Raises:
            ValidationError: If username is already taken.
        """
        
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """Validate uniqueness of email.
        
        Parameters:
            email (StringField): Email entered in the registration form.
        
        Raises:
            ValidationError: If email is already taken.
        """
        
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    """Form for user login.
    
    Parameters:
        FlaskForm (class): Base class for forms in Flask-WTF.
    
    Attributes:
        email (StringField): Field for user's email.
        password (PasswordField): Field for user's password.
        remember (BooleanField): Checkbox for remembering user's login.
        submit (SubmitField): Button for submitting the form.
    """
    
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """Form for updating user account.
    
    Parameters:
        FlaskForm (class): Base class for forms in Flask-WTF.
    
    Attributes:
        username (StringField): Field for user's username.
        email (StringField): Field for user's email.
        picture (FileField): Field for updating user's profile picture.
        submit (SubmitField): Button for submitting the form.
    """
    
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        """Validate uniqueness of username during account update.
        
        Parameters:
            username (StringField): Username entered in the update form.
        
        Raises:
            ValidationError: If username is already taken.
        """
        
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """Validate uniqueness of email during account update.
        
        Parameters:
            email (StringField): Email entered in the update form.
        
        Raises:
            ValidationError: If email is already taken.
        """
        
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    """Form for requesting password reset.
    
    Parameters:
        FlaskForm (class): Base class for forms in Flask-WTF.
    
    Attributes:
        email (StringField): Field for user's email.
        submit (SubmitField): Button for submitting the form.
    """
    
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        """Validate existence of email before requesting password reset.
        
        Parameters:
            email (StringField): Email entered in the reset request form.
        
        Raises:
            ValidationError: If no account is found with the provided email.
        """
        
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    """Form for resetting password.
    
    Parameters:
        FlaskForm (class): Base class for forms in Flask-WTF.
    
    Attributes:
        password (PasswordField): Field for user's new password.
        confirm_password (PasswordField): Field for confirming user's new password.
        submit (SubmitField): Button for submitting the form.
    """
    
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
