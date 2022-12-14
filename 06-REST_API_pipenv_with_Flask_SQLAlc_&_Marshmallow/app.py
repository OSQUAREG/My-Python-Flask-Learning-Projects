"""
$ python --version   #to check that python3 is installed, if not download from website: https://www.python.org/downloads/.
$ pip3 install pipenv   #to install pyhton3 virtual environment manager
$ pipenv shell  #to activate the virtual environment
$ pipenv install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy OR
$ pipenv install flask flask-sqlalchemy flask_marshmallow marshmallow-sqlalchemy
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
# Define base directory for db
basedir = os.path.abspath(os.path.dirname(__file__))

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Init db
db = SQLAlchemy(app)


# Create db with app_context
@app.before_first_request
def create_db():
    with app.app_context():
        db.create_all()


# Run Server
if __name__ == "__main__":
    app.run(debug=True)