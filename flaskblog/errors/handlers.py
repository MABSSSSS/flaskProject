from flask import Blueprint, render_template

# Create a new Blueprint named 'errors' for handling error routes
# 'errors' is the blueprint name, and '__name__' is the current module name
errors = Blueprint('errors', __name__)

# Handle 404 (Not Found) errors with a custom error page
# The 'app_errorhandler' decorator is used to register the error handler for this blueprint
@errors.app_errorhandler(404)
def error_404(error):
    # Render the '404.html' template located in the 'errors' directory
    # Return a 404 status code to indicate that the requested page was not found
    return render_template('errors/404.html'), 404

# Handle 403 (Forbidden) errors with a custom error page
@errors.app_errorhandler(403)
def error_403(error):
    # Render the '403.html' template located in the 'errors' directory
    # Return a 403 status code to indicate that the request is forbidden
    return render_template('errors/403.html'), 403

# Handle 500 (Internal Server Error) with a custom error page
@errors.app_errorhandler(500)
def error_500(error):
    # Render the '500.html' template located in the 'errors' directory
    # Return a 500 status code to indicate a server-side error
    return render_template('errors/500.html'), 500
