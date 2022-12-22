# from sqlalchemy.orm import Session
#
# from . import models, schemas
#
#
# # Test Get Route (without ORM)
# @app.get("/")
# def root():
#     return {"message": "Hello, just learning Python Fast API"}
#
#
# # Test Route (with SQLAlchemy ORM)
# @app.get("/test")
# def test_posts(db: Session = Depends(get_db)):
#     return {"status": "success"}
#
#
# # Create Post (without ORM)
# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(post: schemas.Post):
#     # use %s to avoid SQL injection from users instead of...
#     # cursor.execute("""INSERT INTO posts (title, content, published) VALUE ({post.title}, {post.content},
#     #                                                                          {post.published}) RETURNING * """))
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
#                    (post.title, post.content, post.published))
#     new_post = cursor.fetchone()  # fetch the query result
#     conn.commit()  # save to db
#     return {"data": new_post}
#
#
# # Create Post (with SQLAlchemy ORM)
# @app.get("/createposts")
# def create_posts(post: schemas.Post, db: Session = Depends(get_db)):
#     new_post = models.Post(title=post.title, content=post.content, published=post.published)
#     db.add(new_post)
#     db.commit()
#     post_new = db.refresh(new_post)
#     return {"data": post_new}
#
#
# # Retrieve All Posts (without ORM)
# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")  # queries the database
#     posts = cursor.fetchall()  # to fetch the result into the application
#     # print(posts)  # to check results in terminal.
#     return {'data': posts}
#
#
# # Retrieve All Posts (with SQLAlchemy ORM)
# @app.get("/orm_posts")
# def get_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     # p_check = PostModel.db.query(PostModel)  # to see what actually happens in the terminal.
#     # print(posts)
#     return {"data": posts}
#
#
# # Retrieve a Post by id
# @app.get("/posts/{id}")
# def get_posts(id: int):
#     """
#     You can pass the id as id:int into the get_post function to convert and validate that it's a number. however,
#     we need to convert back to a string to pass is as vars in the query.
#     """
#     cursor.execute("""SELECT * FROM posts WHERE id = %s """, str(id))
#     post = cursor.fetchone()
#
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id: {id} was not found")
#
#     return {'data': post}
#
#
# # Delete a Post
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, str(id))
#     post = cursor.fetchone()
#     conn.commit()
#
#     if post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id: {id} not found")
#
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
#     # we can use this...
#     # return {"message": f"Post with id: {id} was deleted successfully"}
#     # but when using the 204 status code, no content should be sent, so we will use below instead...
#
#
# # Update a Post
# @app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
# def update_post(id: int, post: schemas.Post):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
#                    (post.title, post.content, post.published, str(id)))
#     post = cursor.fetchone()
#     conn.commit()
#
#     if post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id: {id} not found")
#
#     return {"data": post}
