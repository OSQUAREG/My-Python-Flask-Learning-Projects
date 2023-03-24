from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base


"""
Notice that SQLAlchemy models (for creating DB Models) define attributes using =, and pass the type as a parameter to Column, like in:
name = Column(String)

while Pydantic models (for creating Schemas) declare the types using :, the new type annotation syntax/type hints:
name: str
"""


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_on = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    # Create Foreign Key for Posts from the users table
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Create a Relationship with the User model as an author
    author = relationship("User")  # to fetch the user details from the User model table.

    # NB: for setting default value on Server DBs, use server_default='', instead of: default=True/False for Server Database tables.


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_on = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


"""
Composite Keys are primary keys that spans multiple columns. 
This is used, for example, when you want a user not to like a post twice, and whereas in the table fields, duplicate post_id and user_id can exist.
"""


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
