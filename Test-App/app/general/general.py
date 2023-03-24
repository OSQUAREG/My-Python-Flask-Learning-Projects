from app.webforms import MessageForm
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from app.models import db, Article, User, Message
# from ..main import app, db
import os

blueprint = Blueprint("General",__name__, template_folder="templates")

# @app.route("/")
# def index():
#     return os.getenv("SECRET_KEY")

# Home Page Routing (done)
@blueprint.route("/")
def index():
    articles = Article.query.order_by(Article.date_posted.desc()).all
    authors = User.query.order_by(User.id).all
    if current_user.is_authenticated:
        firstname = current_user.firstname
        context = {"firstname" : firstname}
    context = {
        "articles" : articles,
        "authors" : authors,
        }
    return render_template("base.html", **context)
    # return "Showing index"


# # About Page Routing (done)
# @blueprint.route("/about")
# def about():
#     authors = User.query.order_by(User.id).all
#     return render_template("about.html", authors=authors)


# # Contact Page Routing (done)
# @blueprint.route("/contact", methods=["GET","POST"])
# def message():
#     form = MessageForm()

#     if request.method == "POST":
#         if form.validate_on_submit():
#             name = form.name.data
#             email = form.email.data
#             message = form.message.data

#             # adding new article to the db
#             contact = Message(
#                 name=name, email=email, message=message
#             )
#             db.session.add(contact)
#             db.session.commit()

#             # resetting/clearing the form
#             name = ""
#             email = ""
#             message = ""
#             flash(f"Message sent successfully")
#             return redirect(url_for("index"))
#         else:
#             flash(f"Whoops! Something went wrong. Please try again...")
#     return render_template("contact.html", form=form)
    