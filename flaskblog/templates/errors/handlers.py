from flask import Blueprint, render_template, current_app

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(401)
def unauthorized_error(error):
    current_app.logger.error(f"Unauthorized access: {error}")
    return render_template('errors/401.html'), 401

@errors.app_errorhandler(403)
def forbidden_error(error):
    current_app.logger.error(f"Forbidden access: {error}")
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(404)
def not_found_error(error):
    current_app.logger.error(f"Page not found: {error}")
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(500)
def internal_error(error):
    current_app.logger.error(f"Internal server error: {error}")
    return render_template('errors/500.html'), 500
