# $ pip install sqlalchemy

from sqlalchemy import create_engine, Integer, String, DateTime, Boolean, Column
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine("sqlite:///tasks.db") # echo=True to show how the db was created in the Terminal
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

"""
    class Tasks:
        id int
        content str
        date_added datetime
        is_completed boolean
"""

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer(), primary_key=True)
    content = Column(String(500), nullable=False)
    date_added = Column(DateTime(), default=datetime.utcnow)
    is_completed = Column(Boolean(), default=False)

    def __repr__(self):
        return f"<Task: {self.id}>"

Base.metadata.create_all(bind=engine)

# to create the db file, run db.py using: $ python db.py

"""
    # SQL Query version for Creating the Task Tables when you run db.py
    CREATE TABLE tasks (
        id INTEGER NOT NULL,
        content VARCHAR(500) NOT NULL,
        date_added DATETIME,
        is_completed BOOLEAN,
        PRIMARY KEY (id)
    ) 
"""