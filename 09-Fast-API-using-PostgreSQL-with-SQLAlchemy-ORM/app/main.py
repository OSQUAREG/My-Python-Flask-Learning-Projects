from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2  # postgres db driver
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
# from .models import Post
# from .schemas import Post
from .database import engine, get_db

# Init app
app = FastAPI()

# Create all models in models.py
models.Base.metadata.create_all(bind=engine)

"""
Notice that SQLAlchemy models define attributes using =, and pass the type as a parameter to Column, like in:
name = Column(String)

while Pydantic models declare the types using :, the new type annotation syntax/type hints:
name: str
"""

# Create connection to PostgreSQL database
while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="password321",
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")  # just to show results in terminal
        break
    except Exception as error:
        print("Connection to database failed.")
        print("Error: ", error)
        time.sleep(3)


# Test Get Route (without ORM)
@app.get("/test")
def root():
    return {"message": "Hello, just learning Python Fast API"}


# Test Route (with SQLAlchemy ORM)
@app.get("/")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}


# Create Post (without ORM)
@app.post("/test-posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Post):
    # use %s to avoid SQL injection from users instead of...
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUE ({post.title}, {post.content},  {post.published}) RETURNING * """))
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()  # fetch the query result
    conn.commit()  # save to db
    return {"data": new_post}


# Create Post (with SQLAlchemy ORM)
@app.post("/posts", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # Instead of typing in all the fields like this...
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # use **post.dict() to unpack the post as a dict into the Post model like this...
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # to add the "RETURNING *" statement functionality.
    return new_post


# Retrieve All Posts (without ORM)
@app.get("/test-posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")  # queries the database
    posts = cursor.fetchall()  # to fetch the result into the application
    # print(posts)  # to check results in terminal.
    return {'data': posts}


# Retrieve All Posts (with SQLAlchemy ORM)
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(db.query(models.Post))  # to see what actually happens (abstraction) in the terminal.
    return posts


# Retrieve a Post by id (without ORM)
@app.get("/test-posts/{id}")
def get_post(id: int):
    """
    You can pass the id as id:int into the get_post function to convert and validate that it's a number. however,
    we need to convert back to a string to pass is as vars in the query.
    """
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, str(id))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    return {'data': post}


# Retrieve a Post by id (with SQLAlchemy ORM)
@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(id)
    # you can also use this...
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    return post


# Delete a Post (without ORM)
@app.delete("/test-posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, str(id))
    post = cursor.fetchone()
    conn.commit()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # we can use this...
    # return {"message": f"Post with id: {id} was deleted successfully"}
    # but when using the 204 status code, no content should be sent.


# Delete a Post (with SQLAlchemy ORM)
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(id)

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")

    # db.delete(post)  # this also works, instead of this...
    post.delete(synchronize_session=False)  # calling the query.delete method
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # read docs for synchronize_session @ https://docs.sqlalchemy.org/en/14/orm/session_basics.html#selecting-a-synchronization-strategy


# Update a Post (without ORM)
@app.put("/test-posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: schemas.Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    conn.commit()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")

    return {"data": post}


# Update a Post (with SQLAlchemy ORM)
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db)):
    post_to_update = db.query(models.Post).filter(models.Post.id == id)
    post = post_to_update.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")

    post_to_update.update(updated_post.dict(), synchronize_session=False)  # calling the query.update method
    db.commit()

    return post_to_update.first()


# Create User
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Retrieve All Users
@app.get("/users", status_code=status.HTTP_200_OK, response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


# Retrieve a User
@app.get("/users/{id}", status_code=status.HTTP_200_OK, response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(id)
    # user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
    return user
