from ..utils import db


# USER MODEL
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    is_staff = db.Column(db.Boolean(), default=False)
    is_active = db.Column(db.Boolean(), default=False)

    # relationship: create relationship with orders
    orders = db.Relationship("Order", backref="customer", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

    # save user method
    def save(self):
        db.session.add(self)
        db.session.commit()

    # get user by id method
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
