from random import randrange
from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel  # for creating our Schema

# Init app
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # setting default to True
    rating: Optional[int] = None


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
    for i, post in enumerate(my_posts): # to get the specific index as well as the post.
        if post["id"] == id:
            return i # returning the specific index.

# def create_id()
#     for i in my_posts["id"]:
#         if

# Test Get Route
@app.get("/")
def root():
    return {"message": "Hello, just learning Python Fast API"}


# Retrieve All Posts
@app.get("/posts")
def get_posts():
    return {'data': my_posts}


# Create Post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    post_dict = new_post.dict() # convert to a dictionary using .dict() method.
    post_dict['id'] = randrange(0, 1000) # assigning a random number as the id.

    post = my_posts.append(post_dict) # to append to my_post list.
    return dict(data=post_dict)  # using a dictionary constructor


# Retrieve a Post by id
@app.get("/posts/{id}")
def get_posts(id:int):
    """
    You can pass the id as id:int into the get_post function to convert the number to an integer, to avoid reading it as a string.
    OR you can pass int(id) into the find_post function to convert the id to an integer if its convertible as well.
    """
    print(type(id)) # let's just see id datatype in the terminal

    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    return {'data': post}


# Delete a Post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_post_index(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")

    my_posts.pop(index) # to remove or delete from my_post

    # we can use this...
    # return {"message": f"Post with id: {id} was deleted successfully"}
    # but when using the 204 status code, no content should be sent, so we will use below instead...
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts")
# def update_post(post: Post):
#     post_dict = post.dict()
