from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from config import settings
from app.general import general
from app.models import db, User
# from routes import articles, users

# def create_app():
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = settings.database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = settings.secret_key

# db = SQLAlchemy(app)

db.init_app(app)

# CKEDITOR CONFIG FOR WEB FORMS
app.config["CKEDITOR_HEIGHT"] = 400
app.config["CKEDITOR_WIDTH"] = 2000
ckeditor = CKEditor(app)

# LOGIN MANAGER SET UP
login_man = LoginManager(app)
# login_manager.init_app(app)
login_man.login_view = "login"

@login_man.user_loader
def user_loader(id):
    return User.query.get(int(id))


# Create all DB tables
with app.app_context():
    db.create_all()

app.register_blueprint(general.blueprint, url_prefix="")
# app.register_blueprint(users.blueprint, url_prefix="")
# app.register_blueprint(articles.blueprint, url_prefix="")

# @app.route("/")
# def index():
#     return "Hello"



    # return app

# app_run = create_app()

# if __name__ == "__main__":
#     app.run(debug=True) 