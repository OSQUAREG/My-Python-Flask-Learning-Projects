from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint  # a class for creating Schema
# conint


"""
Notice that SQLAlchemy models (for creating DB Models) define attributes using =, and pass the type as a parameter to Column, like in:
name = Column(String)

while Pydantic models (for creating Schemas) declare the types using :, the new type annotation syntax/type hints:
name: str
"""


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # setting default to True


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str
    content: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Response Model Schema
class User(BaseModel):
    id: int
    email: EmailStr
    created_on: datetime

    class Config:
        orm_mode = True


# Response Model Schema - schema used to define what field should be returned.
class Post(PostBase):
    id: int
    created_on: datetime
    author_id: int
    author: User  # returning a pydantic model.

    class Config:
        orm_mode = True


class PostVote(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


"""
Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
This way, instead of only trying to get the id value from a dict, as in:
id = data["id"]

it will also try to get it from an attribute, as in:
id = data.id

And with this, the Pydantic model is compatible with ORMs, and you can just declare it in the response_model argument in your path operations.
You will be able to return a database model and it will read the data from it.
"""


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # dir is for the direction of the post, 1 for vote and 0 for no vote.

    # NB: the voter_id will come from the token data of the current user.
