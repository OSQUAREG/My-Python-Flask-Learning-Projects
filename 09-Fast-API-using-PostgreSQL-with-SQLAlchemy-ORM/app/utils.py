from passlib.context import CryptContext


# Telling Passlib the hashing algorithm to use, which is "bcrypt"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)
