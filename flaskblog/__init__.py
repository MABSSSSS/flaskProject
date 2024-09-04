from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from dotenv import load_dotenv
import os
from flask_bcrypt import Bcrypt

# Load environment variables
load_dotenv()

# Initialize extensions
bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('flaskblog.config.Config')  # This line should work if config.py is in the correct location
    

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    
    
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors, url_prefix='/errors')
    
    return app
