from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # user (owner) foreign key for store(s)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    # store(s) relationship to a user (owner)
    owner = db.relationship("UserModel", back_populates="stores")
    # a store relationship to items
    items = db.relationship("ItemModel", back_populates="store")