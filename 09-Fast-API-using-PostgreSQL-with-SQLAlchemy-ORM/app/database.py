from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base  # for creating DB models
from sqlalchemy.orm import sessionmaker
import psycopg2  # postgres db driver
from psycopg2.extras import RealDictCursor
import time
from .config import settings

"""
# Template for connecting to a local DB: 
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Template for connecting to an external DB server: 
SQLALCHEMY_DATABASE_URL = "postgresql://database_username:database_password@databsae_hostname:database_port/database_name"

# Saving the Environment Variables in different variables
db_username = settings.database_username
db_password = settings.database_password
db_hostname = settings.database_hostname
db_port = settings.database_port
db_name = settings.database_name

# Adding the f string to use the saved variables
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_name}"
"""

db_username = settings.database_username
db_password = settings.database_password
db_hostname = settings.database_hostname
db_port = settings.database_port
db_name = settings.database_name

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

"""
Now use the SessionLocal class we created in the database.py file to create a dependency.
We need to have an independent database session/connection (SessionLocal) per request, use the same session through all the request and then close it after the request is finished.
And then a new session will be created for the next request.
Our dependency will create a new SQLAlchemy SessionLocal that will be used in a single request, and then close it once the request is finished.
"""


# Dependency: this creates a session to the DB whenever there is request to the DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# To Create Connection to Postgres Database without ORM
while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="password321",
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")  # just to show results in terminal
        break
    except Exception as error:
        print("Connection to database failed.")
        print("Error: ", error)
        time.sleep(3)