from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy
from src.blueprints.auth import auth_bp
from extensions import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5434/database_name'
db.init_app(app)

app.register_blueprint(auth_bp)

#TO DO - deal with routes - might only need the one for index.html in this file

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/forum')
def forum():
    return render_template('forum.html')

if __name__ == '__main__':
    app.run(debug=True)
