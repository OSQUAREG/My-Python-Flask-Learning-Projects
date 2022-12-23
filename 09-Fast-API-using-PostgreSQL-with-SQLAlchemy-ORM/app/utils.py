from passlib.context import CryptContext


# Telling Passlib the hashing algorithm to use, which is "bcrypt"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify(password, password_h):
    return pwd_context.verify(password, password_h)
