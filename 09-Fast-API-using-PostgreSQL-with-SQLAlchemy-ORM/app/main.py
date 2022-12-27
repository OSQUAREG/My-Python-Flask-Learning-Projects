from fastapi import FastAPI
from .routes import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# from . import models
# from .database import engine

# Init app
app = FastAPI()

# # Create all models in models.py
# models.Base.metadata.create_all(bind=engine)  # commented out since Alembic will be handling all database table creation and operations.

# Setting Up CORS Middleware.
"""
CORS or "Cross-Origin Resource Sharing" refers to the situations when a frontend running in a browser has JavaScript code that communicates with a backend, and the backend is in a different "origin" than the frontend.

Read more about CORS here: https://fastapi.tiangolo.com/tutorial/cors/
See how to setup here: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

Middleware is a basically a function used in most framework that runs before any request.
"""

origins = ["https://web.facebook.com", "https://www.youtube.com"]

# use a wildcard "*" if you want your API to communicate with all sites, or specify the domain your API is created for. For example, ["https://www.google.com", "https://www.facebook.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the post, user and auth router from post.py, user.py and auth.py to the main.py. So when the code is run, the app goes into the post, user and auth files and find a match to the router.
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Test Get Route (without ORM)
@app.get("/")
def root():
    return {"message": "Hello, just learning Python Fast API"}