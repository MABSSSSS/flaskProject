from flaskblog import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

# Define a callback function to load a user by their user_id
@login_manager.user_loader
def load_user(user_id):
    """
    Load a user by their user_id.
    
    :param user_id: The ID of the user to be loaded.
    :return: The User object corresponding to the user_id.
    """
    return User.query.get(int(user_id))

# Define the User model
class User(db.Model, UserMixin):
    """
    User model representing users in the application.
    
    Attributes:
    - id: Unique identifier for the user.
    - username: The user's username, must be unique and non-nullable.
    - email: The user's email, must be unique and non-nullable.
    - image_file: Path to the user's profile picture.
    - password: The hashed password for the user.
    - posts: Relationship to the Post model, representing posts authored by the user.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def get_reset_token(self, expires_sec=1800):
        """
        Generate a reset token for the user, expiring after a specified number of seconds.
        
        :param expires_sec: The number of seconds until the token expires.
        :return: The reset token as a string.
        """
        # Create a serializer instance with the secret key and expiration time
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_sec)
        # Serialize the user_id into the token
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        """
        Verify the reset token and return the corresponding user.
        
        :param token: The token to be verified.
        :return: The User object if the token is valid, otherwise None.
        """
        # Create a serializer instance with the secret key
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            # Deserialize the token to retrieve the user_id
            user_id = s.loads(token)['user_id']
        except (BadSignature, SignatureExpired):
            # If the token is invalid or expired, return None
            return None
        # Return the User object corresponding to the user_id
        return User.query.get(user_id)
    
    def __repr__(self):
        """
        Return a string representation of the User object.
        
        :return: A string showing the username, email, and image_file.
        """
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# Define the Post model
class Post(db.Model):
    """
    Post model representing blog posts in the application.
    
    Attributes:
    - id: Unique identifier for the post.
    - title: The title of the post, must be non-nullable.
    - date_posted: The date and time when the post was created.
    - content: The content of the post, must be non-nullable.
    - user_id: Foreign key to the User model, representing the post's author.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    
    def __repr__(self):
        """
        Return a string representation of the Post object.
        
        :return: A string showing the title and date_posted.
        """
        return f"Post('{self.title}', '{self.date_posted}')"
