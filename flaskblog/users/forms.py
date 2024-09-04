from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed
from flask_login import current_user
from flaskblog.models import User  # Ensure this is your User model from your models.py

# Define the RegistrationForm class, inheriting from FlaskForm
class RegistrationForm(FlaskForm):
    """
    A form for user registration with fields for username, email, password, and password confirmation.
    Includes custom validation to check if the username or email already exists in the database.
    """
    
    # Username field with validation for required input and length constraints
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=100)])
    
    # Email field with validation for required input and ensuring valid email format
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    
    # Password field with validation for required input
    password = PasswordField('Password', validators=[DataRequired()])
    
    # Confirm Password field with validation for required input and ensuring it matches the password
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    
    # Submit button for the registration form
    submit = SubmitField('Sign Up')
    
    # Custom validator to check if the username already exists in the database
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            # If the username is taken, raise a validation error
            raise ValidationError('That username is taken. Please choose a different one.')
    
    # Custom validator to check if the email already exists in the database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            # If the email is taken, raise a validation error
            raise ValidationError('That email is taken. Please choose a different one.')

# Define the LoginForm class, inheriting from FlaskForm
class LoginForm(FlaskForm):
    """
    A form for user login with fields for email, password, and a 'remember me' checkbox.
    """
    
    # Email field with validation for required input and ensuring valid email format
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    
    # Password field with validation for required input
    password = PasswordField('Password', validators=[DataRequired()])
    
    # Boolean field for 'remember me' option, allowing the user to stay logged in
    remember = BooleanField('Remember me')
    
    # Submit button for the login form
    submit = SubmitField('Login')

# Define the UpdateAccountForm class, inheriting from FlaskForm
class UpdateAccountForm(FlaskForm):
    """
    A form for updating user account information with fields for username, email, and profile picture.
    Includes custom validation to check if the username or email already exists in the database.
    """
    
    # Username field with validation for required input and length constraints
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=100)])
    
    # Email field with validation for required input and ensuring valid email format
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    
    # File field for updating profile picture, allowing only 'jpg' and 'png' file types
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    
    # Submit button for the account update form
    submit = SubmitField('Update')
    
    # Custom validator to check if the username already exists in the database, excluding the current user's username
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                # If the username is taken, raise a validation error
                raise ValidationError('That username is taken. Please choose a different one.')
    
    # Custom validator to check if the email already exists in the database, excluding the current user's email
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                # If the email is taken, raise a validation error
                raise ValidationError('That email is taken. Please choose a different one.')

# Define the RequestResetForm class, inheriting from FlaskForm
class RequestResetForm(FlaskForm):
    """
    A form to request a password reset. It includes a field for the user's email.
    """
    
    # Email field with validation for required input and ensuring valid email format
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    # Submit button for the password reset request form
    submit = SubmitField('Request Password Reset')
    
    # Custom validator to check if the email exists in the database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            # If the email is not found, raise a validation error
            raise ValidationError('There is no account with that email. You must register first.')

# Define the ResetPasswordForm class, inheriting from FlaskForm
class ResetPasswordForm(FlaskForm):
    """
    A form to reset the user's password with fields for the new password and confirmation.
    """
    
    # Password field with validation for required input
    password = PasswordField('Password', validators=[DataRequired()])
    
    # Confirm Password field with validation for required input and ensuring it matches the password
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    
    # Submit button for the password reset form
    submit = SubmitField('Reset Password')
