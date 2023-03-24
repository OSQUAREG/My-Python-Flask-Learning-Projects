from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import os

# creating the path where the db will be stored, same as the app file.
base_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + \
    os.path.join(base_dir, 'users.db')  # defining the db type and name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

gender_dropdown = ["Male", "Female", "Rather Not Say"]

# Creating the class User


class User(db.Model):
    # defining the table name
    __tablename__ = 'user'
    # defining the table columns
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f"User {self.username}"


@app.route("/")
def index():
    # querying the user table
    users = User.query.all()

    # creating a context dictionary
    context = {
        "users": users
    }

    return render_template('index.html', **context)

# Creating User


@app.route("/users", methods=["POST"])
def create_user():
    form_username = request.form.get('username')
    form_email = request.form.get('email')
    form_age = request.form.get('age')
    gender = request.form.get('gender')

    # creating a user instance, by collecting user data from form fields.
    add_user = User(username=form_username, email=form_email,
                    age=form_age, gender=gender)

    db.session.add(add_user)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/dropdown", methods=['GET'])
def dropdown():
    gender = ["Male", "Female", "Rather Not Say"]
    # return redirect(url_for('index'))
    return render_template('index.html', gender=gender)


# Updating a user


@app.route("/update/<int:id>/", methods=["GET", "POST"])
def update(id):
    user_to_update = User.query.get_or_404(id)

    if request.method == "POST":
        user_to_update.username = request.form.get('username')
        user_to_update.email = request.form.get('email')
        user_to_update.age = request.form.get('age')
        user_to_update.gender = request.form.get('gender')

        db.session.commit()  # when doing the Update function, only session.commit is used

        return redirect(url_for("index"))

    context = {
        'user': user_to_update
    }

    return render_template("update.html", **context)

# Deleting a user


@app.route("/delete/<int:id>/")
def delete(id):
    user_to_delete = User.query.get_or_404(id)
    db.session.delete(user_to_delete)
    db.session.commit()

    return redirect(url_for("index"))

# Creating a route for a separate htnl to display the users table


@app.route("/userstable/")
def users():
    # querying the user table
    users = User.query.all()

    # creating a context dictionary
    context = {
        "users": users
    }

    return render_template('users.html', **context)


if __name__ == "__main__":
    app.run(debug=True)


'''
To Create the DB file, manually run in the command terminal run:
$ python
>>> from app import app, db, User
>>> app.app_context().push()
>>> db.create_all()

OR using flask shell, run:
$ flask shell
>>> db.create_all()

OR simply:
$ python
>>> from app import app, db, User
>>> db.create_all()
'''
