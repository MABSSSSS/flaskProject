from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, User
from flaskblog.users.forms import UpdateAccountForm
from flaskblog.posts.forms import PostForm
from flaskblog.users.utils import save_picture

# Create a Blueprint instance for the 'posts' blueprint
# This will handle all routes related to posts
posts = Blueprint('posts', __name__)

# Define the route for the user's account page, which requires the user to be logged in
@posts.route("/account", methods=['GET', 'POST'])
@login_required  # This decorator ensures that the user must be logged in to access this route
def account():
    # Create an instance of the UpdateAccountForm form
    form = UpdateAccountForm()
    # Check if the form has been submitted and is valid
    if form.validate_on_submit():
        # If the user has uploaded a new profile picture, save it
        if form.picture.data:
            # Save the picture using the save_picture function and store the filename
            picture_file = save_picture(form.picture.data)
            # Update the current user's image file in the database
            current_user.image_file = picture_file
        # Update the current user's username and email with the new data from the form
        current_user.username = form.username.data
        current_user.email = form.email.data
        # Commit the changes to the database
        db.session.commit()
        # Flash a success message to the user
        flash('Your account has been updated!', 'success')
        # Redirect the user back to the account page
        return redirect(url_for('posts.account'))
    # If the request method is GET, populate the form with the current user's data
    elif request.method == 'GET':
        # Set the form's username and email fields to the current user's data
        form.username.data = current_user.username
        form.email.data = current_user.email

    # Get the URL of the current user's profile image
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # Render the account.html template, passing in the image file and form data
    return render_template('account.html', title='Account', image_file=image_file, form=form)

# Define the route for creating a new post, which requires the user to be logged in
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required  # This decorator ensures that the user must be logged in to access this route
def new_post():
    # Create an instance of the PostForm form
    form = PostForm()
    # Check if the form has been submitted and is valid
    if form.validate_on_submit():
        # Create a new Post object with the form data and set the current user as the author
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        # Add the new post to the database session
        db.session.add(post)
        # Commit the changes to the database
        db.session.commit()
        # Flash a success message to the user
        flash('Your post has been created!', 'success')
        # Redirect the user to the home page
        return redirect(url_for('main.home'))  # Adjust the redirect if necessary

    # Render the create_post.html template, passing in the form data and a legend
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

# Define the route for viewing a post by its ID
@posts.route("/post/<int:post_id>")
def post(post_id):
    # Query the database for the post with the given ID
    post = Post.query.get_or_404(post_id)
    # Render the post.html template, passing in the post data
    return render_template('post.html', title=post.title, post=post)

# Define the route for updating a post, which requires the user to be logged in
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required  # This decorator ensures that the user must be logged in to access this route
def update_post(post_id):
    # Query the database for the post with the given ID
    post = Post.query.get_or_404(post_id)
    # Check if the current user is the author of the post
    if post.author != current_user:
        # If not, abort the request with a 403 Forbidden error
        abort(403)
    # Create an instance of the PostForm form
    form = PostForm()
    # Check if the form has been submitted and is valid
    if form.validate_on_submit():
        # Update the post's title and content with the new data from the form
        post.title = form.title.data
        post.content = form.content.data
        # Commit the changes to the database
        db.session.commit()
        # Flash a success message to the user
        flash('Your post has been updated!', 'success')
        # Redirect the user to the updated post's page
        return redirect(url_for('posts.post', post_id=post.id))
    # If the request method is GET, populate the form with the post's current data
    elif request.method == 'GET':
        # Set the form's title and content fields to the post's current data
        form.title.data = post.title
        form.content.data = post.content
    # Render the create_post.html template, passing in the form data and a legend
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

# Define the route for deleting a post, which requires the user to be logged in
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required  # This decorator ensures that the user must be logged in to access this route
def delete_post(post_id):
    # Query the database for the post with the given ID
    post = Post.query.get_or_404(post_id)
    # Check if the current user is the author of the post
    if post.author != current_user:
        # If not, abort the request with a 403 Forbidden error
        abort(403)
    # Delete the post from the database
    db.session.delete(post)
    # Commit the changes to the database
    db.session.commit()
    # Flash a success message to the user
    flash('Your post has been deleted!', 'success')
    # Redirect the user to the home page
    return redirect(url_for('main.home'))  # Adjust the redirect if necessary

# Define the route for viewing posts by a specific user
@posts.route("/user/<username>")
def user_posts(username):
    # Query the database for the user with the given username
    user = User.query.filter_by(username=username).first_or_404()
    # Query the database for all posts by this user
    posts = Post.query.filter_by(author=user).all()
    # Render the user_posts.html template, passing in the posts and user data
    return render_template('user_posts.html', posts=posts, user=user)
