"""
This module initializes a SQLAlchemy object named 'db'. SQLAlchemy is an Object-Relational Mapping (ORM) library
that simplifies database interactions in Flask applications. The 'db' object is utilized throughout the project
to define and interact with the database models, such as 'User', 'Post', and 'Reply'.

The inclusion of this 'db' object in a separate module helps prevent circular or looping imports, ensuring a
clean and organized structure in the application.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# Prevents looping imports.