from flaskblog import app, db  # Import your app and db object

with app.app_context():  # Set up the application context
    db.create_all()  # Create database tables
print("Database tables created.")