"""
SQLAlchemy engine and session setup.

get_db() is a FastAPI dependency: each request gets its own session,
which is closed automatically when the request finishes, even if the
handler raises an exception. Routers never construct a session
themselves — they receive one through this dependency.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

'''
a database connection created for thread on is strictly locked for thread one
so  here we want to use the same thread on multiple user requests
'''
connect_args = (
    {"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {}
)
'''
How to talk to the database
'''
engine = create_engine(settings.database_url, connect_args=connect_args)

'''
queries to the db are done through sessions that than on the engine?
'''

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

'''
the model that all the database tables inherit from from class to db table
'''
Base = declarative_base()

'''
request comes to use the db, a session is created via yield 
endpoint does the db work, endpoint finishes then we hit finally to close the session

'''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()