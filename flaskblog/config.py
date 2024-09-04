import os

class Config:
    # Set the database URI for SQLAlchemy, using an environment variable if available
    # If the environment variable is not set, use a default PostgreSQL connection string
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:1234@localhost:5432/flask')
    
    # Set the secret key for the application, which is used for sessions and cryptographic operations
    # It is crucial to set this to a secure value in a production environment
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')  # Ensure this is set
    
    # Configure the mail server settings for sending emails
    # Defaults to Gmail's SMTP server
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    
    # Set the mail server port, convert from string to integer
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))  # Convert to integer
    
    # Set whether to use TLS for secure email transmission
    # Convert from string to boolean
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', '1') == '1'  # Convert to boolean
    
    # Set the username and password for the mail server, fetched from environment variables
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    
    # Controls whether exceptions should be propagated or handled by Flask
    PROPAGATE_EXCEPTIONS = False
