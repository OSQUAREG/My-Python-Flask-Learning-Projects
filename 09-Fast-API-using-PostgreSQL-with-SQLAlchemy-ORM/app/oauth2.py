from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer
from . import schemas, database, models
from sqlalchemy.orm import Session
from .config import settings


# Dependency: This bears the login path operation URL during which the token is generated.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

"""
Notes on Using Dependencies:
1) `db: Session = Depends(database.get_db)`: are added as argument for path operations that depends on connection/request to the database.
"""

# Constant Variables
"""
We will need: 
"""
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


# Function to Create the Access Token During Login Path Operation
def create_access_token(data: dict):
    # creating a copy of the data using .copy method (to avoid changing the data) to encode into the JWT token.
    to_encode = data.copy()

    # adding current time to amount of minutes to expire.
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # adding the expiry time to the data to encode as token
    to_encode.update({"exp": expire})

    # encoding all token data into the token string
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# Function to Decode and Verify the Access Token, and Return the Token Data
def verify_access_token(token: str, credentials_exception):
    try:
        # first, decode the token string
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # then tries to get the user id (or any other data encoded) from the token
        id: str = payload.get("user_id")  # NB: user_id was the token data passed during create_access_token was called in routes/auth.py

        # checks if id exist in the payload (the decoded token), else raise an error.
        if id is None:
            raise credentials_exception

        # validate the schema
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    # returns the user id or any other data encoded in the token.
    return token_data


# Dependency:
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    # decoding the token to return the token data encoded in the token.
    token = verify_access_token(token, credentials_exception)

    # getting the user.id (from the database) and verifying with token.id (decoded from the token).
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
    # return verify_access_token(token, credentials_exception)


"""
The `get_current_user` function takes in the `token: str` generated during the user login path operation, hence `oauth2_scheme` is passed as a Dependency.
This `get_current_user` then calls the `verify_access_token` function, which returns token data, which is needed to verify the user for a specific path operation.

For example, in the create_user route in routes/post.py, the `user_id: int = Depends(get_current_user())` is added to the path as a Dependency in the path arguments to return the user id (stored in a variable as `user_id`) as the required token data to verify the user before allowing access to the path.
"""