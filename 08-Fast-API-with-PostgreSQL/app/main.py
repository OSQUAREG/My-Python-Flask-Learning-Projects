import datetime
from random import randrange
from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel  # for creating our Schema
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# Init app
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # setting default to True
    # created_on: datetime.datetime


# Create connection to database
while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="p@ssword321",
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connection to database failed.")
        print("Error: ", error)
        time.sleep(3)


# creating an in-memory variable to work with
# using a dict constructor
my_posts = [
    dict(title="Title of Post One",
         content="This is the content of post one.",
         published=True,
         rating=3,
         id=1
         ),
    dict(title="Title of Post Two",
         content="This is the content of post two.",
         published=False,
         rating=None,
         id=2
         )
]


# Create a function to find post by id (NB: for DB, we use query)
def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


# Create a function to get the index of a post dictionary in the my_post list.
def find_post_index(id):
    for i, post in enumerate(my_posts):  # to get the specific index as well as the post.
        if post["id"] == id:
            return i  # returning the specific index.


# Test Get Route
@app.get("/")
def root():
    return {"message": "Hello, just learning Python Fast API"}


# Retrieve All Posts
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")  # queries the database
    posts = cursor.fetchall()  # to fetch the result into the application
    # print(posts)  # to check results in terminal.
    return {'data': posts}


# Create Post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))

    # use %s to avoid SQL injection from users instead of...
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUE ({post.title}, {post.content},
    #                                                                          {post.published}) RETURNING * """))
    new_post = cursor.fetchone()  # fetch the query result
    conn.commit()  # save to db

    return {"data": new_post}


# Retrieve a Post by id
@app.get("/posts/{id}")
def get_posts(id: int):
    """
    You can pass the id as id:int into the get_post function to convert and validate that it's a number. however,
    we need to convert back to a string to pass is as vars in the query.
    """
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, str(id))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")

    return {'data': post}


# Delete a Post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, str(id))
    post = cursor.fetchone()
    conn.commit()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # we can use this...
    # return {"message": f"Post with id: {id} was deleted successfully"}
    # but when using the 204 status code, no content should be sent, so we will use below instead...


# Update a Post
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                   (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    conn.commit()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    return {"data": post}
