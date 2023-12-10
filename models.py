"""
This module defines the database models for the Flask application. It utilizes Flask-SQLAlchemy
to create User, Post, and Reply models that represent the structure of the application's database.
These models include relationships between users, posts, and likes.
Classes:
- User: Represents a registered user with associated posts and likes.
- Post: Represents a forum post with an author, title, content, and associated replies.
- Reply: Represents a reply to a post with an author, content, and timestamp.
Table:
- likes: A many-to-many association table to store the likes relationship between users and posts.
"""

from flask_login import UserMixin
from extensions import db
from datetime import datetime

likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    liked_posts = db.relationship('Post', secondary=likes, backref=db.backref('likers', lazy='dynamic'))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50), nullable=False) 


    author = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f"Post('{self.title}', '{self.author.username}', '{self.created_at}')"
    
class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.relationship('User', backref='replies')
    post = db.relationship('Post', backref='replies')
    