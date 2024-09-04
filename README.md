Flask Blog Application
A full-featured blog application built using the Flask framework, integrated with PostgreSQL as the database. This application allows users to register, log in, create posts, edit profiles, and interact with other users' content. The application also includes features such as password reset, email notifications, pagination, and more.

Features
User Authentication:

Register new users with username and email validation.
Log in and log out functionality.
Password hashing using Flask-Bcrypt.
Password reset via email using Flask-Mail.
User Profiles:

Update account details such as username, email, and profile picture.
View user-specific posts.
Blog Posts:

Create, update, and delete blog posts.
Paginated display of posts.
View individual user posts.
Security:

CSRF protection using Flask-WTF.
Secure password storage with bcrypt hashing.
User session management with Flask-Login.
Database Management:

PostgreSQL as the database backend.
Migrations handled by Flask-Migrate for easy schema updates.
Error Handling:

Custom error pages for 404, 403, and 500 errors.
Responsive UI:

Clean and responsive interface using Bootstrap.
Tech Stack
Backend:

Flask - A lightweight WSGI web application framework.
PostgreSQL - A powerful, open-source object-relational database system.
SQLAlchemy - SQL toolkit and Object-Relational Mapping (ORM) library for Python.
Flask-Migrate - Extension that handles SQLAlchemy database migrations for Flask applications using Alembic.
Flask-Mail - Flask extension for sending email messages.
Flask-Login - User session management for Flask.
Flask-WTF - Simple integration of Flask and WTForms.
Frontend:

Bootstrap - CSS framework for responsive and mobile-first web development.
