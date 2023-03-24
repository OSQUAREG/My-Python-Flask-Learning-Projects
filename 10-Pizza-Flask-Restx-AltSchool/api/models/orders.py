from ..utils import db
from enum import Enum
from datetime import datetime


# Create a class Size for Enum function
class OrderSizes(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extra-large"


# Create a class Status for Enum function
class OrderStatus(Enum):
    PENDING = "pending"
    IN_TRANSIT = "in-transit"
    DELIVERED = "delivered"


# ORDER MODEL
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer(), primary_key=True)
    size = db.Column(db.Enum(OrderSizes), default=OrderSizes.SMALL) 
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)
    flavour = db.Column(db.String(), nullable=False)
    quantity = db.Column(db.Integer(), default=1)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)

    # relationship: create foreign key with user
    customer_id = db.Column(db.Integer(), db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<Order {self.id}>"

    # save method
    def save(self):
        db.session.add(self)
        db.session.commit()

    # delete method
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # update method
    def update(self):
        db.session.commit()

    # get order by id method
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    # update status method
    # @classmethod
    def update_status_with_get_json(self, data):   
        self.status = data.get("status")  #for request.get_json   
        db.session.commit()


    # update status method
    def update_status_with_payload(self, data):    
        self.status = data["status"]  #for order_namespace.payload   
        db.session.commit()
