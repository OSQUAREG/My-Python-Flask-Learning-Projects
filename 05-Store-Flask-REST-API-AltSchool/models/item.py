from db import db


class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    # precision for Float data type: allows to set the number of decimal places

    # store foreign key for items
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
    # item(s) relationship to a store
    store = db.relationship("StoreModel", back_populates="items")