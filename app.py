from flask import Flask, request, redirect, url_for, render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from chatbot import chatbot_response

import os
import json
import random
import ssl
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import nltk

from models import db, Post, Comment, Like


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///community.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Initialize db with the app (only once)
db.init_app(app)

# Ensure upload folder exists

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# db = SQLAlchemy(app)

@app.route('/community', methods=['GET', 'POST'])
def community():
    if request.method == 'POST':
        # Handle post upload
        caption = request.form.get('caption')
        image = request.files['image']
        if image:
            filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_post = Post(image_filename=filename, caption=caption)
            db.session.add(new_post)
            db.session.commit()
        return redirect(url_for('community'))
    
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('community.html', posts=posts)

@app.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    content = request.form.get('content')
    if content:
        new_comment = Comment(post_id=post_id, content=content)
        db.session.add(new_comment)
        db.session.commit()
        # Return the new comment data in JSON format
        return jsonify({'content': new_comment.content})
    return jsonify({'error': 'No content provided'}), 400

@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    new_like = Like(post_id=post_id)
    db.session.add(new_like)
    db.session.commit()
    
    # Get the updated like count for the post
    like_count = Like.query.filter_by(post_id=post_id).count()
    return jsonify({'likes': like_count})

@app.route('/delete/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return '', 204

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_message = data.get('message', '')
    response = chatbot_response(user_message)  # Ensure chatbot() returns a response
    return jsonify({'response': response})

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')
    
    new_user = User(name=name, phone=phone, email=email, password=password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return render_template('index.html', success_message=f"Signup successful! Welcome, {name}.")
    except IntegrityError:
        db.session.rollback()
        return render_template('index.html', error_message="User already exists!")

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email, password=password).first()
    
    if user:
        return render_template('index.html', success_message=f"Login successful! Welcome back, {user.name}.")
    else:
        return render_template('index.html', login_error_message="No user found with these credentials.")
    

if __name__ == '__main__':
    app.run(debug=True)
