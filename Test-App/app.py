# from sqlalchemy.exc import IntegrityError
from models import app, db, User
from forms import SignUpForm, LoginForm
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    login_user,
    login_required,
    LoginManager,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


login_manager = LoginManager(app)
# login_manager.init_app(app)
# login_manager.login_view = "login"


@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))


@app.route("/")
def index():
    users = User.query.order_by(User.id).all
    # articles = Article.query.order_by(Article.date_created.desc()).all
    return render_template("index.html", users=users)


# FIXED
@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()

    if request.method == "POST":
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        about_author = form.about_author.data

        # checking if username and email already exists
        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()

        if user_exists:
            flash(f"Whoops!!! Username '{username}' already exist! Please try again...")
            return redirect(url_for("sign_up"))
        elif email_exists:
            flash(f"Whoops!!! Email '{email}' already exist! Please try again...")
            return redirect(url_for("sign_up"))
        else:
            # hashing the password
            password_hash = generate_password_hash(password)
            # creating an instance of user
            user = User(
                firstname=firstname,
                lastname=lastname,
                username=username,
                email=email,
                password_hash=password_hash,
                about_author=about_author,
                isadmin=bool(0),
            )
            # adding to the db
            db.session.add(user)
            db.session.commit()

            flash(f"Account signed up successfully!")
            return redirect(url_for("login"))
    return render_template("sign-up.html", form=form)


# FIXED
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit:
            username_email = form.username_email.data
            password = form.password.data

            user_exists = User.query.filter_by(username=username_email).first()
            email_exists = User.query.filter_by(email=username_email).first()

            if user_exists or email_exists:
                if user_exists:
                    if check_password_hash(user_exists.password_hash, password):
                        login_user(user_exists)
                        flash("Login Successful")
                        return redirect(url_for("dashboard"))
                    else:
                        password = ""
                        flash("Wrong Password! Please try again...")
                elif email_exists:
                    if check_password_hash(email_exists.password_hash, password):
                        login_user(email_exists)
                        flash("Login Successful")
                        return redirect(url_for("dashboard"))
                    else:
                        password = ""
                        flash("Wrong Password! Please try again...")
                else:
                    password = ""
                    flash("Wrong Password! Please try again...")
                    return redirect(url_for("login"))
            else:
                username_email = ""
                flash("Wrong Username or Email! Please try again...")
                return redirect(url_for("login"))

    return render_template("login.html", form=form)


# FIXED
@app.route("/dashboard")
def dashboard():
    id = current_user.id
    user = User.query.get_or_404(id)
    return render_template("dashboard.html", id=id, user=user)


# Logout Routing
@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You have been Logged Out!")
    return redirect(url_for("login"))



# TESTING ROUTES TO FIX THEM
from forms import TestForm
from models import Test

@app.route("/update")



@app.route("/article/view/<int:id>/add-comment", methods=["GET","POST"])
def add_comment(id):
    form = CommentForm()
    




if __name__ == "__main__":
    app.run(debug=True)
