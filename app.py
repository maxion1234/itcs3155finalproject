from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from models import User, Post, Reply
from extensions import db
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from forms import PostForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:[REDACTED]@localhost:3306/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure secret key
login_manager = LoginManager(app)
login_manager.login_view = 'login'
db.init_app(app)
migrate = Migrate(app, db)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username is already taken
        if User.query.filter_by(username=username).first():
            flash('Username already taken. Please choose another.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('forum'))

        flash('Invalid username or password. Please try again.', 'danger')

    return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/forum')
def forum():
    return render_template('forum.html')

@app.route('/posts')
def posts():
    # Fetch posts data from the database
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_post = Post(title=title, content=content, author=current_user)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('posts'))

    return render_template('create_post.html', form=form)

@app.route('/view_post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    # Retrieve the post with the given post_id from the database
    post = Post.query.get_or_404(post_id)

    if current_user != post.author:
        post.views += 1
        db.session.commit()
    
    # If the request is a POST (i.e., user is submitting a reply)
    if request.method == 'POST':
        # Assuming you have a Reply model
        reply_content = request.form.get('reply_content')
        new_reply = Reply(content=reply_content, author=current_user, post=post)
        db.session.add(new_reply)
        db.session.commit()

        # Redirect to the same post after submitting a reply
        return redirect(url_for('view_post', post_id=post.id))

    # Render the view_post.html template with the post and its replies
    return render_template('view_post.html', post=post)

@app.route('/update_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Check if the current user is the author of the post
    if current_user != post.author:
        flash("You don't have permission to update this post.", 'danger')
        return redirect(url_for('posts'))

    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()

        flash('Post updated successfully.', 'success')
        return redirect(url_for('posts'))

    return render_template('update_post.html', form=form, post=post)

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
if __name__ == '__main__':
    app.run(debug=True)
