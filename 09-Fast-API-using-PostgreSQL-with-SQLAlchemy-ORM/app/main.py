from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2  # postgres db driver
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .routes import post, user, auth
from .database import engine, get_db

# from .utils import create_connection

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

# Create connection to Postgres database
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


# Include the post and user router from post.py and user.py to the main.py. SO when the code is run, the app goes into the post and user file and find a match to the router.
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


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
def create_post(post: schemas.PostCreate):
    # use %s to avoid SQL injection from users instead of...
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUE ({post.title}, {post.content}, {post.published}) RETURNING * """))
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))

    new_post = cursor.fetchone()  # fetch the query result
    conn.commit()  # save to db
    return {"data": new_post}


# Retrieve All Posts (without ORM)
@app.get("/test-posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")  # queries the database
    posts = cursor.fetchall()  # to fetch the result into the application
    # print(posts)  # to check results in terminal.
    return {'data': posts}


# Retrieve a Post by id (without ORM)
@app.get("/test-posts/{id}")
def get_post(id: int):
    """
    You can pass the id as id:int into the get_post function to convert and validate that it's a number. however,
    we need to convert back to a string to pass is as vars in the query.
    """
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    return {'data': post}


# Delete a Post (without ORM)
@app.delete("/test-posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    post = cursor.fetchone()
    conn.commit()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # we can use this...
    # return {"message": f"Post with id: {id} was deleted successfully"}
    # but when using the 204 status code, no content should be sent.


# Update a Post (without ORM)
@app.put("/test-posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: schemas.PostCreate):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    conn.commit()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")

    return {"data": post}
