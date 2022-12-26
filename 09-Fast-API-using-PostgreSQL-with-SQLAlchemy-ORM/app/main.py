from fastapi import FastAPI
from . import models
from .routes import post, user, auth, vote
from .database import engine

# Init app
app = FastAPI()

# # Create all models in models.py
# models.Base.metadata.create_all(bind=engine)  # commented out since Alembic will be handling all database table creation and operations.

# Include the post, user and auth router from post.py, user.py and auth.py to the main.py. So when the code is run, the app goes into the post, user and auth files and find a match to the router.
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Test Get Route (without ORM)
@app.get("/test")
def root():
    return {"message": "Hello, just learning Python Fast API"}