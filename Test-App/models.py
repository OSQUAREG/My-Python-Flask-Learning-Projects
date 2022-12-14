from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, login_required, LoginManager, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.orm import relationship

# from uuid import uuid4
import os

# defining app and base directory
app = Flask(__name__)
base_dir = os.path.dirname(os.path.realpath(__file__))

# configuring the app db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    base_dir, "my_blog.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "026b0eb800ec2934fb5cf2e7"

upload_folder = "static/images/"
app.config["UPLOAD_FOLDER"] = upload_folder

db = SQLAlchemy(app)


# Creating Post Model
class Article(db.Model):
    # __tablename__ = "Posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(20))
    is_draft = db.Column(db.Boolean, nullable=False)

    # Relationship of an article to its comments.
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"Article: <{self.title}>"


# Creating User Model
class User(db.Model, UserMixin):
    # __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text(255), nullable=False, unique=True)
    isadmin = db.Column(db.Boolean, default=False, nullable=False)
    about_author = db.Column(db.Text(), nullable=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    # profile_pic = db.Column(db.String(), nullable=True)

    # Relationship of a user to her post(s) and comment(s)
    articles = db.relationship("Article", backref="author")
    comments = db.relationship("Comment", backref="commenter")

    def __repr__(self):
        return f"User: <{self.username}>"


# Creating Comments Model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text(), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Creating foreign keys that relate the comments to a user and an article
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"))

    def __repr__(self):
        return f"Comment by: <{self.name}>"


# Creating Message Model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String, nullable=False)
    message = db.Column(db.Text(), nullable=False)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Send by: <{self.name}>"


# test model
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"User: <{self.name}>"
    

with app.app_context():
    db.create_all()
    # db.drop_all()
