from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, oauth2, database

# Using FastAPI Router with a prefix and tags (to group the routes)
router = APIRouter(prefix="/posts", tags=["Posts"])  # used instead of importing app from main.py

"""
Notes on Using Dependencies:
1) `db: Session = Depends(database.get_db)`: are added as argument for path operations that depends on connection/request  to the database.

2) `current_user: int = Depends(oauth2.get_current_user)`: are added as arguments for path operations that needs to verify that user is logged in to perform the path operation and to only allow those logged in.
"""


# Create Post (with SQLAlchemy ORM)
@router.post("/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    # printing to see what is actually happening (abstraction) in the terminal
    print(current_user.id)  # just to print in the terminal the user id accessing the path.
    print(current_user.email)

    # # Instead of typing in all the fields like this...
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    # # use **post.dict() to unpack the post as a dict into the Post model like this, also sets the current user as the author
    new_post = models.Post(author_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # to add the "RETURNING *" statement functionality.
    return new_post


# Retrieve All Posts (with SQLAlchemy ORM)
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    # printing to see what is actually happening (abstraction) in the terminal
    print(current_user.id)  # to see the user id accessing the path in the terminal.
    print(db.query(models.Post))
    print(db.query(models.Post).filter(models.Post.author_id == current_user.id))

    # # to Retrieve all users posts.
    # posts = db.query(models.Post).all()

    # to retrieve only logged-in user's posts.
    posts = db.query(models.Post).filter(models.Post.author_id == current_user.id).all()

    return posts


# Retrieve a Post by id (with SQLAlchemy ORM)
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    # printing to see what is actually happening (abstraction) in the terminal
    print(current_user.id)  # to see the user id accessing the path in the terminal.
    print(db.query(models.Post).filter(models.Post.id == id))

    # to retrieve any post by any user
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # you can also use this...
    # post = db.query(models.Post).get(id)

    # # to retrieve ONLY logged-in user's post.
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    # check if post exists
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    # # check if current user is the author retrieving own post
    # if post.author_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return post


# Delete a Post (with SQLAlchemy ORM)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    print(current_user.id)  # just to print in the terminal the user id accessing the path.

    post_query = db.query(models.Post).filter(models.Post.id == id)

    # check if post exists
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")

    # check if current user is the author
    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    # db.delete(post)  # this also works, instead of this...
    post_query.delete(synchronize_session=False)  # NB: query.delete method is only performed on the query and not the post itself.
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # read docs for synchronize_session @ https://docs.sqlalchemy.org/en/14/orm/session_basics.html#selecting-a
    # -synchronization-strategy


# Update a Post (with SQLAlchemy ORM)
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)  # just to print in the terminal the user id accessing the path.

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")

    # check if current user is the author
    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)  # NB: query.update method is only performed on the query and not the post itself.
    db.commit()

    return post
