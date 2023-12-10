"""
This file defines FlaskForm classes using Flask-WTF for form handling. The 'PostForm' class, in particular, is
used to create a form for handling post creation and updating. It includes fields for the post title and content,
both of which are required. The form is utilized in the 'create_post' and 'update_post' routes in 'app.py'.

The 'title' field is a StringField, representing the title of the post, and the 'content' field is a TextAreaField,
representing the main content of the post. Validators are applied to ensure that both fields are required.

This form helps maintain a consistent structure for handling post-related data input on the website.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Pet Care Tips', 'Pet Care Tips'),
        ('Adoption Stories', 'Adoption Stories'),
        ('Veterinary Advice', 'Veterinary Advice'),
        ('Pet Behavior', 'Pet Behavior'),
        ('Wildlife Conservation', 'Wildlife Conservation'),
        ('Lost and Found', 'Lost and Found'),
        ('Animal-friendly Travel', 'Animal-friendly Travel'),
        ('Pet Product Reviews', 'Pet Product Reviews'),
        ('Local Animal Events', 'Local Animal Events'),
    ], validators=[DataRequired()])
# Contains the text-area-field used when posting or replying