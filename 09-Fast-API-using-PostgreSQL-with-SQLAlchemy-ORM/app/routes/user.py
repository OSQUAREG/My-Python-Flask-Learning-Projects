from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils, database

# Adding FastAPI Router with a prefix and tags (to group the routes)
router = APIRouter(prefix="/users", tags=["Users"])  # used instead of importing app from main.py

"""
Notes on Using Dependencies:
1) `db: Session = Depends(database.get_db)`: are added as argument for path operations that depends on connection/request to the database.
"""


# Create User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):

    # hashing the user.password
    password_hash = utils.hash_password(user.password)
    user.password = password_hash  # passing the hashed password back to the user.password

    # use **user.dict() to unpack the new user data as a dict into the Post model like this...
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Read All Users
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.User])
def get_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users


# Read a User
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.User)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).get(id)
    # user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
    return user
