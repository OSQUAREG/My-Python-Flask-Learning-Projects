from flask import Flask, request, jsonify
from sqlalchemy.engine import Engine
from flas_sqlalchemy import SQLAlchemy.


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQL_TRACK_MODIFICATION"] = 1

# configure sqlite3 to enforce foreign constraint.
@event.listens_for(Engine, "connect")


class User(db.Model):
    __tablename__ = "user"
    class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.Relationship("BlogPost")