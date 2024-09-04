from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, 
                                   RequestResetForm, ResetPasswordForm, UpdateAccountForm)
from flaskblog.users.utils import send_reset_email
from flask import abort

# Create a Blueprint for user-related routes
users = Blueprint('users', __name__)

# Create a Blueprint for testing error routes
errors_test = Blueprint('errors_test', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    # Redirect to home if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # Instantiate the registration form
    form = RegistrationForm()
    
    # Check if the form is submitted and valid
    if form.validate_on_submit():
        # Hash the password from the form data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Create a new User object with the form data
        user = User(username=form.username.data, email=form.email.data, image_file='default.jpg', password=hashed_password)
        # Add the new user to the database session
        db.session.add(user)
        # Commit the session to save the user to the database
        db.session.commit()
        # Flash a success message and redirect to the login page
        flash('Account created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    
    # Render the registration template with the form
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    # Redirect to home if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # Instantiate the login form
    form = LoginForm()
    
    # Check if the form is submitted and valid
    if form.validate_on_submit():
        # Query the user by the email from the form
        user = User.query.filter_by(email=form.email.data).first()
        # Verify the user's password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Log in the user and remember them if the 'remember' checkbox is checked
            login_user(user, remember=form.remember.data)
            # Redirect to the next page if specified, otherwise go to the home page
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            # Flash a danger message if login is unsuccessful
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    # Render the login template with the form
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    # Log out the current user
    logout_user()
    # Redirect to the home page
    return redirect(url_for('main.home'))

@users.route("/user/<string:username>")
@login_required
def user_posts(username):
    # Get the page number from the request, default to 1
    page = request.args.get('page', 1, type=int)
    # Query the user by username, return 404 if not found
    user = User.query.filter_by(username=username).first_or_404()
    # Query posts by the user, ordered by date, and paginate the results
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # Render the user_posts template with the user's posts and user object
    return render_template('user_posts.html', posts=posts, user=user)

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    # Instantiate the update account form
    form = UpdateAccountForm()
    
    # Check if the form is submitted and valid
    if form.validate_on_submit():
        # Update the current user's username and email with the form data
        current_user.username = form.username.data
        current_user.email = form.email.data
        # Commit the changes to the database
        db.session.commit()
        # Flash a success message and redirect to the account page
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        # Pre-fill the form with the current user's data when loading the page
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    # Render the account template with the form
    return render_template('account.html', title='Account', form=form)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # Redirect to home if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # Instantiate the password reset request form
    form = RequestResetForm()
    
    # Check if the form is submitted and valid
    if form.validate_on_submit():
        # Query the user by email from the form
        user = User.query.filter_by(email=form.email.data).first()
        # Send the password reset email to the user
        send_reset_email(user)
        # Flash an info message and redirect to the login page
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    
    # Render the reset request template with the form
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # Redirect to home if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # Verify the reset token and get the user
    user = User.verify_reset_token(token)
    if user is None:
        # Flash a warning message if the token is invalid or expired
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    
    # Instantiate the reset password form
    form = ResetPasswordForm()
    
    # Check if the form is submitted and valid
    if form.validate_on_submit():
        # Hash the new password from the form data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Update the user's password in the database
        user.password = hashed_password
        db.session.commit()
        # Flash a success message and redirect to the login page
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    
    # Render the reset token template with the form
    return render_template('reset_token.html', title='Reset Password', form=form)

# Error testing routes to trigger specific HTTP error codes
@errors_test.route('/trigger_401')
def trigger_401():
    abort(401)  # Trigger a 401 Unauthorized error

@errors_test.route('/trigger_403')
def trigger_403():
    abort(403)  # Trigger a 403 Forbidden error

@errors_test.route('/trigger_404')
def trigger_404():
    abort(404)  # Trigger a 404 Not Found error

@errors_test.route('/trigger_500')
def trigger_500():
    abort(500)  # Trigger a 500 Internal Server Error

# Register this blueprint in your application setup
