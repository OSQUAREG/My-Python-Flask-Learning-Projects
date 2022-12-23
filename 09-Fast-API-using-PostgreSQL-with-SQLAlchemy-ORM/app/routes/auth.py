from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

# Using FastAPI Router with tags (to group the routes)
router = APIRouter(tags=["Authentication"])  # used instead of importing app from main.py

"""
OAuth2PasswordRequestForm is a form with "username" and "password" fields to receive the user credentials.

So for below login route, we will replace the schemas.UserLogin with the form, and replace the user_credentials.email with .username, but the string inputted is still an email.

In the API test interface, we no longer enter the data in the body, but we enter it in the form-data or form-URL.
"""


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # checking user email from User Model
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    # verifying user password with user hashed password in User Model
    pwd = utils.verify(user_credentials.password, user.password)
    if not pwd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # NB: you can add as many data as you want into the access token data which is a List.

    return {"access_token": access_token, "token_type": "bearer"}
