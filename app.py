"""
This script serves as the main entry point for the Flask application. It defines the web routes,
handles user authentication, and interacts with the database models using Flask-SQLAlchemy.
The application includes features such as user registration, login, logout, post creation, viewing posts,
updating posts, deleting posts, liking posts, and more.

Routes:
- /: Homepage route.
- /register: User registration route.
- /login: User login route.
- /logout: User logout route.
- /forum: Forum main page route.
- /posts: Route for displaying all forum posts.
- /create_post: Route for creating a new post.
- /view_post/<int:post_id>: Route for viewing a specific post.
- /update_post/<int:post_id>: Route for updating a post.
- /delete_post/<int:post_id>: Route for deleting a post.
- /like_post/<int:post_id>: Route for liking a post.
- /about_us: Route for the "About Us" page.
- /user_list: Route for displaying a list of registered users.

Additionally, it configures the Flask application, sets up user authentication using Flask-Login,
and defines the SQLAlchemy models for User, Post, and Reply.
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from models import User, Post, Reply
from extensions import db
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from forms import PostForm

app = Flask(__name__)
# Configure the SQLAlchemy database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:[REDACTED]@localhost:3306/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure secret key

# Initialize Flask-Login for managing user sessions
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize Flask-SQLAlchemy and Flask-Migrate for database operations
db.init_app(app)
migrate = Migrate(app, db)

# Define a user loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define the route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Define the route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Process registration form submission
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username is already taken
        if User.query.filter_by(username=username).first():
            flash('Username already taken. Please choose another.', 'danger')
            return redirect(url_for('register'))
        # Create a new user and add to the database
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Define the route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Process login form submission
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the database for the user
        user = User.query.filter_by(username=username).first()

        # Check if the provided credentials are valid
        if user and user.password == password:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('forum'))

        flash('Invalid username or password. Please try again.', 'danger')

    return render_template('index.html')

# Define the route for user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# Define the route for the main forum page
@app.route('/forum')
def forum():
    return render_template('forum.html')

# Define the route for displaying all posts
@app.route('/posts')
def posts():
    # Fetch the category from the request parameters
    category = request.args.get('category')
    # If a category is specified, filter posts by that category
    if category:
        posts = Post.query.filter_by(category=category).all()
    else:
        # Otherwise, fetch all posts
        posts = Post.query.all()
    return render_template('posts.html', posts=posts, category_name=category)

# Define the route for creating a new post
@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()

    # Process the form submission for creating a new post
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        category = form.category.data

        predefined_categories = ['Pet Care Tips', 'Adoption Stories', 'Veterinary Advice', 'Pet Behavior',
                                 'Wildlife Conservation', 'Lost and Found', 'Animal-friendly Travel',
                                 'Pet Product Reviews', 'Local Animal Events']
        
        if category not in predefined_categories:
            flash('Invalid category selected.', 'danger')
            return redirect(url_for('create_post'))
        
        # Create a new post and add it to the database
        new_post = Post(title=title, content=content, author=current_user, category=category)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('posts', category=category))

    return render_template('create_post.html', form=form)

# Define the route for viewing a specific post
@app.route('/view_post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    # Retrieve the post with the given post_id from the database
    post = Post.query.get_or_404(post_id)

    # Increment post views if the current user is not the author
    if current_user != post.author:
        post.views += 1
        db.session.commit()
    
    # Process the form submission for adding a reply to the post
    if request.method == 'POST':
        reply_content = request.form.get('reply_content')
        new_reply = Reply(content=reply_content, author=current_user, post=post)
        db.session.add(new_reply)
        db.session.commit()

        # Redirect to the same post after submitting a reply
        return redirect(url_for('view_post', post_id=post.id))

    # Render the view_post.html template with the post and its replies
    return render_template('view_post.html', post=post)

# Define the route for updating a post
@app.route('/update_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Check if the current user is the author of the post
    if current_user != post.author:
        flash("You don't have permission to update this post.", 'danger')
        return redirect(url_for('posts'))

    form = PostForm(obj=post)

    # Process the form submission for updating a post
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()

        flash('Post updated successfully.', 'success')
        return redirect(url_for('posts'))

    return render_template('update_post.html', form=form, post=post)

# Define the route for deleting a post
@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Check if the current user is the author
    if current_user == post.author:
        try:
            # Delete replies associated with the post
            Reply.query.filter_by(post_id=post.id).delete()

            # Now, delete the post
            db.session.delete(post)
            db.session.commit()
            flash('Post deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting post: {str(e)}', 'danger')
    else:
        flash('You are not authorized to delete this post.', 'danger')

    return redirect(url_for('posts'))

# Define the route for liking a post
@app.route('/like_post/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get(post_id)
    if post:
        # Check if the user has already liked the post
        if current_user not in post.likers:
            # Increment the likes count
            post.likes += 1

            # Create a reply with a default content
            reply_content = "Liked this post!"
            new_reply = Reply(content=reply_content, author=current_user, post=post)

            # Add the reply to the session and commit changes
            db.session.add(new_reply)
            db.session.commit()

            # Update the likers list for the user
            current_user.liked_posts.append(post)
            db.session.commit()

            flash('You liked the post!', 'success')
        else:
            flash('You have already liked this post.', 'info')

    return redirect(url_for('view_post', post_id=post_id))

# Define the route for the "About Us" page
@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

# Define the route for displaying a list of all registered users
@app.route('/user_list')
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/categories')
def categories():
    predefined_categories = [
        'Pet Care Tips', 'Adoption Stories', 'Veterinary Advice', 'Pet Behavior',
        'Wildlife Conservation', 'Lost and Found', 'Animal-friendly Travel',
        'Pet Product Reviews', 'Local Animal Events'
    ]

    categories_info = [{'name': category, 'description': get_category_description(category)} for category in predefined_categories]

    return render_template('categories.html', categories=categories_info)

# Add a function to get category descriptions (modify it based on your preference)
def get_category_description(category):
    descriptions = {
        'Pet Care Tips': 'Discussions and tips on general pet care, grooming, and health.',
        'Adoption Stories': 'Heartwarming stories about pet adoptions and rescues.',
        'Veterinary Advice': 'Q&A and discussions about veterinary care, illnesses, and treatments.',
        'Pet Behavior': 'Tips and discussions on understanding and training pets.',
        'Wildlife Conservation': 'Discussions about global wildlife conservation efforts.',
        'Lost and Found': 'Help reunite lost pets with their owners.',
        'Animal-friendly Travel': 'Tips and recommendations for traveling with pets.',
        'Pet Product Reviews': 'Reviews and recommendations for pet-related products.',
        'Local Animal Events': 'Announcements and discussions about local animal-related events.'
    }

    return descriptions.get(category, 'No description available')  # Return a default if not found

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
