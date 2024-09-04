import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def save_picture(form_picture):
    """
    Save a profile picture to the static folder after resizing it.
    Generates a random filename to avoid conflicts.

    :param form_picture: The picture file from the form.
    :return: The new filename of the saved picture.
    """
    try:
        # Generate a random 8-byte hex string for the new filename to ensure it's unique
        random_hex = secrets.token_hex(8)
        # Split the original filename into name and extension
        _, f_ext = os.path.splitext(form_picture.filename)
        # Combine the random hex string with the original file extension for the new filename
        picture_fn = random_hex + f_ext
        # Create the full file path in the 'static/profile_pics' directory of your app
        picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

        # Set the desired output size for the image (125x125 pixels)
        output_size = (125, 125)
        # Open the uploaded image using PIL (Python Imaging Library)
        i = Image.open(form_picture)
        # Resize the image to the specified output size, maintaining aspect ratio
        i.thumbnail(output_size)
        # Save the resized image to the specified path
        i.save(picture_path)

        # Return the filename of the saved image to store in the database
        return picture_fn
    except Exception as e:
        # Handle and log any exceptions that occur during the image saving process
        print(f"Error saving picture: {e}")
        raise  # Re-raise the exception after logging it

def send_reset_email(user):
    """
    Send a password reset email to the user with a link to reset the password.

    :param user: The user object containing email and reset token method.
    """
    try:
        # Generate a password reset token for the user
        token = user.get_reset_token()
        # Create a new email message object with a subject and sender information
        msg = Message('Password Reset Request',
                      sender=current_app.config['MAIL_DEFAULT_SENDER'],
                      recipients=[user.email])
        
        # Construct the email body with a link to the reset password page
        msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
        
If you did not make this request, please ignore this email and no changes will be made.
'''
        # Send the email message using Flask-Mail's `send` method
        mail.send(msg)
    except Exception as e:
        # Handle and log any exceptions that occur during the email sending process
        print(f"Error sending email: {e}")
        raise  # Re-raise the exception after logging it
