from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

# Define a form class for creating or editing blog posts
class PostForm(FlaskForm):
    # A title field for the post, which is a simple text input
    # 'DataRequired()' validator ensures that the title field cannot be empty
    title = StringField('Title', validators=[DataRequired()])
    
    # A content field for the post, which is a larger text area input
    # 'DataRequired()' validator ensures that the content field cannot be empty
    content = TextAreaField('Content', validators=[DataRequired()])
    
    # A submit button for submitting the form
    submit = SubmitField('Post')
