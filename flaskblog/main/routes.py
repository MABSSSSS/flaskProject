from flask import Blueprint, render_template, request
from flaskblog.models import Post  # Import the 'Post' model from your application (adjust 'flaskblog' to your app's name)

# Create a Blueprint instance for the 'main' blueprint
# This will group the routes related to the main part of the website
main = Blueprint('main', __name__)

# Define the route for the home page
# The home page can be accessed using the root URL ("/") or "/home"
@main.route("/")
@main.route("/home")
def home():
    # Get the current page number from the URL query parameters (e.g., ?page=2)
    # If no page number is provided, default to page 1
    page = request.args.get('page', 1, type=int)
    
    # Query the 'Post' model to get all posts, ordered by the date they were posted in descending order (newest first)
    # Paginate the results, displaying 2 posts per page
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    
    # Render the 'home.html' template and pass the 'posts' object to it
    # This allows the template to display the posts on the home page
    return render_template('home.html', posts=posts)

# Define the route for the about page
# This page can be accessed using the URL "/about"
@main.route("/about")
def about():
    # Render the 'about.html' template
    # Pass a title variable to the template, which will be used as the page title
    return render_template('about.html', title='About')
